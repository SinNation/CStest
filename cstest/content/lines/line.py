import re
from dataclasses import dataclass, field
from typing import Callable

from cstest.constants import Command
from cstest.content.effects.effect import Effect
from cstest.content.errors.error import error_string
from cstest.content.lines import handler as h
from cstest.content.processors.processor import Processor


@dataclass
class Line:
    row_number: int
    orig_line: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    indent: int = 0
    clean_line: str = ""
    next_line: int = field(init=False)
    command: Command = field(init=False)
    effect: Effect = field(init=False)
    processor: Processor = field(init=False)

    def calc_indent(self) -> None:
        """Calculate length of whitespace indent for the line"""
        self.indent = len(self.orig_line) - len(self.orig_line.lstrip(" "))

    def create_clean_line(self) -> None:
        """Replace new line characters, remove indent and uppercase"""
        self.clean_line = self.clean_line.replace("\n", "").lstrip().upper()

    def set_command(self) -> None:
        """Calculate the type of line (prose, creation, access, comment)
        and store the command type if it is one."""
        command = self.clean_line.split(" ")[0].replace("*", "")

        if self.clean_line.startswith("*"):
            try:
                self.command = Command[command]
            except Exception:
                self.command = Command["INVALID"]
                self.errors.append(error_string("invalid_command", "Command", command))
        else:
            try:  # If it's a valid command missing an *
                Command[command]
                self.warnings.append(error_string("missing_*", "Command", command))
            except Exception:
                self.command = Command["PROSE"]

    def identify_effect_processor(self) -> None:
        pass

    def process_line(self) -> None:
        self.calc_indent()
        self.create_clean_line()
        self.set_command()
        self.identify_effect_processor()
        self.effect.define_effect()
