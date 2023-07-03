import pytest
from app.models.task import Task


class TestTask:

  @pytest.fixture
  def task(self):
    """Returns a Task instance with predefined properties."""
    return Task("Test Task", ["Label1", "Label2"], "30min")

  def test_content(self, task):
    """Tests content getter and setter."""
    assert task.get_content() == "Test Task"
    task.set_content("New Task")
    assert task.get_content() == "New Task"

  def test_labels(self, task):
    """Tests labels getter and setter."""
    assert task.get_labels() == ["Label1", "Label2"]
    task.set_labels(["Label3"])
    assert task.get_labels() == ["Label3"]

  def test_duration(self, task):
    """Tests duration getter and setter."""
    assert task.get_duration() == "30min"
    task.set_duration("60min")
    assert task.get_duration() == "60min"
