from flask import Flask, render_template, jsonify
from todoist_api_python.api import TodoistAPI

app = Flask(__name__)

# Define your API key globally:
API_KEY = "583cd2d37748348ee7173e1e32307ccfd4b4ed31"


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
    if task.due is None or task.due.date is None:
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
            task_dict["label"] = label
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
            if task.due is None or task.due.date is None:
                task_dict = {"content": task.content}

                # Check for duration labels.
                for label in task.labels:
                    if isinstance(label, str) and label in ['10min', '30min', '60min']:
                        task_dict["label"] = label
                print(task_dict)
                tasks_for_project.append(task_dict)

    scheduled_tasks = schedule_tasks(tasks_for_project, start_date)

    return jsonify({"scheduled_tasks": scheduled_tasks})







import datetime


# Add this function to your main.py file
def schedule_tasks(tasks, start_date):
  print('schedule_tasks')
  print(tasks)
  scheduled_tasks = []
  current_date = start_date
  for task in tasks:
    print(task)
    duration = 30  # default to 30 minutes if no label is specified
    if "label" in task:
      duration = int(task["label"][:-3])  # remove 'min' and convert to int
      print(duration)
    end_date = current_date + datetime.timedelta(minutes=duration)
    task["start_date"] = current_date
    task["end_date"] = end_date

    scheduled_tasks.append(task)
    current_date = end_date

  return scheduled_tasks


app.run(host='0.0.0.0', port=81)
