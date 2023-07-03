class Task:
    def __init__(self, content=None, labels=None, duration=None):
        self.content = content
        self.labels = labels or []
        self.duration = duration

    # Getters
    def get_content(self):
        return self.content

    def get_labels(self):
        return self.labels

    def get_duration(self):
        return self.duration

    # Setters
    def set_content(self, content):
        self.content = content

    def set_labels(self, labels):
        self.labels = labels

    def set_duration(self, duration):
        self.duration = duration
