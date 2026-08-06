"""PDF verification: page count, ATS text-layer extraction, keyword
coverage - all via pypdf, no external poppler-utils dependency (design.md
D6 — avoids shelling out to pdfinfo/pdftotext).

Keyword coverage is informational, not a pass/fail gate (document-pipeline
spec.md): a missing keyword is reported but never fails verification on
its own, since keyword stuffing to force a pass would defeat the point.
"""

from io import BytesIO

from pypdf import PdfReader

from rolesherpa.domain.models import VerificationResult


def _normalize(text: str) -> str:
    return " ".join(text.split())


def verify(
    pdf: bytes,
    expected_pages: int | None = None,
    max_pages: int | None = None,
    min_chars: int = 1,
    required_text: tuple[str, ...] = (),
) -> VerificationResult:
    reader = PdfReader(BytesIO(pdf))
    page_count = len(reader.pages)
    text = _normalize(" ".join(page.extract_text() or "" for page in reader.pages))

    errors = []
    if max_pages is not None:
        lower = expected_pages if expected_pages is not None else 1
        if not (lower <= page_count <= max_pages):
            target = f"{lower} page(s)" if lower == max_pages else f"{lower}-{max_pages} page(s)"
            errors.append(f"expected {target}, found {page_count}")
    elif expected_pages is not None and page_count != expected_pages:
        errors.append(f"expected {expected_pages} page(s), found {page_count}")
    if len(text) < min_chars:
        errors.append(f"text layer has {len(text)} character(s); expected at least {min_chars}")

    missing_keywords = [kw for kw in required_text if _normalize(kw) not in text]

    return VerificationResult(
        passed=not errors,
        page_count=page_count,
        expected_pages=expected_pages,
        max_pages=max_pages,
        text_length=len(text),
        missing_keywords=missing_keywords,
        errors=errors,
    )
