# test_day.py
import pytest
from app.models.task import Task
from app.models.zone import Zone
from app.models.day import Day
from datetime import datetime as dt

class TestDay:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        zones = [
            Zone("10:00", "11:00", "label1"),
            Zone("17:00", "21:00", "label2")
        ]
        self.day = Day(zones, "2022-07-03")

        # Define tasks
        self.task1 = Task("task1", "label1", 60)
        self.task2 = Task("task2", "label2", 60)

    def test_add_task(self):
        # Test that a task that fits the zones can be added
        result = self.day.add_task(self.task1)
        assert result
        # Test add
        result = self.day.add_task(self.task2)
        assert result

        # Test that a task that doesn't fit but has correct label can't be added
        task3 = Task("task3", "label1", 300)
        result = self.day.add_task(task3)
        assert not result  # should not have been added because duration is too long for any zone

        # Test that a task with wrong label can't be added 
        task4 = Task("task4", "label3", 30)
        result = self.day.add_task(task4)
        assert not result  # should not have been added because label is incorrect for any zone