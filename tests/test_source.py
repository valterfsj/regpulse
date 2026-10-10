from src.main import Source
import pytest
from pydantic import ValidationError

def make_source_data(**overrides):
    data = {
        "identifier": "lei-exemplo",
        "publisher": "Órgão oficial",
        "jurisdiction": "BR",
        "url": "https://gov.br/legislacao/",
        "access_type": "web",
        "url_terms_of_use": "https://gov.br/legislacao/terms/",
        "status": "active",
    }
    data.update(overrides)
    return data

def test_happy_path():
    source_data = make_source_data()
    source = Source(**source_data)
    assert source.identifier == "lei-exemplo"
    assert source.publisher == "Órgão oficial"
    assert source.jurisdiction == "BR"
    assert str(source.url) == "https://gov.br/legislacao/"
    assert source.access_type == "web"
    assert str(source.url_terms_of_use) == "https://gov.br/legislacao/terms/"
    assert source.status == "active"

def test_invalid_url():
    with pytest.raises(ValidationError):
        Source(**make_source_data(url="not-a-url"))

def test_invalid_access_type():
    with pytest.raises(ValidationError):
        Source(**make_source_data(access_type="scrape"))

def test_invalid_status():
    with pytest.raises(ValidationError):
        Source(**make_source_data(status="unknown"))

def test_optional_fields():
    source_data = make_source_data(url_terms_of_use=None)
    source = Source(**source_data)
    assert source.url_terms_of_use is None

def test_omit_optional_fields():
    source_data = make_source_data()
    del source_data["url_terms_of_use"]
    source = Source(**source_data)
    assert source.url_terms_of_use is None
