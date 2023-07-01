from dataclasses import dataclass, field
from pathlib import Path

from cstest.content.lines.line import Line


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
