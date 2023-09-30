import logging
from flask import Flask, render_template, jsonify, request
from todoist_api_python.api import TodoistAPI
import re
import datetime as dt
from itertools import cycle
from planner.modules.day import Task, Day, Zone

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Define your API key globally:
API_KEY = "583cd2d37748348ee7173e1e32307ccfd4b4ed31"



from collections import deque

class Planner:

  def __init__(self, tasks, zones):
      # make it a deque for efficient popleft operation and sort by duration
      self.tasks = deque(sorted(tasks, key=lambda x: x.duration, reverse=True))
      self.days = [
          Day(zones[day], schedule_date_string=day) for day in [
              'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
              'Sunday'
          ]
      ]

  def schedule(self):
      today = dt.date.today()
      for day_num in cycle(range(7)):
          # Set the date for each day as today plus the number of days passed since scheduling started.
          schedule_date = today + dt.timedelta(days=day_num)
          # Set the schedule_date property of every zone in the day.
          for zone in self.days[day_num].zones:
              zone.schedule_date = schedule_date
          
          while self.tasks:  # while there are still tasks to schedule
              task = self.tasks[0]  # peek at leftmost task
              if self.days[day_num].add_task(task):
                  logger.debug(
                      f'Added Task({task.label}, {task.duration} min) to a day\'s zone.'
                  )
                  self.tasks.popleft()  # remove it from queue
                  
                  # Check from shortest unscheduled task to fill in the remaining time
                  if self.tasks:
                      for idx, remaining_task in enumerate(reversed(self.tasks)): 
                          if self.days[day_num].add_task(remaining_task):
                              del self.tasks[-idx-1]  # delete the scheduled task from deque
                              break 
              else:
                  break  # break out of loop to move to next day
              
          if not self.tasks:  # All tasks are scheduled!
              break

      if self.tasks:  # if there are still unscheduled tasks
          print("The following tasks couldn't be scheduled due to their long durations:")
          for task in self.tasks:
              print(task)

              
  # Generates a data structure ready for frontend consumption
  def get_scheduled_tasks(self):
    scheduled_tasks = []
    for i, day in enumerate(self.days):
        for zone in day.zones:
            for task in zone.tasks:
                if task.scheduled_start is not None:
                    scheduled_tasks.append({
                        "content": f'{task.title} ({task.duration} min)',
                        "start_date": (dt.datetime.combine(task.scheduled_date, dt.time(int(task.scheduled_start.split(':')[0]), int(task.scheduled_start.split(':')[1])))).isoformat(),
                        "end_date": (dt.datetime.combine(task.scheduled_date, dt.time(int(task.scheduled_start.split(':')[0]), int(task.scheduled_start.split(':')[1]))) + dt.timedelta(minutes=task.duration)).isoformat(),
                    })
    return scheduled_tasks


zones = {
  "Monday": [{
    "start": "10:00",
    "end": "11:00",
    "label": "ForMyself😎"
  }, {
    "start": "17:00",
    "end": "21:00",
    "label": "ForWorld🌎"
  }],
  "Tuesday": [{
    "start": "10:00",
    "end": "11:00",
    "label": "ForMyself😎"
  }, {
    "start": "17:00",
    "end": "21:00",
    "label": "ForWorld🌎"
  }],
  "Wednesday": [{
    "start": "10:00",
    "end": "11:00",
    "label": "ForMyself😎"
  }, {
    "start": "17:00",
    "end": "21:00",
    "label": "ForWorld🌎"
  }],
  "Thursday": [{
    "start": "10:00",
    "end": "11:00",
    "label": "ForMyself😎"
  }, {
    "start": "17:00",
    "end": "21:00",
    "label": "ForWorld🌎"
  }],
  "Friday": [{
    "start": "10:00",
    "end": "11:00",
    "label": "ForMyself😎"
  }, {
    "start": "17:00",
    "end": "21:00",
    "label": "ForWorld🌎"
  }],
  "Saturday": [
    {
      "start": "10:00",
      "end": "23:00",
      "label": "ForMyself😎"
    },
  ],
  "Sunday": [
    {
      "start": "10:00",
      "end": "23:00",
      "label": "ForMyself😎"
    },
  ],
}


