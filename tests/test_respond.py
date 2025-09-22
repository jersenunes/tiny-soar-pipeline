import pytest
from src.ingest import ingest_alert
from src.normalize import normalize_alert
from src.enrich import enrich_alert
from src.triage import triage_alert
from src.respond import respond_alert

def test_respond_alert():
    alert_file = "tests/mocks/test_source.json"
    alert_ingested = ingest_alert(alert_file)
    alert_normalized = normalize_alert(alert_ingested)
    alert_enriched = enrich_alert(alert_normalized)
    alert_triaged = triage_alert(alert_enriched)

    result = respond_alert(alert_triaged)
    assert any(a['type']=='isolate' for a in result.get('actions',[]))
    assert 'timeline' in result
