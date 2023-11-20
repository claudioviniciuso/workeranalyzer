import uuid
import os
from datetime import datetime
import json
from collections import Counter

class Session:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.status = None
        self.custom_attributes = {}
        self.tasks = []

    @property
    def session(self):
        """
        Get session dictionary
        :return: session dictionary
        """
        return {
            "id": self.id,
            "start_time": self.start_time.isoformat() if self.start_time is not None else None,
            "end_time": self.end_time.isoformat() if self.end_time is not None else None,
            "duration": self.duration,
            "status": self.status,
            "custom_attributes": self.custom_attributes,
            "tasks": self.tasks,
        }

    def add_attribute(self, key, value):
        """
        Add custom attribute to session
        :param key: name of attribute
        :param value: value of attribute
        :return: None
        """
        if key in self.custom_attributes:
            raise Exception("Attribute already exists")

        if key == ["id", "start_time", "end_time", "status", "tasks"]:
            raise Exception(f"Attribute name '{key}' is reserved")

        if not key and not value:
            raise Exception("Attribute name and value cannot be empty")

        self.custom_attributes[key] = value

    def start(self):
        """
        Start session and set start time
        :return: None
        """
        if self.start_time is not None:
            raise Exception("Session already started")
        self.start_time = datetime.now()
        self.status = "Running"

    @staticmethod
    def __validate_task_dict(task):
        """
        Validate task dictionary
        :param task: task dictionary
        :return: None
        """
        required_keys = [
            "name",
            "start_time",
            "end_time",
            "status",
            "duration",
            "subtasks",
            "id",
        ]
        for key in required_keys:
            if key not in task:
                raise Exception(
                    f"Task missing required key: {key} for adding to session"
                )

        if not isinstance(task["name"], str):
            raise TypeError("Expected string for 'name'")
        if not isinstance(task["status"], str):
            raise TypeError("Expected string for 'status'")
        if not isinstance(task["duration"], (int, float)):
            raise TypeError("Expected int or float for 'duration'")
        if not isinstance(task["subtasks"], list):
            raise TypeError("Expected list for 'subtasks'")
        if not isinstance(task["id"], str):
            raise TypeError("Expected string for 'id'")

    def add_task(self, task: dict):
        if isinstance(task, dict):
            self.__validate_task_dict(task)
            self.tasks.append(task)
        else:
            raise TypeError("Expected dictionary for 'task'")

    def end(self):
        """
        End session and set end time
        :return: None
        """
        if self.end_time is not None:
            raise Exception("Session already ended")
        if self.start_time is None:
            raise Exception("Session not started")

        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
        self.status = "Done"

    def save_tmp_session(self):
        storage_path = os.getenv(
            "WORKER_ANALYZER_STORAGE_PATH", "/default/path/if/not/set"
        )
        if not storage_path:
            raise Exception("Storage path not set")
        
        file_path = os.path.join(storage_path, "tmp_session.json")
        try:
            session_save = self.session
            with open(file_path, "w") as f:
                json.dump(session_save, f)
        except Exception as e:
            print(f"Error saving session: {e}")

    def load_tmp_session(self):
        storage_path = os.getenv(
            "WORKER_ANALYZER_STORAGE_PATH", "/default/path/if/not/set"
        )
        if not storage_path:
            raise Exception("Storage path not set")

        file_path = os.path.join(storage_path, "tmp_session.json")
        try:
            with open(file_path, "r") as f:
                session_load = json.load(f)

                self.id = session_load["id"]
                self.start_time = (
                    datetime.fromisoformat(session_load["start_time"])
                    if session_load["start_time"]
                    else None
                )
                self.end_time = (
                    datetime.fromisoformat(session_load["end_time"])
                    if session_load["end_time"]
                    else None
                )
                self.duration = session_load["duration"]
                self.status = session_load["status"]
                self.custom_attributes = session_load["custom_attributes"]
                self.tasks = session_load["tasks"]
        except Exception as e:
            print(f"Error loading session: {e}")

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
            "start_time": self.start_time.isoformat() if self.start_time is not None else None,
            "end_time": self.end_time.isoformat() if self.end_time is not None else None,
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

