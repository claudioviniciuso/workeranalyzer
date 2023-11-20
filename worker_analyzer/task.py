import uuid
from datetime import datetime
from collections import Counter


class Task:
    def __init__(self, task_name) -> None:
        if not isinstance(task_name, str):
            raise Exception("Task name must be a string")

        if len(task_name) == 0:
            raise Exception("Task name cannot be empty")

        self.id = str(uuid.uuid4())
        self.name = task_name
        self.start_time = None
        self.end_time = None
        self.status = None
        self.duration = None
        self.subtasks = []
        pass

    @property
    def task(self):
        """
        Get task dictionary
        :return: task dictionary
        """
        task = {
            "id": self.id,
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "status": self.status,
            "subtasks": self.subtasks,
        }
        return task

    def start(self):
        """
        Start task and set start time
        :return: None
        """
        if self.start_time is not None:
            raise Exception("Task already started")
        self.start_time = datetime.now()
        self.status = "In Progress"

    @staticmethod
    def __validadate_subtask_dict(subtask):
        required_keys = [
            "name",
            "start_time",
            "end_time",
            "status",
            "duration",
            "metrics",
        ]
        for key in required_keys:
            if key not in subtask:
                raise Exception(
                    f"Task missing required key: {key} for adding to session"
                )
        if not isinstance(subtask["name"], str):
            raise Exception("Task name must be a string")
        if not isinstance(subtask["start_time"], datetime):
            raise Exception("Task start_time must be a datetime object")
        if not isinstance(subtask["end_time"], datetime):
            raise Exception("Task end_time must be a datetime object")
        if not isinstance(subtask["status"], str):
            raise Exception("Task status must be a string")
        if not isinstance(subtask["duration"], (int, float)):
            raise Exception("Task duration must be a int or float")
        if not isinstance(subtask["metrics"], list):
            raise Exception("Task metrics must be a list")

    def add_subtask(self, subtask: dict):
        if not isinstance(subtask, dict):
            raise Exception("Task must be a dictionary")

        if self.start_time is None:
            raise Exception("Task not started")

        if self.end_time is not None:
            raise Exception("Task already ended")

        self.__validadate_subtask_dict(subtask)
        self.subtasks.append(subtask)

    def verify_status(self):
        """
        Verify task status based on subtasks
        """
        status_counts = Counter(subtask["status"] for subtask in self.subtasks)

        if status_counts["success"] == len(self.subtasks):
            self.status = "success"
        elif status_counts["failure"] == len(self.subtasks):
            self.status = "failure"
        elif len(self.subtasks) > 0:
            self.status = "partial"
        else:
            self.status = (
                "not started"  # ou algum outro status padrão para tarefas sem subtasks
            )

        return self.status

    def end(self):
        """
        End task and set end time
        :return: None
        """
        if self.end_time is not None:
            raise Exception("Task already ended")
        if self.start_time is None:
            raise Exception("Task not started")

        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
        self.verify_status()
