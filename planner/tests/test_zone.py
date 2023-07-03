import pytest
from app.models.zone import Zone

# Test creating a Zone object
def test_create_zone():
    zone = Zone("Work", "9:00", "17:00")
    assert zone.get_label() == "Work"
    assert zone.get_start_time() == 9 * 60  # Returns the time in minutes
    assert zone.get_end_time() == 17 * 60


# Test setting and getting label
def test_label_setter_and_getter():
    zone = Zone(None, "9:00", "17:00")
    zone.set_label("Study")
    assert zone.get_label() == "Study"

def test_start_time_setter_and_getter():
    with pytest.raises(TypeError):
        zone = Zone("Work", None, "17:00")  # None as start time

def test_end_time_setter_and_getter():
    with pytest.raises(TypeError):
        zone = Zone("Work", "9:00", None) # None as end time

# Test for edge case: start time later than end time
def test_incorrect_start_end_time():
    with pytest.raises(ValueError):
        Zone("Work", "17:00", "9:00")

def test_incorrect_time_format():
    with pytest.raises(TypeError): 
        zone = Zone("Work", "9am", "5pm")  # Will raise TypeError, not ValueError
