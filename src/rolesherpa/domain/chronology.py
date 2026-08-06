"""Chronology auditing over career-profile employment entries: gap, overlap,
and impossible-range detection via pure date-interval math. No semantic
judgment here (e.g. "is this overlap normal") - that's rolesherpa-audit's
job, which decides Case A (data exists elsewhere, missing from this
document) vs. Case B (a real gap/overlap, worth an honest interview-prep
note) using these deterministic findings as evidence.
"""

import calendar
import re
from dataclasses import dataclass
from datetime import date, timedelta

_MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

_DASH = r"[–—-]"  # en dash, em dash, hyphen


@dataclass
class ChronologyEntry:
    title: str
    company: str
    start: date
    end: date
    raw: str


@dataclass
class Gap:
    after: ChronologyEntry
    before: ChronologyEntry
    days: int


@dataclass
class Overlap:
    a: ChronologyEntry
    b: ChronologyEntry
    days: int


def parse_month_year(text: str, *, end_of_month: bool = False, today: date | None = None) -> date | None:
    text = text.strip()
    if text.lower() == "present":
        return today or date.today()

    m = re.match(r"^([A-Za-z]{3,9})\s+(\d{4})$", text)
    if m:
        month_name, year_str = m.groups()
        month = _MONTHS.get(month_name[:3].lower())
        if month is None:
            return None
        year = int(year_str)
        if end_of_month:
            last_day = calendar.monthrange(year, month)[1]
            return date(year, month, last_day)
        return date(year, month, 1)

    m = re.match(r"^(\d{4})$", text)
    if m:
        year = int(m.group(1))
        return date(year, 12, 31) if end_of_month else date(year, 1, 1)

    return None


def merge_intervals(ranges: list[tuple[date, date]]) -> list[tuple[date, date]]:
    if not ranges:
        return []
    sorted_ranges = sorted(ranges, key=lambda r: r[0])
    merged: list[list[date]] = [list(sorted_ranges[0])]
    for start, end in sorted_ranges[1:]:
        last = merged[-1]
        if start <= last[1] + timedelta(days=1):
            last[1] = max(last[1], end)
        else:
            merged.append([start, end])
    return [(s, e) for s, e in merged]


def detect_gaps(entries: list[ChronologyEntry], threshold_days: int = 30) -> list[Gap]:
    if len(entries) < 2:
        return []
    ranges = [(e.start, e.end) for e in entries]
    merged = merge_intervals(ranges)
    if len(merged) < 2:
        return []

    gaps = []
    for (_, block_end), (block_start, _) in zip(merged, merged[1:]):
        gap_days = (block_start - block_end).days - 1
        if gap_days > threshold_days:
            after_entry = max((e for e in entries if e.end == block_end), key=lambda e: e.start)
            before_entry = min((e for e in entries if e.start == block_start), key=lambda e: e.end)
            gaps.append(Gap(after=after_entry, before=before_entry, days=gap_days))
    return gaps


def detect_overlaps(entries: list[ChronologyEntry]) -> list[Overlap]:
    overlaps = []
    sorted_entries = sorted(entries, key=lambda e: e.start)
    for i, a in enumerate(sorted_entries):
        for b in sorted_entries[i + 1:]:
            latest_start = max(a.start, b.start)
            earliest_end = min(a.end, b.end)
            overlap_days = (earliest_end - latest_start).days + 1
            if overlap_days > 0:
                overlaps.append(Overlap(a=a, b=b, days=overlap_days))
    return overlaps


def detect_impossible_ranges(entries: list[ChronologyEntry]) -> list[str]:
    return [
        f"{e.title} at {e.company}: end date before start date ({e.raw})"
        for e in entries
        if e.end < e.start
    ]


_TOP_LEVEL_RE = re.compile(
    r"^\*\*(?P<title>[^*]+)\*\*\s*\|\s*(?P<company>[^|]+?)\s*\|\s*"
    r"(?P<start>[^–—]+?)\s*[–—]\s*(?P<end>.+)$",
    re.MULTILINE,
)

_EARLIER_CAREER_RE = re.compile(
    r"^-\s*\*\*(?P<title>[^*]+)\*\*,\s*(?P<company>[^(]+?)\s*"
    rf"\((?P<start>\d{{4}}){_DASH}(?P<end>\d{{4}})",
    re.MULTILINE,
)


def parse_profile_experience(markdown: str, *, today: date | None = None) -> list[ChronologyEntry]:
    entries: list[ChronologyEntry] = []

    for m in _TOP_LEVEL_RE.finditer(markdown):
        start = parse_month_year(m.group("start"), today=today)
        end = parse_month_year(m.group("end"), end_of_month=True, today=today)
        if start is None or end is None:
            continue
        entries.append(
            ChronologyEntry(
                title=m.group("title").strip(),
                company=m.group("company").strip(),
                start=start,
                end=end,
                raw=m.group(0).splitlines()[0].strip(),
            )
        )

    for m in _EARLIER_CAREER_RE.finditer(markdown):
        start = parse_month_year(m.group("start"), today=today)
        end = parse_month_year(m.group("end"), end_of_month=True, today=today)
        if start is None or end is None:
            continue
        entries.append(
            ChronologyEntry(
                title=m.group("title").strip(),
                company=m.group("company").strip(),
                start=start,
                end=end,
                raw=m.group(0).strip(),
            )
        )

    return entries
