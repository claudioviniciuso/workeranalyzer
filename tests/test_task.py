import uuid
import pytest
from datetime import datetime
from worker_analyzer.task import Task

def test_task_initialization():
    task = Task("task1")
    assert task.id is not None
    assert task.name == "task1"
    assert task.start_time is None
    assert task.end_time is None
    assert task.duration is None
    assert task.status is None
    assert task.subtasks == []

def test_start_task():
    task = Task("task1")
    task.start()
    assert task.start_time is not None
    assert task.status == "In Progress"

    with pytest.raises(Exception):
        task.start()  # Testando iniciar uma tarefa já iniciada

def test_end_task():
    task = Task("task1")
    task.start()
    task.end()
    assert task.end_time is not None
    assert task.duration is not None
    assert task.status is not None

    with pytest.raises(Exception):
        task.end()  # Testando finalizar uma tarefa já finalizada

def test_add_subtask():
    task = Task("task1")
    task.start()
    subtask = {
        "name": "subtask1",
        "start_time": datetime.now(),
        "end_time": datetime.now(),
        "duration": 1,
        "status": "Success",
        "metrics": [],
    }
    task.add_subtask(subtask)
    assert subtask in task.subtasks

    

def test_add_blank_subtask():
    task = Task("task1")
    task.start()
    with pytest.raises(Exception):
        task.add_subtask({})  # Testando adicionar subtask vazia

def test_add_subtask_before_start():
    task = Task("task1")
    subtask = {
        "name": "subtask1",
        "start_time": datetime.now(),
        "end_time": datetime.now(),
        "duration": 1,
        "status": "Success",
        "metrics": {},
    }
    with pytest.raises(Exception):
        task.add_subtask(subtask)  # Testando adicionar subtask antes de iniciar a tarefa

def test_task():
    task = Task("task1")
    task.start()
    task.end()
    task_dict = task.task
    assert task_dict["id"] == task.id
    assert task_dict["name"] == task.name
    assert task_dict["start_time"] == task.start_time.isoformat()
    assert task_dict["end_time"] == task.end_time.isoformat()
    assert task_dict["duration"] == task.duration
    assert task_dict["status"] == task.status
    assert task_dict["subtasks"] == task.subtasks

def test_task_with_subtasks():
    task = Task("task1")
    task.start()
    subtask = {
        "name": "subtask1",
        "start_time": datetime.now(),
        "end_time": datetime.now(),
        "duration": 1,
        "status": "Success",
        "metrics": []
    }
    task.add_subtask(subtask)
    task_dict = task.task
    assert task_dict["id"] == task.id
    assert task_dict["name"] == task.name
    assert task_dict["start_time"] == task.start_time.isoformat()
    assert task_dict["end_time"] == task.end_time
    assert task_dict["duration"] == task.duration
    assert task_dict["status"] == task.status
    assert task_dict["subtasks"] == task.subtasks

