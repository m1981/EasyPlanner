from flask import Flask, render_template, jsonify
from todoist_api_python.api import TodoistAPI
import datetime

app = Flask(__name__)

# Define your API key globally:
API_KEY = "583cd2d37748348ee7173e1e32307ccfd4b4ed31"
NIGHT_START_HOUR = 0  # midnight
NIGHT_END_HOUR = 6  # 6 AM

zones = {
    "Monday": [
        {"start": "10:00", "end": "11:00", "label": "ForMyself😎"},
        {"start": "17:00", "end": "20:00", "label": "ForWorld"}
    ],
    # other days...
}

def get_zone_total_time(zones):
    zone_times = {}
    for day, day_zones in zones.items():
        total_time = 0
        for zone in day_zones:
            start_time = int(zone["start"].split(":")[0]) * 60 + int(zone["start"].split(":")[1])
            end_time = int(zone["end"].split(":")[0]) * 60 + int(zone["end"].split(":")[1])
            total_time += end_time - start_time
        zone_times[day] = total_time
    return zone_times

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


from flask import request


@app.route("/schedule_tasks", methods=["POST"])
def schedule_tasks_route():
    print("schedule_tasks_route")
    selectedLabels = set(request.form.getlist("selected_labels[]"))
    project_ids = request.form.getlist("project_ids[]")
    start_date_str = request.form["start_date"]
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")

    print(f"Selected Labels: {selectedLabels}")
    print(f"Selected Project IDs: {project_ids}")
    print(f"Start Date: {start_date}")

    api = TodoistAPI(API_KEY)

    # Fetch tasks from all selected projects
    all_project_tasks = []
    for project_id in project_ids:
        tasks = api.get_tasks(project_id=project_id)
        all_project_tasks.extend(tasks)

    tasks_for_project = []
    for task in all_project_tasks:
        print(f"Task: {task}")
        print(f"Task Labels: {task.labels}")
        
        # Compare the task label names with the selected label names
        if set(task.labels).intersection(selectedLabels):
            print("Selected Labels Match")
            task_dict = {"content": task.content, "all_labels": task.labels}

            # Check for duration labels.
            for label in task.labels:
                if isinstance(label, str) and label in ['10min', '30min', '60min']:
                    task_dict["duration"] = label
            print(task_dict)
            tasks_for_project.append(task_dict)

    scheduled_tasks = schedule_tasks(tasks_for_project, start_date)
    return jsonify({"scheduled_tasks": scheduled_tasks})

def schedule_tasks(tasks, start_date):
    print('schedule_tasks')
    print(tasks)
    scheduled_tasks = []

    # Combine all zones and sort them
    all_zones = sorted([zone for day_zones in zones.values() for zone in day_zones],
                       key=lambda z: (int(z["start"].split(":")[0]), int(z["start"].split(":")[1])))
    
    for task in tasks:
        duration = 30  # default to 30 minutes if no label is specified
        if "duration" in task:
            duration = int(task["duration"][:-3])
            print("Task Duration:", duration)
        
        # Iterate over zones to find one where the task fits
        for zone in all_zones:
            if zone["label"] in task["all_labels"]:
                print(f"Zone Found: {zone['label']}")
                # Modify start and end dates of task according to zone time
                task_start_date = start_date + datetime.timedelta(hours=int(zone["start"].split(":")[0]), minutes=int(zone["start"].split(":")[1]))
                task_end_date = task_start_date + datetime.timedelta(minutes=duration)

                print("Task Start Date:", task_start_date)
                print("Task End Date:", task_end_date)

                # Check if task falls within night hours. If it does, move to the next day
                if NIGHT_START_HOUR <= task_start_date.hour < NIGHT_END_HOUR:
                    print("Task falls within night hours, moving to next day.")
                    task_start_date += datetime.timedelta(days=1)
                    task_end_date += datetime.timedelta(days=1)

                # Check if the task fits within the zone and doesn't reach into the next zone or night hours
                next_zone_start = start_date + datetime.timedelta(days=1) if all_zones.index(zone) + 1 == len(all_zones) else start_date + datetime.timedelta(hours=int(all_zones[all_zones.index(zone) + 1]["start"].split(":")[0]), minutes=int(all_zones[all_zones.index(zone) + 1]["start"].split(":")[1]))

                print("Next Zone Start:", next_zone_start)
                # Determine the start of the night
                night_start = task_start_date.replace(hour=NIGHT_START_HOUR)
                if task_start_date.hour >= NIGHT_START_HOUR:
                    night_start += datetime.timedelta(days=1)
                print("Night Start:", night_start)
                
                min_next_or_night_start = min(next_zone_start, night_start)
                print("Minimum of Next Zone Start and Night Start:", min_next_or_night_start)

                if task_end_date < min_next_or_night_start:
                    # This task can be scheduled in this zone
                    print("Task scheduled successfully.")

                    task["start_date"] = task_start_date.strftime("%Y-%m-%d %H:%M:%S")
                    task["end_date"] = task_end_date.strftime("%Y-%m-%d %H:%M:%S")
                    scheduled_tasks.append(task)
                    
                    # Stop looking for zones once a task is scheduled
                    break
                else:
                    print("Task did not fit in zone.")

    return scheduled_tasks



app.run(host='0.0.0.0', port=81)
