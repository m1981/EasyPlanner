from dataclasses import dataclass

@dataclass
class Task:
    title: str
    label: str
    duration: int
    scheduled_date: datetime.datetime = None  # Whatever appropriate value
    scheduled_start: datetime.datetime = None  # Whatever appropriate value 
