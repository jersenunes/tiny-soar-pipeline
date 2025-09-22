import pytest
from src.ingest import ingest_alert

def test_ingest_alert(tmp_path):
    alert_file = "tests/mocks/test_source.json"

    result = ingest_alert(alert_file)

    assert result['alert_id'] == "123"
    assert result['source'] == "test"
    assert 'timeline' in result
