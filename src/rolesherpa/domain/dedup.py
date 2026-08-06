"""Job-posting deduplication: canonical URL hash first, then fuzzy
company+title+description matching (design.md D5). Company-name
normalization strips Uruguay legal suffixes (S.A., S.R.L., S.A.S, Ltda).
"""

import hashlib
import re
import unicodedata
from difflib import SequenceMatcher
from urllib.parse import urlparse

from rolesherpa.domain.models import JobPosting

_UY_LEGAL_SUFFIX_PATTERNS = [
    r"\bs\.?\s*a\.?\s*s\.?\b",  # S.A.S.
    r"\bs\.?\s*r\.?\s*l\.?\b",  # S.R.L.
    r"\bs\.?\s*a\.?\b",  # S.A.
    r"\bltda\.?\b",  # Ltda.
]

TITLE_SIMILARITY_THRESHOLD = 0.85
DESCRIPTION_SIMILARITY_THRESHOLD = 0.6


def normalize_company_name(name: str) -> str:
    normalized = unicodedata.normalize("NFKD", name.lower())
    normalized = "".join(c for c in normalized if not unicodedata.combining(c))
    normalized = re.sub(r"\(.*?\)", "", normalized)
    normalized = re.sub(r",.*$", "", normalized)
    for pattern in _UY_LEGAL_SUFFIX_PATTERNS:
        normalized = re.sub(pattern, "", normalized)
    normalized = re.sub(r"[^a-z0-9]", "", normalized)
    return normalized.strip()


def canonical_key(url: str) -> str:
    parsed = urlparse(url)
    normalized = f"{parsed.netloc.lower()}{parsed.path.lower().rstrip('/')}"
    return hashlib.sha256(normalized.encode()).hexdigest()


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def is_likely_duplicate(a: JobPosting, b: JobPosting) -> bool:
    if canonical_key(a.url) == canonical_key(b.url):
        return True

    if normalize_company_name(a.company) != normalize_company_name(b.company):
        return False

    if _similarity(a.title, b.title) < TITLE_SIMILARITY_THRESHOLD:
        return False

    if a.description is None or b.description is None:
        return False

    return _similarity(a.description, b.description) >= DESCRIPTION_SIMILARITY_THRESHOLD


def filter_new(
    candidates: list[JobPosting], existing: list[JobPosting]
) -> tuple[list[JobPosting], list[tuple[JobPosting, JobPosting]]]:
    """Split candidates into (new, duplicates) against `existing` plus
    each other, so a batch that cross-posts the same role twice is also
    caught (scrape/SKILL.md: dedup within one run, not just against
    seen_jobs.json)."""
    new: list[JobPosting] = []
    duplicates: list[tuple[JobPosting, JobPosting]] = []

    for candidate in candidates:
        match = next(
            (known for known in [*existing, *new] if is_likely_duplicate(candidate, known)),
            None,
        )
        if match is not None:
            duplicates.append((candidate, match))
        else:
            new.append(candidate)

    return new, duplicates
