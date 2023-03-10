from dataclasses import dataclass, field
from pathlib import Path

from cstest.cli.util import banner
from cstest.constants import PROJECTS_PATH


@dataclass
class Project:
    folder_path: Path
    file_list: list[Path] = field(init=False)

    def scrape_files(self) -> None:
        self.file_list = [file for file in self.folder_path.glob("*.txt")]


def setup_project() -> Project:
    while True:
        banner("")
        folder_name = input(
            "What is the folder name of the project you would like to test?"
        )
        folder_path = PROJECTS_PATH / folder_name

        if folder_path.exists():
            break
        else:
            print(
                f"The folder: {folder_name} does not exist in directory:"
                f" {PROJECTS_PATH}."
            )

    return Project(folder_path)
