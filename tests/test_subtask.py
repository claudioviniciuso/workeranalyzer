import uuid
import pytest
from datetime import datetime
from worker_analyzer.subtask import SubTask

def test_subtask_initialization():
    subtask = SubTask("subtask1", "test_type")
    assert subtask.id is not None
    assert subtask.name == "subtask1"
    assert subtask.subtask_type == "test_type"
    assert subtask.start_time is None
    assert subtask.end_time is None
    assert subtask.duration is None
    assert subtask.status is None
    assert subtask.metrics == []

def test_start_subtask():
    subtask = SubTask("subtask1", "test_type")
    subtask.start()
    assert subtask.start_time is not None
    assert subtask.status == "In Progress"

    with pytest.raises(Exception):
        subtask.start()  # Testando iniciar uma subtask já iniciada

def test_end_subtask():
    subtask = SubTask("subtask1", "test_type")
    subtask.start()
    subtask.end("Success")
    assert subtask.end_time is not None
    assert subtask.duration is not None
    assert subtask.status is not None

    with pytest.raises(Exception):
        subtask.end()  # Testando finalizar uma subtask já finalizada

def test_add_metric():
    subtask = SubTask("subtask1", "test_type")
    subtask.start()
    metrics = {
        "metric1": 1,
        "metric2": 2,
    }
    subtask.add_metric(metrics)
    assert metrics in subtask.metrics

def test_add_blank_metric():
    subtask = SubTask("subtask1", "test_type")
    subtask.start()
    with pytest.raises(Exception):
        subtask.add_metric({})  # Testando adicionar metrica vazia

def test_add_metric_before_start():
    subtask = SubTask("subtask1", "test_type")
    metrics = {
        "metric1": 1,
        "metric2": 2,
    }
    with pytest.raises(Exception):
        subtask.add_metric(metrics)  # Testando adicionar metrica antes de iniciar subtask

def test_add_metric_after_end():
    subtask = SubTask("subtask1", "test_type")
    subtask.start()
    subtask.end("Success")
    metrics = {
        "metric1": 1,
        "metric2": 2,
    }
    with pytest.raises(Exception):
        subtask.add_metric(metrics)  # Testando adicionar metrica depois de finalizar subtask

def test_add_metric_diferent_type():
    subtask = SubTask("subtask1", "test_type")
    subtask.start()
    with pytest.raises(Exception):
        subtask.add_metric("metric")  # Testando adicionar metrica com tipo diferente de dict

def test_subtask():
    subtask = SubTask("subtask1", "test_type")
    subtask.start()
    subtask.end("Success")
    subtask_dict = subtask.subtask
    assert subtask_dict == {
        "id": subtask.id,
        "name": subtask.name,
        "task_type": subtask.subtask_type,
        "start_time": subtask.start_time.isoformat() if subtask.start_time is not None else None,
        "end_time": subtask.end_time.isoformat() if subtask.end_time is not None else None,
        "duration": subtask.duration,
        "status": subtask.status,
        "metrics": subtask.metrics,
    }
