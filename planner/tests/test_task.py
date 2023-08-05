import pytest
from task import Task


def test_initialization():
  title = "a new task"
  label = "ForMyself"
  duration = 30
  task = Task(title, label, duration)
  assert task.title == title
  assert task.label == label
  assert task.duration == duration
  assert task.scheduled_date is None
  assert task.scheduled_start is None
