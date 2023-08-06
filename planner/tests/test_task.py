# task_test.py

import pytest
from app.models.task import Task
from datetime import datetime

def test_task_creation():
    title = "Sample Task"
    label = "Sample Label"
    duration = 30
    scheduled_date = datetime.today()
    scheduled_start = datetime.today()

    task = Task(title=title, 
                label=label, 
                duration=duration, 
                scheduled_date=scheduled_date, 
                scheduled_start=scheduled_start)

    assert task.title == title
    assert task.label == label
    assert task.duration == duration
    assert task.scheduled_date == scheduled_date
    assert task.scheduled_start == scheduled_start

def test_task_creation_with_no_dates():
    title = "Sample Task"
    label = "Sample Label"
    duration = 30

    task = Task(title=title, 
                label=label, 
                duration=duration)

    assert task.title == title
    assert task.label == label
    assert task.duration == duration
    assert task.scheduled_date is None
    assert task.scheduled_start is None

def test_task_title_must_not_be_empty():
    title = ""
    label = "Sample Label"
    duration = 30
    
    with pytest.raises(ValueError):
        task = Task(title=title, 
                    label=label, 
                    duration=duration)
