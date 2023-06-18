from dataclasses import dataclass, field
from pathlib import Path

from cstest.cli.util import banner
from cstest.constants import PROJECTS_PATH
from cstest.content.context import Context
from cstest.content.file import File
from cstest.content.variable.variable import DefinedVariable


@dataclass
class Project:
    project_name: str
    project_folder: Path
    test_path: Path
    file_list: list[Path] = field(init=False)
    files: list[File] = field(init=False)
    file_number: int = field(init=False)
    variables: list[DefinedVariable] = field(init=False)
    # context: Context = field(init=False)

    def rep_test_initialise(self) -> None:
        banner("Initialise")
        print(
            f"Project: {self.project_name} has been parsed.\n"
            f"{self.file_number} files have been identified.\n"
            f"Testing will begin. Results will be found in {self.test_path}"
        )

    def scrape_files(self) -> None:
        self.file_list = [file for file in self.project_folder.glob("*.txt")]

    def parse_files(self) -> None:
        self.files = [File(self.project_folder / file) for file in self.file_list]
        for file in self.files:
            pass
            # file.parse_lines()

        self.file_number = len(self.files)

        self.rep_test_initialise()

    def test_project(self) -> None:
        self.scrape_files()
        self.parse_files()
