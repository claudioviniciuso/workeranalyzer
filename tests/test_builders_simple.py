import uuid
import pytest
from datetime import datetime
from worker_analyzer.builders import SimpleMetricsBuilder, DefaultMetricsBuilder



def test_metrics_builder_initialization():
    metrics_builder = SimpleMetricsBuilder("metrics1")
    assert metrics_builder.name == "metrics1"
    assert metrics_builder.start_time is None
    assert metrics_builder.end_time is None
    assert metrics_builder.duration is None
    assert metrics_builder.status is None
    assert metrics_builder.errors == []

def test_start_metrics_collection():
    metrics_builder = SimpleMetricsBuilder("metrics1")
    metrics_builder.start()
    assert metrics_builder.start_time is not None

    with pytest.raises(Exception):
        metrics_builder.start()  # Testando iniciar uma coleta de métricas já iniciada

def test_end_metrics_collection():
    metrics_builder = SimpleMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics_builder.end("success")
    assert metrics_builder.end_time is not None
    assert metrics_builder.duration is not None
    assert metrics_builder.status == "success"

    with pytest.raises(Exception):
        metrics_builder.end("success")  # Testando finalizar uma coleta de métricas já finalizada

def test_end_metrics_collection_with_error():
    metrics_builder = SimpleMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics_builder.end("success", "error content")
    assert metrics_builder.end_time is not None
    assert metrics_builder.duration is not None
    assert metrics_builder.status == "success"
    assert metrics_builder.errors == [{"time": metrics_builder.end_time, "content": "error content"}]


