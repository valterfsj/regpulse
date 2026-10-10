from src.sources import DocumentArtifact
from datetime import datetime
import pytest
from pydantic import HttpUrl, ValidationError

def make_happy_case(**overrides):
    data = {
        "document_id": "doc1",
        "source_url": "https://example.com/doc1",
        "media_type": "application/pdf",
        "content_hash": "abc123",
        "size_bytes": 1024,
        "collected_at": datetime.now().astimezone(),
        "storage_key": "storage_key_1"
    }
    data.update(overrides)
    return DocumentArtifact(**data)

def test_document_artifact_creation():
    artifact = make_happy_case()
    assert artifact.document_id == "doc1"
    assert str(artifact.source_url) == "https://example.com/doc1"
    assert artifact.media_type == "application/pdf"
    assert artifact.content_hash == "abc123"
    assert artifact.size_bytes == 1024
    assert artifact.collected_at is not None
    assert artifact.storage_key == "storage_key_1"
    assert isinstance(artifact.collected_at, datetime)

def test_size_bytes():
    artifact = make_happy_case(size_bytes=2048)
    assert artifact.size_bytes == 2048
    with pytest.raises(ValidationError):
        artifact = make_happy_case(size_bytes=-1024)

def test_media_type():
    artifact = make_happy_case(media_type="text/html")
    assert artifact.media_type == "text/html"
    artifact = make_happy_case(media_type="application/pdf")
    assert artifact.media_type == "application/pdf"
    artifact = make_happy_case(media_type="text/plain")
    assert artifact.media_type == "text/plain"
    artifact = make_happy_case(media_type="image")
    assert artifact.media_type == "image"
    # Test invalid media type should raise a validation error
    with pytest.raises(ValueError):
        make_happy_case(media_type="invalid/type")

def test_collected_at():
    artifact = make_happy_case()
    assert artifact.collected_at.tzinfo is not None
    assert artifact.collected_at.utcoffset() is not None
    now = datetime.now().astimezone()
    artifact = make_happy_case(collected_at=now)
    assert artifact.collected_at == now

def test_storage_key():
    artifact = make_happy_case()
    assert artifact.storage_key == "storage_key_1"
    artifact = make_happy_case(storage_key="storage_key_2")
    assert artifact.storage_key == "storage_key_2"
    # Test invalid storage key should raise a validation error
    with pytest.raises(ValueError):
        make_happy_case(storage_key="")