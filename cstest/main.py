from cstest.cli.util import welcome
from cstest.content.project import setup_project
from cstest.process.orchestrate import test_project


def run_cstest() -> None:
    welcome()

    project = setup_project()

    test_project(project)
