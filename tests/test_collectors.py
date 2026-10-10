from datetime import date, datetime, UTC
import pytest
from src.collectors import InMemoryCollector
from src.main import Source, RegulatoryDocument
from test_source import make_source_data

def test_in_memory_collector_active_source():
    source_data = make_source_data(status="active")
    source = Source(**source_data)
    collector = InMemoryCollector()
    documents = collector.collect(source)
    assert isinstance(documents, list)
    assert len(documents) > 0, "Collector returned an empty list"
    assert all(isinstance(doc, RegulatoryDocument) for doc in documents), "Collector did not return a list of RegulatoryDocument instances"
    assert all(doc.source_id == source.identifier for doc in documents), "Document source_id does not match the source identifier"
    assert all(doc.collected_at is not None for doc in documents), "Document collected_at is None"
    assert all(doc.collected_at.tzinfo is not None and doc.collected_at.utcoffset() is not None for doc in documents), "Document collected_at is not timezone naive"
    assert all(doc.published_at is None or isinstance(doc.published_at, date) for doc in documents), "Document published_at is not a datetime instance"


def test_in_memory_collector_inactive_source():
    source_data = make_source_data(status="inactive")
    source = Source(**source_data)
    collector = InMemoryCollector()
    with pytest.raises(ValueError, match="Source is not active"):
        collector.collect(source)