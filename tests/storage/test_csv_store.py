from rolesherpa.domain.models import Application
from rolesherpa.storage.csv_store import CSV_HEADER, CsvStore


def _application(**overrides):
    defaults = dict(company="Acme S.A.", role="Data Engineer", status="applied", date="2026-08-01")
    defaults.update(overrides)
    return Application(**defaults)


def test_load_returns_empty_list_when_file_is_missing(tmp_path):
    store = CsvStore(tmp_path / "job_search_tracker.csv")
    assert store.load() == []


def test_append_creates_file_with_header(tmp_path):
    path = tmp_path / "job_search_tracker.csv"
    store = CsvStore(path)

    store.append(_application())

    lines = path.read_text().splitlines()
    assert lines[0] == ",".join(CSV_HEADER)
    assert len(lines) == 2


def test_append_twice_does_not_duplicate_header(tmp_path):
    path = tmp_path / "job_search_tracker.csv"
    store = CsvStore(path)

    store.append(_application(company="Acme S.A."))
    store.append(_application(company="Globex S.A."))

    lines = path.read_text().splitlines()
    assert lines.count(",".join(CSV_HEADER)) == 1
    assert len(lines) == 3


def test_load_round_trips_all_fields(tmp_path):
    store = CsvStore(tmp_path / "job_search_tracker.csv")
    app = Application(
        company="Acme S.A.",
        role="Data Engineer",
        status="interview",
        date="2026-08-01",
        sector="Tech",
        role_type="full_time",
        channel="linkedin",
        contact_person="Jane Recruiter",
        fit_rating=78,
        notes="Strong fit",
        cv_file="cv/main_acme.pdf",
        cover_letter_file="cover_letters/cover_acme_data_engineer.pdf",
        source="https://example.com/jobs/1",
    )

    store.append(app)
    loaded = store.load()

    assert len(loaded) == 1
    assert loaded[0] == app


def test_load_handles_missing_optional_fields_as_none(tmp_path):
    store = CsvStore(tmp_path / "job_search_tracker.csv")
    store.append(_application())

    loaded = store.load()[0]

    assert loaded.sector is None
    assert loaded.fit_rating is None
    assert loaded.notes is None


def test_save_rewrites_the_whole_file(tmp_path):
    store = CsvStore(tmp_path / "job_search_tracker.csv")
    store.append(_application(company="Acme S.A."))
    store.append(_application(company="Globex S.A."))

    store.save([_application(company="OnlyOne S.A.")])

    loaded = store.load()
    assert len(loaded) == 1
    assert loaded[0].company == "OnlyOne S.A."


def test_never_reorders_or_touches_other_rows_on_append(tmp_path):
    store = CsvStore(tmp_path / "job_search_tracker.csv")
    store.append(_application(company="First S.A."))
    store.append(_application(company="Second S.A."))

    loaded = store.load()

    assert [a.company for a in loaded] == ["First S.A.", "Second S.A."]
