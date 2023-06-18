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
    def val_process(self, game_variables: dict[str, Any]) -> Tuple[list[str], str, Any]:
        """Calls the components of the resolver class to enable full processing of
        a variable name"""


@dataclass
class ResolveBaseVar(Resolver):
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

    def val_process(self, game_variables: dict[str, Any]) -> Tuple[list[str], str, Any]:
        errors = self.validate_struct()
        return (self.resolve(game_variables)) if not errors else (errors, "", "")


@dataclass
class ResolveHashVar(Resolver):
    call_name: str

    def splitter(self) -> list[str]:
        return self.call_name.split("#")

    def validate_struct(self) -> list[str]:
        CallVarValidator(self.call_name).is_blank()

        errors = []
        if not CallVarValidator(self.call_name).single_hash():
            return [var_error_string("multiple_hash", self.call_name)]

        # If more than one hash (above), then can't correctly split and
        # evaluate the two components of the variable call

        split = self.splitter()
        errors.extend(CallVarValidator(split[0]).is_name_valid())
        if not CallVarValidator(split[1]).hash_is_number():
            errors.append(var_error_string("hash_not_number", self.call_name))

        return errors

    def resolve(
        self, game_variables: dict[str, Any] = {}
    ) -> Tuple[list[str], str, Any]:
        split = self.splitter()

        # Get the value of the variable, then generate the index to slice from the hash
        var = ResolveBaseVar(split[0].replace("]", ""))
        errors, _, value = var.val_process(game_variables)
        split_val = int(split[1]) - 1

        if not errors:
            try:
                # If hash value is invalid, this will return an index error
                out_val = str(value)[split_val]  # Slice variable value using hash val
                return errors, self.call_name, out_val
            except IndexError:
                return [var_error_string("inv_hash", self.call_name)], "", ""
        else:
            return errors, "", ""

    def val_process(self, game_variables: dict[str, Any]) -> Tuple[list[str], str, Any]:
        errors = self.validate_struct()
        return (self.resolve(game_variables)) if not errors else (errors, "", "")


@dataclass
class ResolveBracketVar(Resolver):
    call_name: str

    def splitter(self) -> list[str]:
        return self.call_name.split("[")

    def validate_struct(self) -> list[str]:
        CallVarValidator(self.call_name).is_blank()

        errors = []
        if CallVarValidator(self.call_name).is_first_bracket():
            errors.append(var_error_string("first_alpha", self.call_name))
        if not CallVarValidator(self.call_name).is_equal_bracket():
            errors.append(var_error_string("mismatch_bracket", self.call_name))

        if errors:
            return errors

        for var in self.splitter():  # Iterate over each component of variable
            errors.extend(CallVarValidator(var.replace("#", "")).is_name_valid())
            if "#" in var:
                # Specific validation of hash when included as part of a bracket var
                if not CallVarValidator(var).hash_correct_place():
                    errors.append(var_error_string("hash_place", self.call_name))
                # Then usual validation of a hash variable
                errors.extend(ResolveHashVar(var.replace("]", "")).validate_struct())

        return errors

    def resolve(
        self, game_variables: dict[str, Any] = {}
    ) -> Tuple[list[str], str, Any]:
        final_variable = ""
        bracket_value = ""
        errors: list[str] = []
        full_errors: list[str] = []

        for iteration, part_name in enumerate(reversed(self.splitter())):
            if iteration + 1 == len(self.splitter()):
                # Final component of variable - can't contain a bracket or hash
                # Pulls together remaining constituent parts
                final_variable = f"{part_name}{bracket_value}{final_variable}"
                # Final variable is always a 'base' variable
                var: Resolver = ResolveBaseVar(final_variable.replace("]", ""))
                errors, name, value = var.val_process(game_variables)
                full_errors.extend(errors)
                return full_errors, name, value

            else:
                if full_errors:
                    return full_errors, "", ""

                # Fully enclosed component - goes and fetches the value of that
                # component. If prior component was a bracket value, appends that
                # in first, as it is resolved.
                if part_name.count("]") == 1:
                    final_variable = f"{bracket_value}{final_variable}"
                    bracket_value = ""

                    var = (
                        ResolveHashVar(f"{part_name}".replace("]", ""))
                        if "#" in part_name
                        else ResolveBaseVar(f"{part_name}".replace("]", ""))
                    )
                    errors, name, value = var.val_process(game_variables)
                    full_errors.extend(errors)

                    final_variable = f"_{value}{final_variable}"

                # Is a nested bracket value, to be appended to the next value
                else:
                    var = (
                        ResolveHashVar(f"{part_name}{bracket_value}".replace("]", ""))
                        if "#" in part_name
                        else ResolveBaseVar(
                            f"{part_name}{bracket_value}".replace("]", "")
                        )
                    )
                    errors, name, value = var.val_process(game_variables)

                    bracket_value = f"_{value}"
                    full_errors.extend(errors)

        return full_errors, "", ""

    def val_process(self, game_variables: dict[str, Any]) -> Tuple[list[str], str, Any]:
        return [], "", ""
