import logging
from flask import Flask, render_template, jsonify, request
from todoist_api_python.api import TodoistAPI
import re
import datetime as dt
from itertools import cycle

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Define your API key globally:
API_KEY = "583cd2d37748348ee7173e1e32307ccfd4b4ed31"


class Task:

  def __init__(self, label, duration):
    self.label = label
    self.duration = int(duration[:-3]) if duration else 30
    # Additional properties for scheduling detail
    self.scheduled_date = None
    self.scheduled_start = None
    logger.debug(
      f'Creating task with label {self.label} and duration {self.duration} minutes'
    )

  def set_scheduled_detail(self, date, start):
    self.scheduled_date = date
    self.scheduled_start = start

  def __repr__(self):
    return f"{self.label} ({self.duration} min at {self.scheduled_start} on {self.scheduled_date})"


class Zone:
  def __init__(self, start, end, label, schedule_date=None):
      self.start = start
      self.end = end
      self.label = label
      self.tasks = []
      self.remaining_mins = self._calculate_total_time()
      self.schedule_date = schedule_date
      logger.debug(
          f'Creating zone starting at {self.start}, ending at {self.end} for label {self.label}'
      )

  def __repr__(self):
    return f"\n{self.label} from {self.start} to {self.end} with {len(self.tasks)} tasks: {self.tasks}"

  def _calculate_total_time(self):
    start_time = [int(i) for i in self.start.split(":")]
    end_time = [int(i) for i in self.end.split(":")]
    return ((end_time[0] * 60 + end_time[1]) -
            (start_time[0] * 60 + start_time[1]))
  
  def add(self, task):
    if self.fits(task):
      self.tasks.append(task)
      self.remaining_mins -= task.duration
      # Set the scheduled details for the task
      task.set_scheduled_detail(self.schedule_date, self.start)
      logger.debug(
        f'Adding Task({task.label}, {task.duration} min) to zone starting at {self.start}. Remaining min in zone: {self.remaining_mins}'
      )
  
      # after adding the task increment the start time of the zone
      hour, minute = self.start.split(':')
      end_hour, end_minute = self.end.split(':')
      new_time = int(minute) + task.duration
      if new_time >= 60:
        new_time -= 60
        hour = int(hour) + 1
  
      # check if zone time exceeds end time, if so reset to start
      if int(hour) > int(end_hour) or (int(hour) == int(end_hour) and new_time > int(end_minute)):
        hour, new_time = self.start.split(':') # reset to start
      self.start = f'{hour}:{new_time:02d}' # make sure minute is two digits
  
      return True
    else:
      logger.debug(
        f'Task({task.label}, {task.duration} min) does not fit in zone {self.start}. Remaining min in zone: {self.remaining_mins}'
      )
      return False
  
  def fits(self, task):
    hour, minute = self.start.split(':')
    end_hour, end_minute = self.end.split(':')
    new_time = int(minute) + task.duration
    if new_time >= 60:
      new_time -= 60
      hour = int(hour) + 1
    # If the task does not exceed the zone time and matches the label
    if task.label == self.label and not (int(hour) > int(end_hour) or (int(hour) == int(end_hour) and new_time > int(end_minute))):
      return True
    else:
      return False


class Day:
  def __repr__(self):
    return f"\nZones for day {self.zones[0].schedule_date} are: {self.zones}"
    
  def __init__(self, zones, schedule_date):
    self.zones = [Zone(**z, schedule_date=schedule_date) for z in zones]
    self.zones.sort(key=lambda x: x.start)

  def add_task(self, task):
    for zone in self.zones:
      if zone.add(task):
        logger.debug(
          f'Task added task to the day\'s zone. {task.label}, {task.duration} min'
        )
        return True
    logger.debug(
      f'Task not added to current zone. {task.label}, {task.duration} min'
    )

    return False




class Planner:

  def __init__(self, tasks, zones):
    self.tasks = tasks
    self.days = [
      Day(zones[day], schedule_date=day) for day in [  # Include scheduling date
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
        'Sunday'
      ]
    ]


  def schedule(self):
      today = dt.date.today()
      weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
      for task in self.tasks:
          for day_num in cycle(range(7)):
              # Set the date for each day as today plus the number of days passed since scheduling started.
              schedule_date = today + dt.timedelta(days=day_num)
              # Set the schedule_date property of every zone in the day.
              for zone in self.days[day_num].zones:
                  zone.schedule_date = schedule_date
              if self.days[day_num].add_task(task):
                  logger.debug(
                      f'Added Task({task.label}, {task.duration} min) to a day\'s zone.'
                  )
                  break
              logger.debug(
                  f'Failed to add Task({task.label}, {task.duration} min). Cycling to the next day.'
              )
              continue

  # Generates a data structure ready for frontend consumption
  def get_scheduled_tasks(self):
    scheduled_tasks = []
    for i, day in enumerate(self.days):
        for zone in day.zones:
            for task in zone.tasks:
                # Check if the task was actually scheduled
                if task.scheduled_start is not None:
                   scheduled_tasks.append({
                      "content": f'{task.label} ({task.duration} min)',
                      "start_date": dt.datetime.combine(task.scheduled_date, dt.time(int(task.scheduled_start.split(':')[0]), int(task.scheduled_start.split(':')[1]))),
                      "end_date": dt.datetime.combine(task.scheduled_date, dt.time(int(task.scheduled_start.split(':')[0]), int(task.scheduled_start.split(':')[1]))) + dt.timedelta(minutes=task.duration),
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
  print(projects)
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
    print(task_dict)
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
          selected_tasks.append(Task(label=task_label, duration=duration))
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
