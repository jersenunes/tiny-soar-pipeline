import pytest
from src.ingest import ingest_alert
from src.normalize import normalize_alert

def test_normalize_alert():
    alert_file = "tests/mocks/test_source.json"
    alert_ingested = ingest_alert(alert_file) 

    result = normalize_alert(alert_ingested)

    assert result['asset']['device_id'] == "dev-9999"
    assert result['indicators'][0]['value'] == "76.76.21.21"
    assert 'timeline' in result
