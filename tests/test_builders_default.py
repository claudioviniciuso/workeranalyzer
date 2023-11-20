import uuid
import pytest
from datetime import datetime
from worker_analyzer.builders import DefaultMetricsBuilder

def test_metrics_builder_initialization():
    metrics_builder = DefaultMetricsBuilder("metrics1")
    assert metrics_builder.name == "metrics1"
    assert metrics_builder.start_time is None
    assert metrics_builder.end_time is None
    assert metrics_builder.duration is None
    assert metrics_builder.status is None
    assert metrics_builder.total == 0
    assert metrics_builder.success == 0
    assert metrics_builder.failure == 0
    assert metrics_builder.errors == []

def test_metrics_builder_start():
    metrics_builder = DefaultMetricsBuilder("metrics1")
    metrics_builder.start()
    assert metrics_builder.start_time is not None

    with pytest.raises(Exception):
        metrics_builder.start()  # Testando iniciar uma coleta de métricas já iniciada
    
def test_metrics_builder_end():
    metrics_builder = DefaultMetricsBuilder("metrics1")
    metrics_builder.start()
    metrics_builder.log("success")
    metrics_builder.end()
    assert metrics_builder.end_time is not None
    assert metrics_builder.duration is not None
    assert metrics_builder.status == "success"
    assert metrics_builder.total == 1

    with pytest.raises(Exception):
        metrics_builder.end("success")  # Testando finalizar uma coleta de métricas já finalizada


