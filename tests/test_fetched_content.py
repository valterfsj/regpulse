from src.sources import FetchedContent
from datetime import datetime
import pytest
from pydantic import ValidationError

def create_happy_path(**overrides):
    data = {
        "body": b"example content",
        "media_type": "text/html",
        "size_bytes": 1024,
        "content_hash": "abc123",
        "fetched_at": datetime.now().astimezone()
    }
    data.update(overrides)
    return FetchedContent(**data)

def test_fetched_content_creation():
    content = create_happy_path()
    assert content.body == b"example content"
    assert content.media_type == "text/html"
    assert content.size_bytes == 1024
    assert content.content_hash == "abc123"
    assert content.fetched_at is not None
    assert isinstance(content.fetched_at, datetime)

def test_empty_body_is_allowed():
    content = create_happy_path(body=b"")
    assert content.body == b""

def test_size_bytes():
    content = create_happy_path(size_bytes=2048)
    assert content.size_bytes == 2048
    with pytest.raises(ValidationError):
        create_happy_path(size_bytes=-1024)

def test_media_type():
    content = create_happy_path(media_type="text/html")
    assert content.media_type == "text/html"
    content = create_happy_path(media_type="application/pdf")
    assert content.media_type == "application/pdf"
    content = create_happy_path(media_type="text/plain")
    assert content.media_type == "text/plain"
    content = create_happy_path(media_type="image")
    assert content.media_type == "image"
    with pytest.raises(ValidationError):
        create_happy_path(media_type="invalid/type")

def test_body():
    content = create_happy_path(body=b"new content")
    assert content.body == b"new content"
    with pytest.raises(ValidationError):
        create_happy_path(body=None)