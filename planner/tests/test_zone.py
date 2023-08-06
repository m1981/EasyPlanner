# zone_test.py
import pytest
from app.models.zone import Zone, Task
from datetime import datetime


class TestZone:

  def setup_method(self):
    self.zone = Zone("10:00", "13:00", "label1")
    self.task1 = Task("task1", "label1", 60)
    self.task2 = Task("task1", "label1", 200)

  def test_add_task(self):
    # Test that a task that fits the zone can be added
    result = self.zone.add(self.task1)
    assert result
    assert len(self.zone.tasks) == 1

    # Test that a task that doesn't fit the zone can't be added
    result = self.zone.add(self.task2)
    assert not result
    assert len(self.zone.tasks) == 1

  def test_fits(self):
    # Test that a task that fits the zone is recognized
    result = self.zone.fits(self.task1)
    assert result

    # Test that a task that doesn't fit the zone isn't recognized
    result = self.zone.fits(self.task2)
    assert not result
