from dataclasses import dataclass, field
from pathlib import Path

from cstest.cli.util import banner
from cstest.content.file import File
from cstest.content.variable import Variable
from cstest.content.context import Context
from cstest.constants import PROJECTS_PATH


@dataclass
class Project:
    project_name: str
    project_folder: Path
    test_path: Path
    file_list: list[Path] = field(init=False)
    files: list[File] = field(init=False)
    variables: list[Variable] = field(init=False)
    context: Context = field(init=False)

    def scrape_files(self) -> None:
        self.file_list = [file for file in self.project_folder.glob("*.txt")]

    def test_project(self) -> None:
        self.scrape_files()
