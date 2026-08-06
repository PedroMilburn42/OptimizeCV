"""The reference implementation's scraper skipped expired/closed postings
and out-of-range postings before presenting results, and flagged undated
postings as "date unknown" rather than silently including or excluding
them. RoleSherpa's port dropped all three safeguards.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRAPE_SKILL = REPO_ROOT / ".agents" / "skills" / "rolesherpa-scrape" / "SKILL.md"
SEARCH_QUERIES_TEMPLATE = REPO_ROOT / "templates" / "profile" / "search-queries.md"


def test_scrape_skips_expired_or_closed_postings_before_presenting():
    text = SCRAPE_SKILL.read_text().lower()
    assert "closed" in text
    assert "expired" in text or "deadline" in text


def test_scrape_filters_by_configured_location_range_before_presenting():
    text = SCRAPE_SKILL.read_text().lower()
    assert "location tier" in text or "commute" in text or "out of range" in text or "outside" in text


def test_search_queries_template_has_a_date_filter_section():
    text = SEARCH_QUERIES_TEMPLATE.read_text()
    assert "Date Filter" in text


def test_scrape_skill_documents_the_date_unknown_flag():
    text = SCRAPE_SKILL.read_text().lower()
    assert "date unknown" in text
