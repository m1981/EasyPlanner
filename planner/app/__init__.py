from flask import Flask
from app.controllers import planner_controller

def create_app():
    app = Flask(__name__)

    # Register the blueprint for the PlannerController
    app.register_blueprint(planner_controller.planner_blueprint)

    return app
