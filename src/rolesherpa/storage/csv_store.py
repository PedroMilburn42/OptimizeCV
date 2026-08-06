"""CSV StoragePort adapter for job_search_tracker.csv. append() writes a
single row without rewriting existing ones - never restructures the CSV,
reorders rows, or touches other rows (/outcome, /rank).
"""

import csv
from pathlib import Path

from rolesherpa.domain.models import Application

CSV_HEADER = [
    "date",
    "company",
    "sector",
    "role",
    "role_type",
    "channel",
    "status",
    "contact_person",
    "fit_rating",
    "notes",
    "cv_file",
    "cover_letter_file",
    "source",
]


def _row_to_application(row: dict) -> Application:
    fit_rating = row.get("fit_rating") or ""
    return Application(
        date=row.get("date", ""),
        company=row.get("company", ""),
        sector=row.get("sector") or None,
        role=row.get("role", ""),
        role_type=row.get("role_type") or None,
        channel=row.get("channel") or None,
        status=row.get("status", ""),
        contact_person=row.get("contact_person") or None,
        fit_rating=int(fit_rating) if fit_rating else None,
        notes=row.get("notes") or None,
        cv_file=row.get("cv_file") or None,
        cover_letter_file=row.get("cover_letter_file") or None,
        source=row.get("source") or None,
    )


def _application_to_row(app: Application) -> dict:
    return {
        "date": app.date,
        "company": app.company,
        "sector": app.sector or "",
        "role": app.role,
        "role_type": app.role_type or "",
        "channel": app.channel or "",
        "status": app.status,
        "contact_person": app.contact_person or "",
        "fit_rating": app.fit_rating if app.fit_rating is not None else "",
        "notes": app.notes or "",
        "cv_file": app.cv_file or "",
        "cover_letter_file": app.cover_letter_file or "",
        "source": app.source or "",
    }


class CsvStore:
    def __init__(self, path: Path):
        self._path = Path(path)

    def load(self) -> list[Application]:
        if not self._path.exists():
            return []
        with self._path.open(newline="", encoding="utf-8") as f:
            return [_row_to_application(row) for row in csv.DictReader(f)]

    def append(self, application: Application) -> None:
        is_new = not self._path.exists()
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
            if is_new:
                writer.writeheader()
            writer.writerow(_application_to_row(application))

    def save(self, data: list[Application]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
            writer.writeheader()
            for application in data:
                writer.writerow(_application_to_row(application))
