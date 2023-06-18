from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Tuple

from cstest.content.errors.error import var_error_string
from cstest.content.variable.validators import CallVarValidator


class Resolver(ABC):
    call_name: str

    @abstractmethod
    def splitter(self) -> list[str]:
        """Splits a variable name call into its constituent components (i.e.,
        where the name is a composite of other variable values)"""
        ...

    @abstractmethod
    def validate_struct(self) -> list[str]:
        """Validates the structure of a variable name call"""
        ...

    @abstractmethod
    def resolve(
        self, game_variables: dict[str, Any] = {}
    ) -> Tuple[list[str], str, Any]:
        """Creates the actual name of the variable (at run time) that is called
        (provided it is valid) - Composite names are dependent on actual
        value of the constituent variable names"""
        ...

    @abstractmethod
    def process(self, game_variables: dict[str, Any]) -> Tuple[list[str], str, Any]:
        """Calls the components of the resolver class to enable full processing of
        a variable name"""


@dataclass
class ResolveBaseVariable(Resolver):
    """Resolver class for 'base' variables, i.e., those without square brackets
    or hashes. E.g., ${variable_name}"""

    call_name: str

    def splitter(self) -> list[str]:
        return [self.call_name]

    def validate_struct(self) -> list[str]:
        CallVarValidator(self.call_name).is_blank()
        return CallVarValidator(self.call_name).is_name_valid()

    def resolve(
        self, game_variables: dict[str, Any] = {}
    ) -> Tuple[list[str], str, Any]:
        if CallVarValidator(self.call_name, list(game_variables.keys())).is_defined():
            return [], self.call_name, game_variables[self.call_name]
        else:
            return [var_error_string("inv_var", self.call_name)], "", ""

    def process(self, game_variables: dict[str, Any]) -> Tuple[list[str], str, Any]:
        errors = self.validate_struct()
        return (self.resolve(game_variables)) if not errors else (errors, "", "")


@dataclass
class ResolveHashVariable(Resolver):
    call_name: str

    def splitter(self) -> list[str]:
        return self.call_name.split("#")

    def validate_struct(self) -> list[str]:
        CallVarValidator(self.call_name).is_blank()

        errors = []
        if not CallVarValidator(self.call_name).single_hash():
            return [var_error_string("multiple_hash", self.call_name)]

        split = self.splitter()
        errors.extend(CallVarValidator(split[0]).is_name_valid())
        if not CallVarValidator(split[1]).hash_is_number():
            errors.append(var_error_string("hash_not_number", self.call_name))

        return errors

    def resolve(
        self, game_variables: dict[str, Any] = {}
    ) -> Tuple[list[str], str, Any]:
        split = self.splitter()

        var = ResolveBaseVariable(split[0].replace("]", ""))
        errors, _, value = var.process(game_variables)
        split_val = int(split[1]) - 1

        if not errors:
            try:
                out_val = str(value)[split_val]
                return errors, self.call_name, out_val
            except IndexError:
                errors.append(var_error_string("inv_hash", self.call_name))
                return errors, "", ""
        else:
            return errors, "", ""

    def process(self, game_variables: dict[str, Any]) -> Tuple[list[str], str, Any]:
        errors = self.validate_struct()
        return (self.resolve(game_variables)) if not errors else (errors, "", "")


@dataclass
class ResolveBracketVariable(Resolver):
    call_name: str

    def splitter(self) -> list[str]:
        return self.call_name.split("[")

    def validate_struct(self) -> list[str]:
        CallVarValidator(self.call_name).is_blank()

        errors = []
        if CallVarValidator(self.call_name).is_first_bracket():
            errors.append(var_error_string("first_alpha", self.call_name))
        elif CallVarValidator(self.call_name).is_equal_bracket():
            for variable in self.splitter():
                errors.extend(
                    CallVarValidator(variable.replace("#", "")).is_name_valid()
                )
                if "#" in variable:
                    if not CallVarValidator(variable).hash_correct_place():
                        errors.append(
                            var_error_string("hash_incorrect_place", self.call_name)
                        )
                    errors.extend(
                        ResolveHashVariable(variable.replace("]", "")).validate_struct()
                    )

        else:
            errors.append(var_error_string("mismatch_bracket", self.call_name))

        return errors

    def resolve(
        self, game_variables: dict[str, Any] = {}
    ) -> Tuple[list[str], str, Any]:
        final_variable = ""
        bracket_value = ""
        errors: list[str] = []
        full_errors: list[str] = []
        length = len(self.splitter())

        for iteration, part_name in enumerate(reversed(self.splitter())):
            if iteration + 1 == length:
                final_variable = f"{part_name}{bracket_value}{final_variable}"
                var = ResolveBaseVariable(final_variable.replace("]", ""))
                errors, name, value = var.process(game_variables)
                full_errors.extend(errors)
                return full_errors, name, value

            else:
                if not full_errors:
                    if part_name.count("]") == 1:
                        if bracket_value != "":
                            final_variable = f"{bracket_value}{final_variable}"
                            bracket_value = ""

                        if "#" in part_name:
                            hash_var = ResolveHashVariable(
                                f"{part_name}".replace("]", "")
                            )
                            errors, name, value = hash_var.process(game_variables)
                        else:
                            var = ResolveBaseVariable(f"{part_name}".replace("]", ""))
                            errors, name, value = var.process(game_variables)

                        if errors:
                            full_errors.extend(errors)
                            return full_errors, "", ""
                        else:
                            final_variable = f"_{value}{final_variable}"
                    else:
                        if "#" in part_name:
                            hash_var = ResolveHashVariable(
                                f"{part_name}{bracket_value}".replace("]", "")
                            )
                            errors, name, value = hash_var.process(game_variables)
                        else:
                            var = ResolveBaseVariable(
                                f"{part_name}{bracket_value}".replace("]", "")
                            )
                            errors, name, value = var.process(
                                game_variables,
                            )
                        bracket_value = f"_{value}"
                        full_errors.extend(errors)
                else:
                    return full_errors, "", ""

        return full_errors, "", ""

    def process(self, game_variables: dict[str, Any]) -> Tuple[list[str], str, Any]:
        return [], "", ""
