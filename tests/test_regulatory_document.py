from src.sources import RegulatoryDocument
import pytest
from pydantic import ValidationError
from datetime import UTC, datetime, date

def make_regulatory_document_data(**overrides):
    data = {
        "source_id": "id",
        "document_id": "doc-123",
        "title": "Exemplo de Documento",
        "document_type": "portaria",
        "official_reference": "BR-123",
        "document_url": "https://gov.br/legislacao/doc/123/",
        "published_at": date.today(),
        "collected_at": datetime.now(UTC),
        "content_hash": "abc123",
    }
    data.update(overrides)
    return data

def test_happy_path():
    data = make_regulatory_document_data()
    doc = RegulatoryDocument(**data)
    assert doc.source_id == "id"
    assert doc.title == "Exemplo de Documento"
    assert doc.document_type == "portaria"
    assert doc.official_reference == "BR-123"
    assert str(doc.document_url) == "https://gov.br/legislacao/doc/123/"
    assert doc.content_hash == "abc123"
    assert doc.published_at is not None
    assert doc.collected_at is not None
    assert doc.document_id == "doc-123"

def test_missing_required_field():
    data = make_regulatory_document_data()
    del data["source_id"]
    with pytest.raises(ValidationError):
        RegulatoryDocument(**data)

def test_missing_document_id():
    data = make_regulatory_document_data()
    del data["document_id"]
    with pytest.raises(ValidationError):
        RegulatoryDocument(**data)

def test_invalid_url():
    data = make_regulatory_document_data(document_url="invalid-url")
    with pytest.raises(ValidationError):
        RegulatoryDocument(**data)

def test_not_date_fields():
    data = make_regulatory_document_data(published_at="not-a-date", collected_at="not-a-date")
    with pytest.raises(ValidationError):
        RegulatoryDocument(**data)

def test_not_aware_datetime_fields():
    data = make_regulatory_document_data(published_at=datetime.now(), collected_at=datetime.now())
    with pytest.raises(ValidationError):
        RegulatoryDocument(**data)

def test_source_id():
    data = make_regulatory_document_data(source_id=123)
    with pytest.raises(ValidationError):
        RegulatoryDocument(**data)

def test_document_type():
    data = make_regulatory_document_data(document_type="invalid-type")
    with pytest.raises(ValidationError):
        RegulatoryDocument(**data)