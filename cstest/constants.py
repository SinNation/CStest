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
    type: str
    name: str


class Commands(Enum):
    PROSE = CommandType("prose", "PROSE")
    CREATE = CommandType("creation", "CREATE")
    TEMP = CommandType("creation", "TEMP")
    SET = CommandType("access", "SET")
    SELECTABLE_IF = CommandType("access_prose", "SELECTABLE_IF")
    IF = CommandType("access", "IF")
    ELSE = CommandType("access", "ELSE")
    ELSEIF = CommandType("access", "ELSEIF")
    INPUT_TEXT = CommandType("access", "INPUT_TEXT")
    INPUT_NUMBER = CommandType("access", "INPUT_NUMBER")
    COMMENT = CommandType("comment", "COMMENT")
    INVALID = CommandType("invalid", "INVALID")


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
