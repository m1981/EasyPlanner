import pytest
from unittest.mock import MagicMock
from app.models.todoist_api_wrapper import TodoistAPIWrapper

@pytest.fixture
def todoist_api():
    api_key = "test_api_key"
    return TodoistAPIWrapper(api_key)

def test_get_projects(todoist_api):
    # Arrange
    mock_projects = [
        {
            "id": "220474322",
            "name": "Inbox",
        },
        {
            "id": "220474323",
            "name": "Work",
        },
    ]
    todoist_api.api.get_projects = MagicMock(return_value=mock_projects)

    # Act
    projects = todoist_api.get_projects()

    # Assert
    assert len(projects) == 2
    assert projects[0]["name"] == "Inbox"
    assert projects[1]["name"] == "Work"

from collections import namedtuple

def test_get_tasks_by_project_id(todoist_api):
    # Arrange
    Task = namedtuple("Task", ["id", "content", "project_id"])
    mock_tasks = [
        Task(id="2995104339", content="Buy Milk", project_id="220474322"),
        Task(id="2995104340", content="Finish Report", project_id="220474323"),
    ]
    todoist_api.api.get_tasks = MagicMock(return_value=mock_tasks)

    # Act
    project_id = "220474322"
    tasks = todoist_api.get_tasks_by_project_id(project_id)

    # Assert
    assert len(tasks) == 1
    assert tasks[0].content == "Buy Milk"
    assert tasks[0].project_id == project_id

