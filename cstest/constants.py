from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path

TIMESTAMP = datetime.now().strftime("%Y%M%d-%H%M%S")

CS_PATH = Path.cwd()
DATA_PATH = CS_PATH / "data"
PROJECTS_PATH = CS_PATH.parents[0]

INVALID_LINE_FILE = "invalid_line.csv"


@dataclass
class CommandType:
    variable_handle_type: str
    conditional: bool
    effect: bool
    name: str


class Commands(Enum):
    PROSE = CommandType("prose", False, False, "*PROSE")
    CREATE = CommandType("creation", False, True, "*CREATE")
    TEMP = CommandType("creation", False, True, "*TEMP")
    SET = CommandType("access", False, True, "*SET")
    SELECTABLE_IF = CommandType("access_prose", True, False, "*SELECTABLE_IF")
    IF = CommandType("access", True, False, "*IF")
    ELSE = CommandType("access", False, False, "*ELSE")
    ELSEIF = CommandType("access", True, False, "*ELSEIF")
    INPUT_TEXT = CommandType("access", False, True, "*INPUT_TEXT")
    INPUT_NUMBER = CommandType("access", False, True, "*INPUT_NUMBER")
    COMMENT = CommandType("comment", False, False, "*COMMENT")
    INVALID = CommandType("invalid", False, False, "*INVALID")


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


CONDITION_SYMBOLS = ["(", ")", ">=", "<=", ">", "<", "=", "NOT"]
