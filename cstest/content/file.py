import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from cstest.constants import COMMANDS, COMMON_NON_VARIABLE_WORDS, KEYWORDS
from cstest.content.variable import Variable


@dataclass
class Line:
    orig_line: str
    clean_line: str = field(init=False)
    indent: int = field(init=False)
    line_type: str = field(init=False)
    command: Optional[str] = field(init=False)
    called_variables: list[str] = field(init=False)
    called_bracket_variables: list[str] = field(init=False)
    created_variable: Optional[Variable] = field(init=False)

    def calc_indent(self) -> None:
        self.indent = len(self.orig_line) - len(self.orig_line.lstrip(" "))

    def create_clean_line(self) -> None:
        self.clean_line = self.clean_line.replace("\n", "").lstrip().upper()

        for word in COMMON_NON_VARIABLE_WORDS:
            self.clean_line = re.sub(word, "", self.clean_line)

    def calc_line_type(self) -> None:
        if self.clean_line.startswith("*"):
            self.command = self.clean_line.split(" ")[0]
            self.line_type = COMMANDS[self.clean_line.split(" ")[0]]
        else:
            self.line_type = "prose"

    def remove_keywords(self, string: str, keyword_type: str) -> str:
        keywords = KEYWORDS["common"] + KEYWORDS[keyword_type]
        for keyword in keywords:
            new_line = string.replace(keyword, " ")
        return new_line

    def sq_bracket_handler(self, word: str) -> str:
        bracketed_word = word.split("[")[1].replace("]", "")
        return bracketed_word.split("#")[0] if "#" in bracketed_word else bracketed_word

    def find_cmd_call_variables(self, string: str) -> None:
        """Iterates over every word in the command. If it is a literal string
        or a number, then it is rejected. Anything else should be a variable
        of some kind"""

        string = self.remove_keywords(string, "command").split()  # type: ignore

        multi_word_string = False

        for word in string:
            if multi_word_string:
                if word.endswith(("'", '"')):
                    multi_word_string = False
                    continue
                continue
            if word.startswith(("'", '"')):
                multi_word_string = True
                continue
            if word.isnumeric():
                continue
            if word.startswith(("'", '"')) and word.endswith(("'", '"')):
                continue
            if "#" in word and "[" not in word:
                self.called_variables.extend(word)
            if "[" in word:
                self.called_bracket_variables.extend(word)
                self.called_variables.extend(self.sq_bracket_handler(word))

    def find_prose_call_variables(self, string: str) -> None:
        """Iterates over every word in a prose string."""

        string = self.remove_keywords(string, "prose").split()  # type: ignore

        if "{" in string:
            for word in string:
                if "{" in word:
                    word = word.split("}")[0].split("{")[1]
                    if "[" in word:
                        self.called_bracket_variables.extend(word)
                        self.called_variables.extend(self.sq_bracket_handler(word))

    def find_created_variables(self, string: str) -> None:
        self.created_variable = Variable(string.split(" ")[1].split(" ")[0])

    def find_dual_call_variables(self, string: str) -> None:
        cmd_string = string.split("#")[0]
        prose_string = string.replace(cmd_string, "")
        self.find_cmd_call_variables(cmd_string)
        self.find_prose_call_variables(prose_string)

    def transform_line(self) -> None:
        self.calc_indent()
        self.create_clean_line()
        self.calc_line_type()

    def extract_variables(self) -> None:
        line_process_dispatcher: dict[str, Callable[[str], None]] = {
            "creation": self.find_cmd_call_variables,
            "access": self.find_prose_call_variables,
            "prose": self.find_created_variables,
            "access_prose": self.find_dual_call_variables,
        }

        line_process_dispatcher[self.line_type](self.clean_line)


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
                self.code[row_number] = Line(code_line)
                self.code[row_number].transform_line()
                self.code[row_number].extract_variables()
