import pytest
from modules.day import Day, Task, Zone
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s"
)

logger = logging.getLogger(__name__)

def test_task_order():
    zone_definition = {"start": "10:00", "end": "23:00", "label": "ForMyself😎"}
    day = Day([zone_definition], "Monday")

    # Create and add task1
    task1 = Task('Task1', ['ForMyself😎'], '30min')
    result = day.add_task(task1)
    assert result, f"Failed to add task {task1.title} to Day."
    
    # Checking the state after adding task1
    logger.log(day)  # Assuming you have a __str__ or __repr__ method in Day for pretty print

    # Create and add task2
    task2 = Task('Task2', ['ForMyself😎'], '30min')
    result = day.add_task(task2)
    assert result, f"Failed to add task {task2.title} to Day."
    
    # Checking the state after adding task2
    print(day)

    assert day.zones[0].tasks[0] == task1, "Task order incorrect. Task1 is not at position 0."
    assert day.zones[0].tasks[1] == task2, "Task order incorrect. Task2 is not at position 1."



# Test if tasks with correct label can be added
def test_add_task_correct_label():
    task = Task('Test Task', ['ForMyself😎'], '30min')  # Notice the change here
    zone_definition = {"start": "10:00", "end": "23:00", "label": "ForMyself😎"}
    day = Day([zone_definition], "Monday")
    assert day.add_task(task) is True


# Test if tasks are not added when labels are incorrect
def test_add_task_incorrect_label():
    task = Task('Test Task', ['IncorrectLabel'], '30min')
    zone_definition = {"start": "10:00", "end": "23:00", "label": "ForMyself😎"}
    day = Day([zone_definition], "Monday")
    assert day.add_task(task) is False
    assert len(day.zones[0].tasks) == 0

# Test if tasks are added in correct order
def test_task_order():
    zone_definition = {"start": "10:00", "end": "23:00", "label": "ForMyself😎"}
    day = Day([zone_definition], "Monday")
    
    # Create and add task1
    task1 = Task('Task1', ['ForMyself😎'], '30min')
    day.add_task(task1)

    # Create and add task2
    task2 = Task('Task2', ['ForMyself😎'], '30min')
    day.add_task(task2)
    
    # Check the order of tasks added to the first zone for the day
    assert day.zones[0].tasks[0] == task1
    assert day.zones[0].tasks[1] == task2


# Test if tasks with a label not matching any zone are not added
def test_add_task_no_matching_zone():
    task = Task('Test Task', ['NonExistentZone'], '30min')
    zone_definition = {"start": "10:00", "end": "23:00", "label": "ForMyself😎"}
    day = Day([zone_definition], "Monday")
    assert day.add_task(task) is False
    assert len(day.zones[0].tasks) == 0

# Test if tasks are not added to a day with no zones
def test_add_task_no_zones():
    task = Task('Test Task', ['ForMyself😎'], '30min')
    day = Day([], "Monday")  # No zones defined for this day
    assert day.add_task(task) is False