@app.route('/')
def index():
  api = TodoistAPI(API_KEY)
  projects = api.get_projects()
  return render_template('index.html', projects=projects)


@app.route("/get_projects")
def get_projects():
  api = TodoistAPI(API_KEY)
  projects = api.get_projects()
  project_list = []
  for project in projects:
    project_list.append({"id": project.id, "name": project.name})
  return jsonify({"projects": project_list})


@app.route("/get_tasks_for_project/<project_id>")
def get_tasks_for_project(project_id):
  print('get_tasks_for_project')
  api = TodoistAPI(API_KEY)
  tasks = api.get_tasks(project_id=project_id)
  tasks_for_project = []
  for task in tasks:
    task_dict = {"content": task.content, "all_labels": task.labels}

    # Check if the task object has a 'labels' attribute.
    if hasattr(task, 'labels'):
      labels = task.labels

      # If labels are a list of dictionaries, extract their 'name' attribute.
      if isinstance(labels, list) and all(
          isinstance(label, dict) for label in labels):
        labels = [label['name'] for label in labels]

      # Iterate over labels and check for the duration labels.
      for label in labels:
        if isinstance(label, str) and label in ['10min', '30min', '60min']:
          task_dict["duration"] = label
    tasks_for_project.append(task_dict)
  return jsonify({"tasks": tasks_for_project})


@app.route("/get_labels")
def get_labels():
  api = TodoistAPI(API_KEY)
  labels = api.get_labels()
  label_list = []
  for label in labels:
    label_list.append({"id": label.id, "name": label.name})
  return jsonify({"labels": label_list})


@app.route("/schedule_tasks", methods=["POST"])
def schedule_tasks_route():
  logger.debug('Starting schedule_tasks_route function.')

  api = TodoistAPI(API_KEY)

  selected_labels = set(request.form.getlist("selected_labels[]"))
  project_ids = request.form.getlist("project_ids[]")

  logger.debug(f'Selected labels: {selected_labels}')
  logger.debug(f'Project Ids: {project_ids}')

  # Fetch all labels 
  all_labels = api.get_labels()
  # Create label name to id mapping
  name_to_id = {label.name: str(label.id) for label in all_labels}

  logger.debug(f'All Labels: {name_to_id}')

  selected_tasks = []

  for project_id in project_ids:
    tasks = api.get_tasks(project_id=project_id)
    logger.debug(f'Fetched {len(tasks)} tasks for project {project_id}')

    for task in tasks:
      task_labels = [label for label in task.labels]  # task labels are names
      logger.debug(f'Task id: {task.id} labels conv to {task_labels}')

      duration_labels = [label for label in task_labels if bool(re.match(r'^\d+min$', label))]
      if len(duration_labels) > 0:
        duration = duration_labels[0]
      else:
        duration = '30min'
      
      # Removing all duration labels
      task_types = set(task_labels) - set(duration_labels)

      logger.debug(f'Task types: {task_types}')
      logger.debug(f'Selected labels: {selected_labels}')
      
      for task_label in task_types:
        if task_label in selected_labels:
          selected_tasks.append(Task(title=task.content, label=[task_label], duration=duration))
          logger.debug(f'Task added : {task.content} with label {task_label} and duration {duration}')
        else:
          logger.debug(f'Task label not in selected labels: {task_label}')

  logger.debug(f'Selected tasks: {selected_tasks}')

  planner = Planner(selected_tasks, zones)
  planner.schedule()

  logger.debug(f'Finished scheduling tasks. Current planner state: {planner.__dict__}')
  logger.debug(f'Finished scheduling tasks. Current planner state: {planner.__dict__}')
  for task in planner.tasks:
    logger.debug(str(task))
  for day in planner.days:
    logger.debug(str(day))
  logger.debug('Finished schedule_tasks_route function.')

  scheduled_tasks = planner.get_scheduled_tasks()  
  return jsonify({"scheduled_tasks": scheduled_tasks}), 200



app.run(host='0.0.0.0', port=81)
