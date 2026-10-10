from pydantic import BaseModel, HttpUrl, AwareDatetime, Field
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
    document_id: str = Field(min_length=1)
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

class DocumentArtifact(BaseModel):
    document_id: str
    source_url: HttpUrl
    media_type: Literal["text/html", "application/pdf", "text/plain", "image"]
    content_hash: str = Field(min_length=1)
    size_bytes: int = Field(ge=0)
    collected_at: AwareDatetime
    storage_key: str = Field(min_length=1)

class FetchedContent(BaseModel):
    body: bytes
    media_type: Literal["text/html", "application/pdf", "text/plain", "image"]
    size_bytes: int = Field(ge=0)
    content_hash: str = Field(min_length=1)
    fetched_at: AwareDatetime