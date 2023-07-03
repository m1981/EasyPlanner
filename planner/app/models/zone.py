class Zone:
    def __init__(self, label, start_time, end_time):
        self.start_time = self._parse_time(start_time)
        self.end_time = self._parse_time(end_time)
        
        if self.end_time <= self.start_time:
            raise ValueError("End time must be later than start time")
        
        self.label = label
        print(f"Zone created. Label: {self.label}, Start Time: {self.start_time}, End Time: {self.end_time}")

    def _parse_time(self, time):
        if isinstance(time, str) and ':' in time:
            hours, minutes = map(int, time.split(':'))
            return hours * 60 + minutes  # returns time in minutes for easier comparison
        elif isinstance(time, int):
            return time
        else:
            raise TypeError("Time must be a string in the format 'HH:MM' or an integer representing minutes since midnight")


    # Getters
    def get_label(self):
        return self.label

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    # Setters
    def set_label(self, label):
        self.label = label

    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_end_time(self, end_time):
        self.end_time = end_time
