from datetime import datetime   

class DefaultMetricsBuilder:
    """
    Default Metrics Builder is a class that helps build metrics based on counts.
    It receives a status, stores it and at the end returns the metrics and status based on the counts per status.
    """
    VALID_STATUSES = {'success', 'failure', 'blank'}

    def __init__(self, name) -> None:
        if not isinstance(name, str) or not name:
            raise ValueError("Subtask name must be a non-empty string")

        self.name = name
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.status = None
        self.total = 0
        self.success = 0
        self.failure = 0
        self.blank = 0
        self.errors = []
        self.additional_metrics = {}

    @property
    def metrics(self):
        """ Returns a dictionary of the collected metrics. """
        self.metrics_dict = {
            "name": self.name,
            "duration": self.duration,
            "status": self.status,
            "total": self.total,
            "success": self.success,
            "failure": self.failure,
            "blank": self.blank,
            "errors": self.errors
        }
        self.metrics_dict.update(self.additional_metrics)
        return self.metrics_dict

    def start(self):
        """ Marks the start time of the metric collection. """
        if self.start_time is not None:
            raise Exception("Metrics collection already started")
        
        self.start_time = datetime.now()
    
    def add_metrics_attr(self, metrics: dict):
        """ Adds metrics to the metrics dictionary. """
        if not isinstance(metrics, dict):
            raise Exception("Metrics must be a dict")

        if self.start_time is None:
            raise Exception("Metrics collection must be started before adding metrics")

        if self.end_time is not None:
            raise Exception("Metrics collection already ended")

        if len(metrics) == 0:
            raise Exception("Metrics cannot be empty")

        keys = metrics.keys()
        for key in keys:
            if key in self.metrics:
                raise Exception(f"Metric '{key}' already exists")
        
        self.additional_metrics.update(metrics)


    def log(self, status, error_content=None):
        """ Logs a specific status and optional error content. """
        if self.start_time is None:
            raise Exception("Metrics collection must be started before logging")
        if self.end_time is not None:
            raise Exception("Metrics collection already ended")
        status = status.lower()
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Valid statuses are: {self.VALID_STATUSES}")

        self.total += 1
        if status == 'success':
            self.success += 1
        elif status == 'failure':
            self.failure += 1
        elif status == 'blank':
            self.blank += 1
        
        if error_content:
            self.errors.append(error_content)

    def end(self):
        """ Marks the end time of the metric collection and calculates duration and final status. """
        if self.start_time is None:
            raise Exception("Metrics collection must be started before ending")

        if self.end_time is not None:
            raise Exception("Metrics collection already ended")

        self.end_time = datetime.now()
        try:
            self.duration = (self.end_time - self.start_time).total_seconds()
        except Exception as e:
            raise Exception(f"Error calculating duration: {e}")

        if self.total == 0:
            self.status = 'Not metrics logged'
        elif self.total == self.success:
            self.status = 'success'
        elif self.total == self.failure:
            self.status = 'failure'
        elif self.total == self.blank:
            self.status = 'partial'
        else:
            self.status = 'Not started'


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
