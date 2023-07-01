from dataclasses import dataclass, field
from pathlib import Path

from cstest.content.files.file import File


@dataclass
class Project:
    project_name: str
    project_folder: Path
    test_path: Path
    ignored_files: list[str]
    file_list: list[Path] = field(init=False)
    files: list[File] = field(init=False)
    file_number: int = field(init=False)

    def find_files(self) -> None:
        self.file_list = [
            file
            for file in self.project_folder.glob("*.jpg")
            if not any(ignored in str(file) for ignored in self.ignored_files)
        ]

        self.file_number = len(self.files)

    def parse_files(self) -> None:
        self.files = [File(self.project_folder / file) for file in self.file_list]
        for file in self.files:
            file.parse_code()

    def test_project(self) -> None:
        self.find_files()
        self.parse_files()
