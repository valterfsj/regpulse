import pytest
from src.fetchers import StaticFetcher, HttpCollector
from src.sources import Source, RegulatoryDocument, FetchedContent
from datetime import datetime, UTC

def create_happy_path(**overrides):
    data = {
        "body": b"static content",
        "media_type": "text/html",
        "size_bytes": 14,
        "content_hash": "abc123",
        "fetched_at": datetime.now(UTC)
    }
    data.update(overrides)
    return FetchedContent(**data)

def test_static_fetcher():
    content = FetchedContent(
        body=b"static content",
        media_type="text/html",
        size_bytes=14,
        content_hash="abc123",
        fetched_at=datetime.now(UTC)
    )
    fetcher = StaticFetcher(content)
    url = "https://example.com"
    assert fetcher.fetch(url) == content

def test_http_collector_return():
    content = FetchedContent(
        body=b"static content",
        media_type="text/html",
        size_bytes=14,
        content_hash="abc123",
        fetched_at=datetime.now(UTC)
    )
    fetcher = StaticFetcher(content)
    collector = HttpCollector(fetcher)
    source = Source(
        identifier="id",
        publisher="Example Publisher",
        jurisdiction="BR",
        url="https://example.com",
        access_type="web",
        status="active",
    )
    data = collector.collect(source)
    assert data is not None, "Collector returned None"
    assert isinstance(data, list)
    assert all(isinstance(doc, RegulatoryDocument) for doc in data)
    assert all(doc.source_id == source.identifier for doc in data)
    assert all(doc.document_url == source.url for doc in data)
    assert all(doc.collected_at.tzinfo is not None and doc.collected_at.utcoffset() is not None for doc in data)

def test_empty_content():
    fetcher = StaticFetcher(create_happy_path(body=b""))
    collector = HttpCollector(fetcher)
    source = Source(
        identifier="id",
        publisher="Example Publisher",
        jurisdiction="BR",
        url="https://example.com",
        access_type="web",
        status="active",
    )
    with pytest.raises(ValueError, match="No documents fetched"):
        collector.collect(source)

def test_inactive_source():
    content = create_happy_path()
    fetcher = StaticFetcher(content)
    collector = HttpCollector(fetcher)
    source = Source(
        identifier="id",
        publisher="Example Publisher",
        jurisdiction="BR",
        url="https://example.com",
        access_type="web",
        status="inactive",
    )
    with pytest.raises(ValueError, match="Source is not active"):
        collector.collect(source)
