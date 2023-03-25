import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from cstest.constants import COMMON_NON_VARIABLE_WORDS, KEYWORDS, Commands
from cstest.content.effect import Effect
from cstest.content.variable import Variable


def sq_bracket_handler(word: str) -> str:
    bracketed_word = word.split("[")[1].replace("]", "")
    return bracketed_word.split("#")[0] if "#" in bracketed_word else bracketed_word


def remove_common_non_variable_words(string: str) -> str:
    for word in COMMON_NON_VARIABLE_WORDS:
        string = re.sub(word, "", string)
    return string


def remove_keywords(string: str, keyword_type: str) -> str:
    keywords = KEYWORDS["common"] + KEYWORDS[keyword_type]
    for keyword in keywords:
        new_line = string.replace(keyword, " ")
    return new_line


@dataclass
class Line:
    row_number: int
    orig_line: str
    errors: dict[str, str] = {}
    warnings: dict[str, str] = {}
    indent: int = 0
    clean_line: str = ""
    command_type: Commands = field(init=False)
    called_variables: list[str] = []
    called_bracket_variables: list[str] = []
    created_variable: Optional[Variable] = None
    # condition_map: Optional[Condition] = None
    effect: Optional[Effect] = None
    # next line

    def calc_indent(self) -> None:
        """Calculate length of whitespace indent for the line"""
        self.indent = len(self.orig_line) - len(self.orig_line.lstrip(" "))

    def create_clean_line(self) -> None:
        """Replace new line characters, remove indent and uppercase"""
        self.clean_line = self.clean_line.replace("\n", "").lstrip().upper()

    def calc_command_type(self) -> None:
        """Calculate the type of line (prose, creation, access, comment)
        and store the command type if it is one."""
        command = self.clean_line.split(" ")[0].replace("*", "")

        if self.clean_line.startswith("*"):
            try:
                self.command_type = Commands[command]
            except Exception:
                self.command_type = Commands["INVALID"]
                self.errors[
                    "command_type"
                ] = f"Command: {command} is not a valid Choicescript command"

        else:
            try:
                Commands[command]
                self.warnings["command_type"] = (
                    f"Starting word {command} might be missing an '*' to make it"
                    "a Choicescript command"
                )
            except Exception:
                self.command_type = Commands["PROSE"]

    def find_created_variables(self, string: str) -> None:
        parts = string.split()
        try:
            name = parts[1]
        except Exception:
            self.errors["created_variable"] = "Create command has no variable name"
            return
        try:
            value = parts[2]
        except Exception:
            self.errors[
                "created_variable"
            ] = f"Created variable {name} has no initial value"
            return

        var_type = "str" if isinstance(value, str) else "number"
        self.created_variable = Variable(name, var_type, value)

    def find_cmd_call_variables(self, string: str) -> None:
        """Iterates over every word in the command. If it is a literal string
        or a number, then it is rejected. Anything else should be a variable
        of some kind"""

        string = remove_keywords(string, "command")
        string = remove_common_non_variable_words(string).split()  # type: ignore

        multi_word_string = False

        for word in string:
            if multi_word_string:
                if word.endswith(("'", '"')):
                    multi_word_string = False
                    continue
                continue
            if word.startswith(("'", '"')) and not word.endswith(("'", '"')):
                multi_word_string = True
                continue
            if word.isnumeric():
                continue
            if word.startswith(("'", '"')) and word.endswith(("'", '"')):
                continue
            if "#" in word and "[" not in word:
                self.called_variables.extend(word)
                continue
            if "[" in word:
                self.called_bracket_variables.extend(word)
                self.called_variables.extend(sq_bracket_handler(word))
                continue
            self.called_variables.extend(word)

    def find_prose_call_variables(self, string: str) -> None:
        """Iterates over every word in a prose string."""

        string = remove_keywords(string, "prose").split()  # type: ignore
        string = remove_common_non_variable_words(string)

        if "{" in string:
            for word in string:
                if "{" in word:
                    word = word.split("}")[0].split("{")[1]
                    if "[" in word:
                        self.called_bracket_variables.extend(word)
                        self.called_variables.extend(sq_bracket_handler(word))
                    self.called_variables.extend(word)

    def find_dual_call_variables(self, string: str) -> None:
        cmd_string = string.split("#")[0]
        prose_string = string.replace(cmd_string, "")
        self.find_cmd_call_variables(cmd_string)
        self.find_prose_call_variables(prose_string)

    # def evaluate_condition(self) -> None:
    #     if self.command_type.value.conditional:
    #         self.condition = create_condition(
    #             self.clean_line, self.command_type.value.name
    #         )

    def process_line(self) -> None:
        line_process_dispatcher: dict[str, Callable[[str], None]] = {
            "creation": self.find_created_variables,
            "access": self.find_cmd_call_variables,
            "prose": self.find_prose_call_variables,
            "access_prose": self.find_dual_call_variables,
        }

        self.calc_indent()
        self.create_clean_line()
        self.calc_command_type()
        line_process_dispatcher[self.command_type.value.variable_handle_type](
            self.clean_line
        )
        # self.evaluate_condition()
        # self.calc_effect()


@dataclass
class File:
    file_path: Path
    code: dict[int, Line] = field(init=False)

    def parse_code(self) -> None:
        self.code = {}
        with open(self.file_path, encoding="utf-8") as cs_file:
            code = cs_file.readlines()

        for row_number, code_line in enumerate(code):
            if str.isspace(code_line) or not code_line:
                continue
            else:
                self.code[row_number] = Line(row_number, code_line)
                self.code[row_number].process_line()
