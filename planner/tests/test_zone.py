import pytest
import datetime as dt
from modules.day import Zone, Task, Day



def test_empty_zone_raises_error():
    with pytest.raises(AssertionError):
        Zone("", "", ["Work"])

def test_task_without_labels_does_not_fit():
    zone = Zone('10:00', '12:00', ['Work'])
    task = Task('test task', [], '10min')
    assert zone.fits(task) == False
    assert zone.add(task) == False

def test_task_without_matching_labels_does_not_fit():
    zone = Zone('10:00', '12:00', ['School'])
    task = Task('test task', ['Work'], '10min')
    assert zone.fits(task) == False
    assert zone.add(task) == False

def test_task_with_matching_labels_fits():
    zone = Zone('10:00', '12:00', ['Work', 'School'])
    task = Task('test task', ['Work'], '10min')
    assert zone.fits(task) == True

def test_task_with_matching_labels_is_added():
    zone = Zone('10:00', '12:00', ['Work', 'School'])
    task = Task('test task', ['Work'], '10min')
    assert zone.add(task) == True
    assert zone.tasks == [task]
    assert zone.current_time == (dt.datetime.combine(dt.date.today(), dt.datetime.strptime('10:10', '%H:%M').time())).time()

def test_zone_with_inadequate_time_left():
    zone = Zone('10:00', '10:15', ['Work'])
    task = Task('test task', ['Work'], '20min')
    assert zone.fits(task) == False
    assert zone.add(task) == False
    assert zone.tasks == []
    assert zone.current_time == dt.datetime.strptime('10:00', '%H:%M').time()



def test_task_does_not_fit_due_to_non_matching_labels():
    zone = Zone('10:00', '12:00', 'Work')
    task = Task('Rest task', ['Rest'], '45min')
    assert zone.fits(task) == False

def test_task_fits_due_to_matching_labels():
    zone = Zone('10:00', '12:00', 'Work')
    task = Task('Work task', ['Work'], '45min')
    assert zone.fits(task) == True

def test_multiple_matching_labels_are_accepted():
    zone = Zone('10:00', '12:00', ['Work', 'Exercise'])
    task = Task('Exercise task', ['Exercise'], '45min')
    assert zone.fits(task) == True

def test_multiple_non_matching_labels_are_rejected():
    zone = Zone('10:00', '12:00', ['Work', 'Exercise'])
    task = Task('Rest task', ['Rest'], '45min')
    assert zone.fits(task) == False

def test_matching_and_non_matching_labels_are_accepted():
    zone = Zone('10:00', '12:00', ['Work', 'Exercise'])
    task = Task('Work task', ['Work', 'Rest'], '45min')
    assert zone.fits(task) == True
