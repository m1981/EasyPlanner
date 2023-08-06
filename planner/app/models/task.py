from datetime import datetime as dt
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Task:
    title: str
    label: str
    duration: int
    scheduled_date: Optional[dt] = field(default=None)
    scheduled_start: Optional[dt] = field(default=None)

    def __post_init__(self):
        if not self.title:
           raise ValueError("Task title cannot be empty")
        if not self.label:
           raise ValueError("Task label cannot be empty")
        if not self.duration or self.duration < 0:
           raise ValueError("Task duration cannot be empty or negative")

    def set_scheduled_detail(self, date, start):
      self.scheduled_date = date
      self.scheduled_start = start
  
    def __repr__(self):
        return f"{self.title} ({self.duration} min at {self.scheduled_start} on {self.scheduled_date})"
