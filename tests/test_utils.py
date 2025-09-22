import pytest
from src.utils import add_timeline

def test_add_timeline_structure():
    tl = add_timeline("ingest", "details")
    assert tl['stage'] == "ingest"
    assert 'ts' in tl
    assert tl['details'] == "details"
