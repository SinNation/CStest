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


def is_first_alpha(word: str) -> bool:
    """Checks the variable name begins with an alpha character"""
    if word == "" or str(word).isspace():
        raise NoVariableNameValue("Error in CStest: Identified variable name is blank")
    return True if str(word)[0].isalpha() else False


def inv_symbol(word: str) -> bool:
    """Checks the variable name doesn't contain an invalid symbol"""
    return True if not [sym for sym in INVALID_VAR_SYMBOLS if sym in word] else False


def validate_variable_word(word: str) -> tuple[bool, list[str]]:
    """Checks the variable name passes all required checks"""
    errors: list = []
    if not is_first_alpha(word):
        errors.append(var_error_string("first_alpha", word))
    if not inv_symbol(word):
        errors.append(var_error_string("inv_symbol", word))

    return (True, errors) if not errors else (False, errors)


def equal_sq_brackets(int_name: str) -> bool:
    """Checks the full variable name has an equal number
    of open and closed square brackets"""
    return True if int_name.count("[") == int_name.count("]") else False


def is_defined_variable(name: str, def_variables: list[str]) -> bool:
    """Checks that the called variable name is defined in the game"""
    return True if name in def_variables else False
