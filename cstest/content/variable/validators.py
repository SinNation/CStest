from cstest.content.errors.error import var_error_string
from cstest.content.variable.def_var import DefinedVariable
from cstest.content.variable.exceptions import NoVariableNameValue

INVALID_VAR_SYMBOLS = [
    "'",
    '"',
    "!",
    "£",
    "$",
    "^",
    "&",
    "*",
    "(",
    ")",
    "-",
    "=",
    "+",
    "{",
    "}",
    ":",
    ";",
    "@",
    "~",
    "#",
    "\\",
    "|",
    ",",
    "<",
    ".",
    ">",
    "/",
    "?",
    " ",
]


def empty_variable_name(name: str) -> None:
    if name == "" or str(name).isspace():
        raise NoVariableNameValue("Error in CStest: Identified variable name is blank")


def is_first_alpha(name: str) -> bool:
    """Checks the variable name begins with an alpha character"""
    return True if str(name)[0].isalpha() else False


def inv_symbol(name: str) -> bool:
    """Checks the variable name doesn't contain an invalid symbol"""
    return True if not [sym for sym in INVALID_VAR_SYMBOLS if sym in name] else False


def validate_variable_name(name: str) -> list[str]:
    """Checks the variable name passes all required checks"""
    errors: list = []
    if not is_first_alpha(name):
        errors.append(var_error_string("first_alpha", name))
    if not inv_symbol(name):
        errors.append(var_error_string("inv_symbol", name))

    return errors


def first_char_sq_bracket(name: str) -> bool:
    return True if name[0] == "[" else False


def equal_sq_brackets(name: str) -> bool:
    """Checks the full variable name has an  equal number
    of open and closed square brackets"""
    return True if name.count("[") == name.count("]") else False


def is_defined_variable(name: str, def_variables: list[str]) -> bool:
    """Checks that the called variable name is defined in the game"""
    return True if name in def_variables else False
