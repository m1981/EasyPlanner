class TimeSlot:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    # Getters
    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    # Setters
    def set_start_time(self, start_time):
        if start_time > self.end_time:
            raise ValueError("Start time cannot be set after end time.")
        self.start_time = start_time


    def set_end_time(self, end_time):
        if end_time < self.start_time:
            raise ValueError("End time cannot be set before start time.")
        self.end_time = end_time
