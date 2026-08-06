"""Shared value types for job postings, search results, applications, and
document verification. Plain dataclasses — behavior lives in dedup.py,
documents/, and the connectors, not here.
"""

from dataclasses import dataclass, field


@dataclass
class JobPosting:
    id: str
    title: str
    company: str
    url: str
    source: str
    location: str | None = None
    date: str | None = None
    description: str | None = None


@dataclass
class SearchMeta:
    count: int
    page: int = 1


@dataclass
class SearchResult:
    meta: SearchMeta
    results: list[JobPosting] = field(default_factory=list)


@dataclass
class Application:
    company: str
    role: str
    status: str
    date: str
    sector: str | None = None
    role_type: str | None = None
    channel: str | None = None
    contact_person: str | None = None
    fit_rating: int | None = None
    notes: str | None = None
    cv_file: str | None = None
    cover_letter_file: str | None = None
    source: str | None = None


@dataclass
class VerificationResult:
    passed: bool
    page_count: int | None = None
    expected_pages: int | None = None
    max_pages: int | None = None
    text_length: int = 0
    missing_keywords: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
