import uuid
import pytest
from datetime import datetime
from worker_analyzer.session import Session

def test_session_initialization():
    session = Session()
    assert session.id is not None
    assert session.start_time is None
    assert session.end_time is None
    assert session.duration is None
    assert session.status is None
    assert session.custom_attributes == {}
    assert session.tasks == []

def test_add_attribute():
    session = Session()
    session.add_attribute("test_key", "test_value")
    assert "test_key" in session.custom_attributes
    assert session.custom_attributes["test_key"] == "test_value"

    with pytest.raises(Exception):
        session.add_attribute("test_key", "new_value")  # Testando adição de chave duplicada

def test_add_blank_attribute():
    session = Session()
    with pytest.raises(Exception):
        session.add_attribute("", "")  # Testando adição de chave e valor vazios

def test_start_session():
    session = Session()
    session.start()
    assert session.start_time is not None
    assert session.status == "Running"

    with pytest.raises(Exception):
        session.start()  # Testando iniciar uma sessão já iniciada

def test_end_session():
    session = Session()
    session.start()
    session.end()
    assert session.end_time is not None
    assert session.duration is not None
    assert session.status == "Done"

    with pytest.raises(Exception):
        session.end()  # Testando finalizar uma sessão já finalizada

def test_add_task():
    session = Session()
    session.start()
    task = {
        "name": "task1",
        "start_time": datetime.now(),
        "end_time": datetime.now(),
        "duration": 1,
        "status": "Success",
        "subtasks": [],
        "id": str(uuid.uuid4())
        }
    session.add_task(task)
    assert session.tasks == [task]

    with pytest.raises(Exception):
        session.add_task("task")  # Testando adição de tarefa após finalizar sessão

def test_add_task_diferent_type():
    session = Session()
    session.start()
    with pytest.raises(Exception):
        session.add_task("task")  # Testando adição de tarefa com tipo diferente de dict


def test_save_session():
    session = Session()
    session.start()
    task = {
        "name": "task1",
        "start_time": datetime.now(),
        "end_time": datetime.now(),
        "duration": 1,
        "status": "Success",
        "subtasks": [],
        "id": str(uuid.uuid4())
        }
    session.add_task(task)
    session.add_attribute("test_key", "test_value")
    session.end()
    assert session.session == {
        "id": session.id,
        "start_time": session.start_time.isoformat(),
        "end_time": session.end_time.isoformat(),
        "duration": session.duration,
        "status": session.status,
        "custom_attributes": session.custom_attributes,
        "tasks": session.tasks,
    }

def test_start_session_after_end():
    session = Session()
    session.start()
    session.end()
    with pytest.raises(Exception):
        session.start()  # Testando iniciar sessão após finalizar

def test_end_session_before_start():
    session = Session()
    with pytest.raises(Exception):
        session.end()  # Testando finalizar sessão antes de iniciar
    
def test_save_session_without_storage_path():
    session = Session()
    session.start()
    task = {
        "name": "task1",
        "start_time": datetime.now(),
        "end_time": datetime.now(),
        "duration": 1,
        "status": "Success",
        "subtasks": [],
        "id": str(uuid.uuid4())
        }
    session.add_task(task)
    session.add_attribute("test_key", "test_value")
    session.end()
    with pytest.raises(Exception):
        session.save()  # Testando salvar sessão sem definir o caminho de armazenamento