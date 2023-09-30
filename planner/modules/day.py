import logging
import datetime as dt
import calendar

logger = logging.getLogger(__name__)


class Task:

  def __init__(self, title, label, duration):
    assert isinstance(label, list), ("Label should be a list of labels")
    self.title = title
    self.label = label
    self.duration = int(duration.replace("min", "")) if duration else 30
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
    return f"{self.title} ({self.duration} min at {self.scheduled_start} on {self.scheduled_date})"


class Zone:

  def __init__(self, start, end, labels, schedule_date=None):
    assert start and end and isinstance(start, str) and isinstance(end, str), "Start and end times must be non-empty strings"
    assert start < end, "End time should be greater than start time"
    assert labels and all(labels), "Label list should not be empty"
    assert schedule_date is None or isinstance(schedule_date, dt.date), (
      "schedule_date should either be None or a datetime.date instance")

    if isinstance(labels, str):
      labels = [labels]
    if isinstance(start, str):
      start = dt.datetime.strptime(start, "%H:%M").time()
    if isinstance(end, str):
      end = dt.datetime.strptime(end, "%H:%M").time()


    self.start = start
    self.end = end
    self.labels = labels
    self.tasks = []
    self.current_time = start
    self.schedule_date = schedule_date

    logger.debug(
      f'Creating zone starting at {self.start}, ending at {self.end} for label {self.labels}'
    )
    self._calculate_total_time()

  def _calculate_total_time(self):
    # create remaining_mins attribute
    start_datetime = dt.datetime.combine(dt.date.today(), self.start)
    end_datetime = dt.datetime.combine(dt.date.today(), self.end)
    self.remaining_mins = int((end_datetime - start_datetime).total_seconds() // 60)


  def __repr__(self):
    return f"\n{self.labels} from {self.start} to {self.end} with {len(self.tasks)} tasks: {self.tasks}"

  def add(self, task):
      if self.fits(task):
          self.tasks.append(task)
          task.set_scheduled_detail(self.schedule_date, self.current_time)
          self.current_time = (dt.datetime.combine(dt.date.today(), self.current_time) + dt.timedelta(minutes=task.duration)).time()
          self._calculate_total_time()  # re-calculate remaining minutes after a new task is added
          return True
      return False

  def fits(self, task):
      # Only checking if there's enough remaining time for task in Zone
      # For label compatibility, it checks if Zone's label is in Task's label
      assert isinstance(task.label, list), "task.label should be a list of labels"
      
      if any(lbl in self.labels for lbl in task.label):
          end_datetime = dt.datetime.combine(dt.date.today(), self.end)
          new_end_time = (dt.datetime.combine(dt.date.today(), self.current_time) +
                          dt.timedelta(minutes=task.duration))
          return new_end_time <= end_datetime  # it fits when the new end time is less than the Zone's end time
      return False  # doesn't fit if the Zone's label is not found in the Task's labels
  


class Day:

  def __repr__(self):
    return f"\nZones for day {self.zones[0].schedule_date} are: {self.zones}"

  def __init__(self, zones, schedule_date_string):
        today = dt.date.today()
        weekday_today = today.weekday()  # Monday is 0 and Sunday is 6
        days_ahead = (list(calendar.day_name).index(schedule_date_string) - weekday_today) % 7
        schedule_date = today + dt.timedelta(days=days_ahead)

        self.zones = [Zone(start=z['start'], end=z['end'], labels=[z['label']], schedule_date=schedule_date) for z in zones]
        self.zones.sort(key=lambda x: x.start)  

  def add_task(self, task):
    if not self.zones:  # Check if the zones list is empty
      logger.debug(f"No zones defined. Task not added.")
      return False

    for zone in self.zones:
      if zone.add(task):
        logger.debug(
          f"Task added task to the day's zone. {task.label}, {task.duration} min"
        )
        return True

    logger.debug(f"Task not added. {task.title}, {task.duration} min, {zone}")
    return False
