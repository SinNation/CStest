from cstest.cli.util import welcome
from cstest.content.project import Project
from cstest.config.core import Config


def run_cstest() -> None:
    welcome()

    config = Config()
    config.config_test()

    project = Project(config.project_name, config.project_path, config.test_path)
    project.test_project()

    print(project)
