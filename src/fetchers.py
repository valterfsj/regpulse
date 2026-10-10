from typing import Protocol
from .sources import RegulatoryDocument, Source, FetchedContent
from pydantic import HttpUrl
from datetime import datetime, UTC

class Fetcher(Protocol):
    def fetch(self, url: HttpUrl) -> FetchedContent:
        ...

class StaticFetcher:
    def __init__(self, content: FetchedContent) -> None:
        self.content = content

    def fetch(self, url: HttpUrl) -> FetchedContent:
        return self.content

class HttpCollector:
    def __init__(self, fetcher: Fetcher) -> None:
        self.fetcher = fetcher

    def collect(self, source: Source) -> list[RegulatoryDocument]:
        if source.status != "active":
            raise ValueError("Source is not active")
        data = self.fetcher.fetch(source.url)
        if not data.body:
            raise ValueError("No documents fetched from the source URL")
        document = RegulatoryDocument(
            source_id=source.identifier,
            document_id="static-fetched-document-1",
            title="Static fetched document",
            document_type="outro",
            document_url=source.url,
            published_at=None,
            collected_at=datetime.now(UTC),
            content_hash=None,
        )
        return [document]