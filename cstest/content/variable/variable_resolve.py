from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Tuple

from cstest.content.errors.error import var_error_string
from cstest.content.variable import validators as v


class Resolver(ABC):
    called_name: str

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


@dataclass
class ResolveBaseVariable(Resolver):
    called_name: str

    def splitter(self) -> list[str]:
        return [self.called_name]

    def validate_struct(self) -> list[str]:
        v.empty_variable_name(self.called_name)
        return v.validate_variable_name(self.called_name)

    def resolve(
        self, game_variables: dict[str, Any] = {}
    ) -> Tuple[list[str], str, Any]:
        return (
            ([], self.called_name, game_variables[self.called_name])
            if v.is_defined_variable(self.called_name, list(game_variables.keys()))
            else ([v.var_error_string("inv_var", self.called_name)], "", "")
        )


def validate_base_variable(
    name: str, game_variables: dict[str, Any]
) -> Tuple[list[str], str, Any]:
    var = ResolveBaseVariable(name.replace("]", ""))
    errors = var.validate_struct()
    if not errors:
        return var.resolve(game_variables)
    else:
        return errors, "", ""


@dataclass
class ResolveBracketVariable(Resolver):
    called_name: str

    def splitter(self) -> list[str]:
        return self.called_name.split("[")

    def validate_struct(self) -> list[str]:
        v.empty_variable_name(self.called_name)

        errors = []
        if v.first_char_sq_bracket(self.called_name):
            errors.append(var_error_string("first_alpha", self.called_name))
        elif v.equal_sq_brackets(self.called_name):
            for variable in self.splitter():
                errors.extend(v.validate_variable_name(variable))
        else:
            errors.append(var_error_string("mismatch_bracket", self.called_name))

        return errors

    def resolve(
        self, game_variables: dict[str, Any] = {}
    ) -> Tuple[list[str], str, Any]:
        final_variable = ""
        bracket_value = ""
        errors: list[str] = []
        length = len(self.splitter())

        for iteration, part_name in enumerate(reversed(self.splitter())):
            if iteration + 1 == length:
                final_variable = f"{part_name}{bracket_value}{final_variable}"
                errors, name, value = validate_base_variable(
                    final_variable, game_variables
                )
                return errors, name, value

            else:
                if not errors:
                    if part_name.count("]") == 1:
                        if bracket_value != "":
                            final_variable = f"{bracket_value}{final_variable}"
                            bracket_value = ""
                        errors, name, value = validate_base_variable(
                            f"{part_name}", game_variables
                        )
                        final_variable = f"_{value}{final_variable}"
                    else:
                        errors, name, value = validate_base_variable(
                            f"{part_name}{bracket_value}",
                            game_variables,
                        )
                        bracket_value = f"_{value}"

        return errors, "", ""


@dataclass
class ResolveHashVariable(Resolver):
    called_name: str

    def splitter(self) -> list[str]:
        return self.called_name.split("#")

    def validate_struct(self) -> list[str]:
        v.empty_variable_name(self.called_name)

        errors = []
        if not v.check_count_hashes(self.called_name):
            return [var_error_string("multiple_hash", self.called_name)]

        split = self.splitter()
        errors.extend(v.validate_variable_name(split[0]))
        if not v.check_hash_is_number(split[1]):
            errors.append(var_error_string("hash_not_number", self.called_name))

        return errors

    def resolve(
        self, game_variables: dict[str, Any] = {}
    ) -> Tuple[list[str], str, Any]:
        split = self.splitter()

        errors, _, value = validate_base_variable(split[0], game_variables)
        split_val = int(split[1]) - 1
        return (
            (errors, self.called_name, str(value)[split_val])
            if not errors
            else (errors, "", "")
        )


# @dataclass
# class ResolveBracketHashVariable(Resolver):
#     called_name: str
#     error: Optional[str] = ""
#     valid_struct: bool = field(init=False)
#     valid_name: bool = field(init=False)
#     name: str = field(init=False)

#     def splitter(self) -> list[str]:
#         split_variable = self.called_name.split("[")
#         split_suffix = split_variable[1].split("#")
#         return [split_variable[0], split_suffix[0], split_suffix[1].replace("]", "")]

#     def validator(
#         self, game_variables: list[str]
#     ) -> tuple[bool, str]:
#         if len(self.called_name) - 3 == len(
#             self.called_name.replace("[", "").replace("]", "").replace("#", "")
#         ):
#             try:
#                 split_variable = self.splitter()
#             except Exception as e:
#                 return False, f"{error_string('split', self.called_name)}. {e}"

#             if split_variable[1] in game_variables.keys().keys():
#                 try:
#                     int(split_variable[2])
#                     suffix_val = str(game_variables[split_variable[1]])
#                     suffix = suffix_val[int(split_variable[2])]

#                     if f"{split_variable[0]}_{suffix}" in
# game_variables.keys().keys():
#                         return True, ""
#                     else:
#                         return False, error_string("inv_var", self.called_name)

#                 except Exception:
#                     return False, error_string("invalid_hash", self.called_name)
#             else:
#                 return False, error_string("inv_var", self.called_name)
#         else:
#             return False, error_string("multiple_bracket_hash", self.called_name)

#     def resolve(self, _: Optional[list[str]] = []) -> None:
#         split_variable = self.splitter()
#         suffix_val = game_variables[split_variable[1]]
#         suffix = suffix_val[split_variable[2]]
#         self.name = f"{split_variable[0]}_{suffix}"
