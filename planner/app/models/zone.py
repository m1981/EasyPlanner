# zone.py
from __future__ import annotations
from typing import List, Optional
from datetime import datetime
from app.models.task import Task

class Zone:
    def __init__(self, start: str, end: str, label: str, schedule_date: Optional[datetime] = None):
        self.start = start
        self.end = end
        self.label = label
        self.tasks: List[Task] = []
        self.remaining_mins = self._calculate_total_time()
        self.schedule_date = schedule_date

    def _calculate_total_time(self) -> int:
        start_time = [int(i) for i in self.start.split(":")]
        end_time = [int(i) for i in self.end.split(":")]
        return ((end_time[0] * 60 + end_time[1]) - (start_time[0] * 60 + start_time[1]))

    def add(self, task: Task) -> bool:
        original_start = self.start

        fits = self.fits(task)
        if not fits:
            self.start = original_start
            return False

        self.tasks.append(task)
        self.remaining_mins -= task.duration
        task.set_scheduled_detail(self.schedule_date, original_start)

        hour, minute = self.start.split(':')
        new_time = int(minute) + task.duration
        if new_time >= 60:
            new_time -= 60
            hour = int(hour) + 1
        self.start = f'{hour}:{new_time:02d}'

        return True

    def fits(self, task: Task) -> bool:
        hour, minute = self.start.split(':')
        end_hour, end_minute = self.end.split(':')
        new_time = int(minute) + task.duration
        if new_time >= 60:
            new_time -= 60
            hour = int(hour) + 1

        return (task.label == self.label
            and int(hour) <= int(end_hour)
            and new_time <= int(end_minute))
