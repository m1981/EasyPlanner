from todoist_api_python.api import TodoistAPI

class TodoistAPIWrapper:
    def __init__(self, api_key):
        self.api = TodoistAPI(api_key)

    def get_projects(self):
        try:
            projects = self.api.get_projects()
            return projects
        except Exception as error:
            print(error)
            return []

    def get_tasks_by_project_id(self, project_id):
        try:
            tasks = self.api.get_tasks()
            project_tasks = [task for task in tasks if task.project_id == project_id]
            return project_tasks
        except Exception as error:
            print(error)
            return []
