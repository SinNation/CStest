from dataclasses import dataclass, field
from pathlib import Path

from cstest.constants import DATA_PATH, PROJECTS_PATH, TIMESTAMP


@dataclass
class Config:
    project_name: str = field(init=False)
    project_path: Path = field(init=False)
    test_path: Path = field(init=False)
    ignored_files: list[str] = field(default_factory=list)

    def set_folder_path(self) -> None:
        while True:
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
        self.ignored_files = ["choicescript_stats"]
