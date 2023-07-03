from datetime import timedelta

class Schedule:
    def __init__(self, night_start, night_end, start_date=None):
        self.tasks = {}
        self.start_date = start_date
        self.night_start = night_start
        self.night_end = night_end

    def add_task(self, task, time_slot):
        self.tasks[task] = time_slot

    def remove_task(self, task):
        self.tasks.pop(task, None)

    def get_tasks(self):
        return self.tasks

    def match_labels(self, task, zone):
        return zone.get_label() in task.get_labels()

    def calculate_task_time(self, task, zone):
        task_start = self.start_date + \
            timedelta(hours=int(zone.get_start_time().split(":")[0]),
                      minutes=int(zone.get_start_time().split(":")[1]))
        task_end = task_start + timedelta(minutes=int(task.get_duration()[:-3]))
        return task_start, task_end

    def check_night_hours(self, task_start):
        if self.night_start <= task_start.hour < self.night_end:
            task_start += timedelta(days=1)
        return task_start

    def task_fits_in_zone(self, task_end, zone):
        zone_end_time = zone.get_end_time()
    
        # Convert task_end to the same format as zone_end_time for comparison
        task_end_time = task_end.hour * 60 + task_end.minute
    
        return task_end_time <= zone_end_time



    def schedule_tasks(self, tasks, zones):
        for task in tasks:
            for zone in zones:
                if self.match_labels(task, zone):
                    task_start, task_end = self.calculate_task_time(task, zone)
                    task_start = self.check_night_hours(task_start)
                    if self.task_fits_in_zone(task_end, zone):
                        self.add_task(task, TimeSlot(task_start, task_end))
                        break
