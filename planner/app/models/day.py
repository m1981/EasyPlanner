from __future__ import annotations
from typing import List
from datetime import datetime as dt
from app.models.zone import Zone
from app.models.task import Task

class Day:
    def __init__(self, zones: List[Zone], schedule_date: str):
        self.zones: List[Zone] = zones
        self.schedule_date = dt.strptime(schedule_date, '%Y-%m-%d')

    def add_task(self, task: Task) -> bool:
        for zone in self.zones:
            if zone.add(task):
                return True
        return False