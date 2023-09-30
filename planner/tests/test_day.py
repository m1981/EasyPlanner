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


def test_adding_a_task_non_fitting_labels():
    zone_1 = {"start": "10:00", "end": "12:00", "label": "ForMyself😎"}
    zone_2 = {"start": "17:00", "end": "21:00", "label": "ForWorld🌎"}

    # Testing the scenario where ForMyself😎 is scheduled for a task with label ForWorld
    task_a = Task("wydrukować szablon", ["ForWorld🌎"], "30min")
    weekday = "Sunday"
    day = Day([zone_1, zone_2], weekday) 

    # Task label doesn't exist in any zone within the day.
    assert day.add_task(task_a) == False
  
def test_adding_a_task_non_fitting_times():
    zone_1 = {"start": "10:00", "end": "12:00", "label": "ForMyself😎"}
    zone_2 = {"start": "17:00", "end": "18:00", "label": "ForWorld🌎"}
  
    # Testing the scenario where only 60 mins left but a task with 90 mins requested
    task_a = Task("wydrukować szablon", ["ForWorld🌎"], "90min")
    weekday = "Sunday"
    day = Day([zone_1, zone_2], weekday) 

    # Task duration > remaining time in the matching zone within the day.
    assert day.add_task(task_a) == False



def test_task_not_scheduled_results_in_infinite_loop():
    # Defining zones where no task can be scheduled
    zones = {
        "Monday": [{"start": "10:00", "end": "11:00", "label": "UNAVAILABLE"}],
        "Tuesday": [{"start": "10:00", "end": "11:00", "label": "UNAVAILABLE"}],
        "Wednesday": [{"start": "10:00", "end": "11:00", "label": "UNAVAILABLE"}],
        "Thursday": [{"start": "10:00", "end": "11:00", "label": "UNAVAILABLE"}],
        "Friday": [{"start": "10:00", "end": "11:00", "label": "UNAVAILABLE"}],
        "Saturday": [{"start": "10:00", "end": "23:00", "label": "UNAVAILABLE"}],
        "Sunday": [{"start": "10:00", "end": "23:00", "label": "UNAVAILABLE"}],
    }
    tasks = [Task("Task 1", ["ForWorld🌎"], "30min"), Task("Task 2", ["ForMyself😎"], "10min")]

    planner = Planner(tasks, zones)

    with pytest.raises(RuntimeError):
         planner.schedule()
