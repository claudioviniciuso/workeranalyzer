from datetime import datetime

class SimpleMetricsBuilder:
    def __init__(self, name) -> None:
        if not isinstance(name, str) or not name:
            raise ValueError("Name must be a non-empty string")

        self.name = name
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.status = None
        self.errors = []

    @property
    def metrics(self):
        """ Returns a dictionary of the collected metrics. """
        return {
            "name": self.name,
            "status": self.status,
            "duration": self.duration,
            "errors": self.errors
        }

    def start(self):
        """ Marks the start time of the metric collection. """
        if self.start_time is not None:
            raise Exception("Metrics collection has already started")
        self.start_time = datetime.now()

    def end(self, status, error_content=None):
        """ Marks the end time of the metric collection, sets the status, and logs any error. """
        if self.end_time is not None:
            raise Exception("Metrics collection has already ended")
        if self.start_time is None:
            raise Exception("Metrics collection must be started before ending")

        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds() if self.start_time else None
        if error_content:
            self.errors.append({"time": datetime.now(), "content": error_content})
        self.status = status
