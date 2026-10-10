from typing import Protocol
from .sources import RegulatoryDocument, Source
from datetime import UTC, datetime

class Collector(Protocol):
    def collect(self, source: Source) -> list[RegulatoryDocument]:
        ...

class InMemoryCollector:
    def collect(self, source: Source) -> list[RegulatoryDocument]:
        if source.status != "active":
            raise ValueError("Source is not active")
        document = RegulatoryDocument(
            source_id=source.identifier,
            document_id="doc-123",
            title="Example Document",
            document_type="portaria",
            official_reference="BR-123",
            document_url="https://gov.br/legislacao/doc/123/",
            published_at=None,
            collected_at=datetime.now(UTC),
            content_hash="abc123",
        )
        return [document]
