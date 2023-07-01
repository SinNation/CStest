from cstest.config.core import Config
from cstest.project.project import Project


def run_cstest() -> None:
    config = Config()
    config.config_test()

    project = Project(
        config.project_name, config.project_path, config.test_path, config.ignored_files
    )
    project.test_project()


if __name__ == "__main__":
    run_cstest()
