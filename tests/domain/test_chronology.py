from datetime import date

from rolesherpa.domain.chronology import (
    ChronologyEntry,
    detect_gaps,
    detect_impossible_ranges,
    detect_overlaps,
    merge_intervals,
    parse_month_year,
    parse_profile_experience,
)


def entry(title, company, start, end):
    return ChronologyEntry(title=title, company=company, start=start, end=end, raw=f"{title} | {company}")


# --- parse_month_year ---

def test_parses_month_year():
    assert parse_month_year("Oct 2024") == date(2024, 10, 1)


def test_parses_month_year_end_of_month():
    assert parse_month_year("Feb 2024", end_of_month=True) == date(2024, 2, 29)


def test_parses_year_only():
    assert parse_month_year("2008") == date(2008, 1, 1)


def test_parses_year_only_end_of_month():
    assert parse_month_year("2008", end_of_month=True) == date(2008, 12, 31)


def test_parses_present_using_supplied_today():
    assert parse_month_year("Present", today=date(2026, 8, 2)) == date(2026, 8, 2)


def test_unparseable_text_returns_none():
    assert parse_month_year("whenever") is None


# --- merge_intervals ---

def test_merge_intervals_keeps_disjoint_ranges_separate():
    ranges = [(date(2020, 1, 1), date(2020, 6, 1)), (date(2021, 1, 1), date(2021, 6, 1))]
    assert merge_intervals(ranges) == ranges


def test_merge_intervals_merges_overlapping_ranges():
    ranges = [(date(2020, 1, 1), date(2020, 6, 1)), (date(2020, 3, 1), date(2020, 9, 1))]
    assert merge_intervals(ranges) == [(date(2020, 1, 1), date(2020, 9, 1))]


def test_merge_intervals_merges_contiguous_ranges():
    ranges = [(date(2020, 1, 1), date(2020, 6, 1)), (date(2020, 6, 2), date(2020, 9, 1))]
    assert merge_intervals(ranges) == [(date(2020, 1, 1), date(2020, 9, 1))]


# --- detect_gaps ---

def test_no_gap_for_contiguous_entries():
    entries = [
        entry("Role A", "Co A", date(2020, 1, 1), date(2020, 6, 1)),
        entry("Role B", "Co B", date(2020, 6, 2), date(2020, 12, 1)),
    ]
    assert detect_gaps(entries) == []


def test_gap_detected_above_threshold():
    entries = [
        entry("Role A", "Co A", date(2020, 1, 1), date(2020, 6, 1)),
        entry("Role B", "Co B", date(2021, 1, 1), date(2021, 6, 1)),
    ]
    gaps = detect_gaps(entries, threshold_days=30)
    assert len(gaps) == 1
    assert gaps[0].after.title == "Role A"
    assert gaps[0].before.title == "Role B"
    assert gaps[0].days > 200


def test_small_gap_under_threshold_not_reported():
    entries = [
        entry("Role A", "Co A", date(2020, 1, 1), date(2020, 6, 1)),
        entry("Role B", "Co B", date(2020, 6, 15), date(2020, 12, 1)),
    ]
    assert detect_gaps(entries, threshold_days=30) == []


def test_concurrent_overlapping_entries_produce_no_false_gap():
    # Associate Professor (2008-2014) overlaps Kestrel IT (2008-2012) and Meridian
    # Consultancy (2007-2008) - the union of coverage is continuous, so no gap
    # should appear between them.
    entries = [
        entry("Developer", "Kestrel IT", date(2002, 1, 1), date(2007, 12, 31)),
        entry("Functional Analyst", "Meridian Consultancy", date(2007, 1, 1), date(2008, 12, 31)),
        entry("Associate Professor", "Delta State University", date(2008, 1, 1), date(2014, 12, 31)),
        entry("Technical Lead", "Kestrel IT", date(2008, 1, 1), date(2012, 12, 31)),
    ]
    assert detect_gaps(entries, threshold_days=30) == []


# --- detect_overlaps ---

def test_overlap_detected_between_two_entries():
    entries = [
        entry("Role A", "Co A", date(2020, 1, 1), date(2020, 12, 31)),
        entry("Role B", "Co B", date(2020, 6, 1), date(2021, 6, 1)),
    ]
    overlaps = detect_overlaps(entries)
    assert len(overlaps) == 1
    assert {overlaps[0].a.title, overlaps[0].b.title} == {"Role A", "Role B"}
    assert overlaps[0].days > 0


def test_no_overlap_for_sequential_entries():
    entries = [
        entry("Role A", "Co A", date(2020, 1, 1), date(2020, 6, 1)),
        entry("Role B", "Co B", date(2020, 6, 2), date(2020, 12, 1)),
    ]
    assert detect_overlaps(entries) == []


# --- detect_impossible_ranges ---

def test_end_before_start_is_impossible():
    entries = [entry("Role A", "Co A", date(2020, 6, 1), date(2020, 1, 1))]
    problems = detect_impossible_ranges(entries)
    assert len(problems) == 1
    assert "Role A" in problems[0]


def test_valid_range_is_not_impossible():
    entries = [entry("Role A", "Co A", date(2020, 1, 1), date(2020, 6, 1))]
    assert detect_impossible_ranges(entries) == []


# --- parse_profile_experience ---

FIXTURE_MARKDOWN = """
## Professional Experience

**Program Manager / Release Manager** | Northwind Systems | Oct 2024 – Present
- Manage things.

**IT Manager** | Bramble Logistics | Apr 2024 – Sep 2024
- Did things.

**Program Manager / Release Manager** | Solent Payments — Global Payments Technology | Mar 2021 – Dec 2023
- Governed releases.

**Earlier career:**
- **Associate Professor**, Delta State University (2008–2014, concurrent with full-time industry roles): teaching.
- **Technical Lead**, Kestrel IT (2008–2012): led development.
- **Functional Analyst**, Meridian Consultancy (2007–2008): analysis.
- **Developer**, Kestrel IT (2002–2007): development.

## Independent Projects
"""


def test_parses_top_level_entries():
    entries = parse_profile_experience(FIXTURE_MARKDOWN, today=date(2026, 8, 2))
    top_level = [e for e in entries if e.company != "Kestrel IT" and "Meridian Consultancy" not in e.company and e.company != "Delta State University"]
    assert len(top_level) == 3
    northwind = next(e for e in top_level if "Northwind" in e.company)
    assert northwind.start == date(2024, 10, 1)
    assert northwind.end == date(2026, 8, 2)  # "Present" resolved to supplied today


def test_parses_earlier_career_bullets():
    entries = parse_profile_experience(FIXTURE_MARKDOWN, today=date(2026, 8, 2))
    prof = next(e for e in entries if e.title == "Associate Professor")
    assert prof.start == date(2008, 1, 1)
    assert prof.end.year == 2014


def test_em_dash_in_company_name_not_confused_with_date_separator():
    entries = parse_profile_experience(FIXTURE_MARKDOWN, today=date(2026, 8, 2))
    solent = next(e for e in entries if "Solent" in e.company)
    assert solent.start == date(2021, 3, 1)
    assert solent.end.year == 2023


def test_parses_real_profile_file_without_crashing():
    from pathlib import Path

    import pytest

    path = Path(__file__).parents[2] / "data/profile/candidate-profile.md"
    if not path.exists():
        pytest.skip("requires a populated data/profile/candidate-profile.md (gitignored, local-only)")
    text = path.read_text()
    entries = parse_profile_experience(text, today=date(2026, 8, 2))
    assert len(entries) >= 8
