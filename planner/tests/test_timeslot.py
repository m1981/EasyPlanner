import pytest
from datetime import datetime, timedelta
from app.models.time_slot import TimeSlot

# Initialize TimeSlot object for testing
start_time = datetime.now()
end_time = start_time + timedelta(hours=1)
timeslot = TimeSlot(start_time, end_time)

def test_get_start_time():
    assert timeslot.get_start_time() == start_time

def test_get_end_time():
    assert timeslot.get_end_time() == end_time

def test_set_start_time():
    new_start_time = datetime.now()
    timeslot.set_start_time(new_start_time)
    assert timeslot.get_start_time() == new_start_time

def test_set_end_time():
    new_end_time = datetime.now() + timedelta(hours=2)
    timeslot.set_end_time(new_end_time)
    assert timeslot.get_end_time() == new_end_time

# Edge case: Setting the end time to be earlier than the start time
def test_set_end_time_before_start_time():
    with pytest.raises(ValueError):
        new_end_time = datetime.now() - timedelta(hours=2)
        timeslot.set_end_time(new_end_time)

# Edge case: Setting the start time to be later than the end time
def test_set_start_time_after_end_time():
    with pytest.raises(ValueError):
        new_start_time = datetime.now() + timedelta(hours=2)
        timeslot.set_start_time(new_start_time)
