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


def validate_variable_word(word: str) -> tuple[bool, str]:
    """Checks the variable name passes all required checks"""
    if is_first_alpha(word):
        if inv_symbol(word):
            return True, ""
        else:
            return False, var_error_string("inv_symbol", word)
    else:
        return False, var_error_string("first_alpha", word)


def equal_sq_brackets(variables: list[str]) -> bool:
    """Checks the full variable name has an equal number
    of open and closed square brackets"""
    return (
        True
        if sum("[" in word for word in variables)
        == sum("]" in word for word in variables)
        else False
    )


def validate_variable_name(
    name: str, def_variables: dict[str, DefinedVariable]
) -> bool:
    return True if name in def_variables.keys() else False
