import pytest
from src.ingest import ingest_alert
from src.normalize import normalize_alert
from src.enrich import enrich_alert
from src.triage import triage_alert

def test_triage_alert_basic():
    alert_file = "tests/mocks/test_source.json"
    alert_ingested = ingest_alert(alert_file)
    alert_normalized = normalize_alert(alert_ingested)
    alert_enriched = enrich_alert(alert_normalized)
    
    result = triage_alert(alert_enriched)
    assert result['triage']['severity'] >= 70
    assert len(result['triage']['tags']) > 0
    assert result['mitre']['techniques'] == ["T1566"]
    assert 'timeline' in result
