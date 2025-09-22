import pytest
from src.ingest import ingest_alert
from src.normalize import normalize_alert
from src.enrich import enrich_alert

def test_enrich_alert():
    alert_file = "tests/mocks/test_source.json"
    alert_ingested = ingest_alert(alert_file)
    alert_normalized = normalize_alert(alert_ingested)

    result = enrich_alert(alert_normalized)
    assert result['indicators'][0]['risk']['verdict'] in ['malicious', 'suspicious', 'clean', 'unknown']
    assert 'sources' in result['indicators'][0]['risk']
    assert 'timeline' in result
