from pydantic import BaseModel, HttpUrl, AwareDatetime
from typing import Literal
from datetime import date

class Source(BaseModel):
    identifier: str
    publisher: str
    jurisdiction: str
    url: HttpUrl
    access_type: Literal["api", "rss", "download", "web", "manual"]
    url_terms_of_use: HttpUrl | None = None
    status: Literal["active", "inactive"]

class RegulatoryDocument(BaseModel):
    source_id: str
    title: str
    document_type: Literal[
    "portaria",
    "resolucao",
    "consulta_publica",
    "norma_regulamentadora",
    "outro",
]
    official_reference: str | None = None
    document_url: HttpUrl | None = None
    published_at: date | None = None
    collected_at: AwareDatetime
    content_hash: str | None = None