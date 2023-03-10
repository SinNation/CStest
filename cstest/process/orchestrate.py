from cstest.content.project import Project


def test_project(project: Project) -> None:
    project.scrape_files()
