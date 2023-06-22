from flask import Flask
from app.controllers.planner_controller import PlannerController
from app.views.planner_view import PlannerView

app = Flask(__name__)

# Initialize the PlannerController and PlannerView instances
planner_controller = PlannerController()
planner_view = PlannerView()

# Define your routes and views here, using the planner_controller and planner_view instances

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)
