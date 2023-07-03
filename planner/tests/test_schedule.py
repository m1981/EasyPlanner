import pytest
from datetime import datetime, timedelta
from app.models.task import Task
from app.models.zone import Zone
from app.models.time_slot import TimeSlot
from app.models.schedule import Schedule

def test_schedule_add_task():
    schedule = Schedule(0, 6)
    task = Task('Task 1', ['Label 1'], '10min')
    slot = TimeSlot(datetime(2022, 1, 1, 10, 0), datetime(2022, 1, 1, 10, 10))

    schedule.add_task(task, slot)
    assert task in schedule.get_tasks()

def test_schedule_remove_task():
    schedule = Schedule(0, 6)
    task = Task('Task 2', ['Label 2'], '30min')
    slot = TimeSlot(datetime(2022, 1, 1, 11, 0), datetime(2022, 1, 1, 11, 30))

    schedule.add_task(task, slot)
    schedule.remove_task(task)
    assert task not in schedule.get_tasks()

def test_schedule_match_labels():
    schedule = Schedule(0, 6)
    task = Task('Task 3', ['Label 3', 'Label 4'], '30min')
    zone = Zone('Label 3', '09:00', '10:00')

    assert schedule.match_labels(task, zone) is True

def test_schedule_match_labels_negative():
    schedule = Schedule(0, 6)
    task = Task('Task 4', ['Label 5', 'Label 6'], '30min')
    zone = Zone('Label 7', '09:00', '10:00')

    assert schedule.match_labels(task, zone) is False

# Here is an edge case where schedule falls into the night hours
def test_schedule_check_night_hours():
    schedule = Schedule(0, 6)
    task_start = datetime(2022, 1, 1, 1, 0)

    assert schedule.check_night_hours(task_start) == datetime(2022, 1, 2, 1, 0)


def test_schedule_task_fits_in_zone():
    schedule = Schedule(0, 6)
    task_end = datetime(2022, 1, 1, 10, 0)
    zone = Zone('Label 8', '09:00', '11:00')

    assert schedule.task_fits_in_zone(task_end, zone) is True

def test_schedule_task_fits_in_zone_negative():
    schedule = Schedule(0, 6)
    task_end = datetime(2022, 1, 1, 12, 0)
    zone = Zone('Label 8', '09:00', '11:00')

    assert schedule.task_fits_in_zone(task_end, zone) is False
