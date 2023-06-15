from dataclasses import dataclass, field
from typing import Any

from cstest.content.errors.error import var_error_string
from cstest.content.variable.constants import INVALID_VAR_SYMBOLS
from cstest.content.variable.exceptions import NoVariableNameValue


@dataclass
class CallVarValidator:
    """Variable name structure validator class for called variables."""

    name: str
    game_variables: list[str] = field(default_factory=list)

    def is_blank(self) -> None:
        """Raises exception if the passed variable name is blank.
        This is a code error if it occurs"""
        if self.name == "" or str(self.name).isspace():
            raise NoVariableNameValue(
                "Error in CStest: Identified variable name is blank"
            )

    def is_first_alpha(self) -> bool:
        """Checks the variable name begins with an alpha character"""
        return True if str(self.name)[0].isalpha() else False

    def inv_symbol(self) -> bool:
        """Checks the variable name doesn't contain an invalid symbol"""
        return (
            True if [sym for sym in INVALID_VAR_SYMBOLS if sym in self.name] else False
        )

    def is_name_valid(self) -> list[str]:
        """Checks the variable name passes all required checks"""
        errors: list = []
        if not self.is_first_alpha():
            errors.append(var_error_string("first_alpha", self.name))
        if self.inv_symbol():
            errors.append(var_error_string("inv_symbol", self.name))

        return errors

    def single_hash(self) -> bool:
        """Checks there is only a"""
        return True if self.name.count("#") == 1 else False

    def hash_is_number(self) -> bool:
        return True if str(self.name).isnumeric() else False

    def is_first_bracket(self) -> bool:
        """Checks if the first character of a variable name is a square bracket"""
        return True if self.name[0] == "[" else False

    def is_equal_bracket(self) -> bool:
        """Checks the full variable name has an  equal number
        of open and closed square brackets"""
        return True if self.name.count("[") == self.name.count("]") else False

    def is_defined(self) -> bool:
        """Checks that the called variable name is defined in the game"""
        return True if self.name in self.game_variables else False
