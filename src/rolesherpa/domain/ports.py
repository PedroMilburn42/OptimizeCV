"""Ports the core depends on instead of any specific connector, storage
format, or rendering library (design.md D2)."""

from typing import Protocol

from rolesherpa.domain.models import JobPosting, SearchResult


class JobSourcePort(Protocol):
    def search(self, query: str, **filters: object) -> SearchResult: ...
    def detail(self, job_id: str) -> JobPosting: ...


class StoragePort(Protocol):
    def load(self) -> dict | list: ...
    def save(self, data: dict | list) -> None: ...


class DocumentRendererPort(Protocol):
    def render(self, html: str) -> bytes: ...
