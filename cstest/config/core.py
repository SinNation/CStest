from dataclasses import dataclass, field
from pathlib import Path

from cstest.cli.util import banner
from cstest.constants import PROJECTS_PATH, DATA_PATH, TIMESTAMP


@dataclass
class Config:
    project_name: str = field(init=False)
    project_path: Path = field(init=False)
    test_path: Path = field(init=False)

    def set_folder_path(self) -> None:
        while True:
            banner("")
            folder_name = input(
                "What is the folder name of the project you would like to test?"
            )
            self.project_name = folder_name
            self.project_path = PROJECTS_PATH / folder_name

            if self.project_path.exists():
                break
            else:
                print(
                    f"The folder: {folder_name} does not exist in directory:"
                    f" {PROJECTS_PATH}."
                )

    def create_test_folder(self) -> None:
        self.test_path = DATA_PATH / self.project_name / str(TIMESTAMP)
        Path.mkdir(self.test_path, parents=True)

    def config_test(self) -> None:
        self.set_folder_path()
        self.create_test_folder()
