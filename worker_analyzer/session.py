import uuid
import os
from datetime import datetime
import json


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
        if not isinstance(task["start_time"], datetime):
            raise TypeError("Expected datetime for 'start_time'")
        if not isinstance(task["end_time"], datetime):
            raise TypeError("Expected datetime for 'end_time'")
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
