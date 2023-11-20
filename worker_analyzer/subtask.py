import uuid
from datetime import datetime
from collections import Counter


class SubTask:
    def __init__(self, name, subtask_type) -> None:
        if not isinstance(name, str):
            raise Exception("Subtask name must be a string")
        if len(name) == 0:
            raise Exception("Subtask name cannot be empty")

        self.id = str(uuid.uuid4())
        self.name = name
        self.subtask_type = subtask_type
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.status = None
        self.metrics = []

    @property
    def subtask(self):
        subtask = {
            "id": self.id,
            "name": self.name,
            "task_type": self.subtask_type,
            "start_time": self.start_time.isoformat() if self.start_time is not None else None,
            "end_time": self.end_time.isoformat() if self.end_time is not None else None,
            "duration": self.duration,
            "status": self.status,
            "metrics": self.metrics,
        }
        return subtask

    def start(self):
        """
        Start subtask and set start time
        """
        if self.start_time is not None:
            raise Exception("Subtask already started")
        self.start_time = datetime.now()
        self.status = "In Progress"

    def add_metric(self, metrics: dict):
        """
        Add metrics to subtask
        :param metrics: metrics to be added
        """
        if not isinstance(metrics, dict):
            raise Exception("Metrics must be a dict")

        if self.start_time is None:
            raise Exception("Subtask not started")

        if self.end_time is not None:
            raise Exception("Subtask already ended")

        if len(metrics) == 0:
            raise Exception("Metrics cannot be empty")
        
        self.metrics.append(metrics)

    def get_status_by_metrics(self):
        """
        Get task status based on metrics
        :return: task status
        """
        status_counts = Counter(metric["status"] for metric in self.metrics)
        if status_counts["success"] == len(self.metrics):
            self.status = "success"
        elif status_counts["failure"] == len(self.metrics):
            self.status = "failure"
        elif len(self.metrics) > 0:
            self.status = "partial"
        else:
            self.status = (
                "not started"  # ou algum outro status padrão para tarefas sem subtasks
            )

        return self.status

    def end(self, status):
        """
        End subtask and set end time
        :return: None
        """
        if self.end_time is not None:
            raise Exception("Subtask already ended")

        if self.start_time is None:
            raise Exception("Subtask not started")

        self.end_time = datetime.now()
        self.status = status
        self.duration = (self.end_time - self.start_time).total_seconds()
