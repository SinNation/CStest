from datetime import datetime
from enum import Enum
from pathlib import Path

TIMESTAMP = datetime.now().strftime("%Y%M%d-%H%M%S")

CS_PATH = Path.cwd()
DATA_PATH = CS_PATH / "data"
PROJECTS_PATH = CS_PATH.parents[0]

COMMANDS = {
    "*CREATE": "creation",
    "*TEMP": "creation",
    "*SET": "access",
    "*SELECTABLE_IF": "access_prose",
    "*IF": "access",
    "*ELSE": "access",
    "*ELSEIF": "access",
    "*INPUT_TEXT": "access",
    "*INPUT_NUMBER": "access",
}


COMMON_NON_VARIABLE_WORDS = [
    r"\bAND\b",
    r"\bOR\b",
    r"\bTRUE\b",
    r"\bFALSE\b",
    r"\bNOT\b",
]

KEYWORDS: dict[str, list[str]] = {
    "common": [
        "ROUND(",
        "MODULO",
        "LENGTH(",
        "(",
        ")",
        "+",
        "=",
        "<",
        ">",
        "-",
        "&",
        "!",
        "%",
        "*IF",
        "*",
        "[B]",
        "[I]",
        "[/B]",
        "[/I]",
        "/",
        "$",
        "@",
        ":",
        ".",
        ",",
        ";",
        "£",
    ],
    "code": [
        "{",
        "}",
        "*SET",
        "*ELSEIF",
        "*SELECTABLE_IF",
        "*ALLOW_REUSE",
        "*DISABLE_REUSE",
        "*HIDE_REUSE",
        "*ELSE",
        "*INPUT_TEXT",
        "*INPUT_NUMBER",
        "'",
        "NOT(",
    ],
    "prose": [
        '"',
        "*page_break",
        "*line_break",
    ],
}
