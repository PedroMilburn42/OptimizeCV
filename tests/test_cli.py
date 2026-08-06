import json
import subprocess
import sys

import pytest

from rolesherpa import cli
from rolesherpa.domain.models import JobPosting, SearchMeta, SearchResult


class FakeConnector:
    def __init__(self):
        self.search_calls = []

    def search(self, query="", **filters):
        self.search_calls.append((query, filters))
        return SearchResult(
            meta=SearchMeta(count=1, page=filters.get("page", 1)),
            results=[
                JobPosting(
                    id="1",
                    title="Data Engineer",
                    company="Acme",
                    location="Montevideo",
                    date="2026-07-01",
                    url="https://example.com/jobs/1",
                    source="fake",
                )
            ],
        )

    def detail(self, job_id):
        if job_id == "missing":
            raise LookupError(f"not found: {job_id}")
        return JobPosting(
            id=job_id,
            title="Data Engineer",
            company="Acme",
            location="Montevideo",
            date="2026-07-01",
            url="https://example.com/jobs/1",
            source="fake",
            description="Build things.",
        )


class ExplodingConnector:
    def search(self, query="", **filters):
        raise RuntimeError("boom")

    def detail(self, job_id):
        raise RuntimeError("boom")


class RejectingConnector:
    def search(self, query="", **filters):
        raise ValueError("location is required")

    def detail(self, job_id):
        raise RuntimeError("unused")


class FakeRegistry:
    def __init__(self, connectors, blocked=None):
        self._connectors = connectors
        self._blocked = blocked or []

    def active_connectors(self):
        return self._connectors

    def blocked_sources(self):
        return self._blocked


def test_search_prints_json_envelope(capsys):
    registry = FakeRegistry({"fake": FakeConnector()})
    exit_code = cli.main(["connectors", "search", "--source", "fake", "--query", "data"], registry=registry)

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["meta"]["count"] == 1
    assert payload["results"][0]["id"] == "1"
    assert payload["results"][0]["title"] == "Data Engineer"
    assert payload["results"][0]["company"] == "Acme"
    assert payload["results"][0]["url"] == "https://example.com/jobs/1"


def test_search_passes_location_jobage_and_filters_through(capsys):
    connector = FakeConnector()
    registry = FakeRegistry({"fake": connector})

    cli.main(
        [
            "connectors",
            "search",
            "--source",
            "fake",
            "--query",
            "data",
            "--location",
            "Montevideo, Uruguay",
            "--jobage",
            "7",
            "--filter",
            "seniority=senior",
        ],
        registry=registry,
    )

    query, filters = connector.search_calls[0]
    assert query == "data"
    assert filters["location"] == "Montevideo, Uruguay"
    assert filters["jobage"] == 7
    assert filters["seniority"] == "senior"


def test_search_table_format(capsys):
    registry = FakeRegistry({"fake": FakeConnector()})
    cli.main(["connectors", "search", "--source", "fake", "--format", "table"], registry=registry)

    out = capsys.readouterr().out
    assert "Data Engineer" in out
    assert "Acme" in out


def test_search_plain_format(capsys):
    registry = FakeRegistry({"fake": FakeConnector()})
    cli.main(["connectors", "search", "--source", "fake", "--limit", "5", "--format", "plain"], registry=registry)

    out = capsys.readouterr().out
    assert "Data Engineer — Acme" in out
    assert "https://example.com/jobs/1" in out


def test_detail_plain_format(capsys):
    registry = FakeRegistry({"fake": FakeConnector()})
    cli.main(["connectors", "detail", "1", "--source", "fake", "--format", "plain"], registry=registry)

    out = capsys.readouterr().out
    assert "Data Engineer — Acme" in out
    assert "Build things." in out


def test_invalid_argument_errors_to_stderr_with_exit_1(capsys):
    registry = FakeRegistry({"fake": RejectingConnector()})
    exit_code = cli.main(["connectors", "search", "--source", "fake"], registry=registry)

    assert exit_code == 1
    out, err = capsys.readouterr()
    assert out == ""
    payload = json.loads(err)
    assert payload["code"] == "INVALID_ARGUMENT"


def test_detail_prints_json(capsys):
    registry = FakeRegistry({"fake": FakeConnector()})
    exit_code = cli.main(["connectors", "detail", "1", "--source", "fake"], registry=registry)

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["id"] == "1"
    assert payload["description"] == "Build things."


def test_unknown_source_errors_to_stderr_with_exit_1(capsys):
    registry = FakeRegistry({"fake": FakeConnector()})
    exit_code = cli.main(["connectors", "search", "--source", "not-real"], registry=registry)

    assert exit_code == 1
    out, err = capsys.readouterr()
    assert out == ""
    payload = json.loads(err)
    assert payload["error"]
    assert payload["code"] == "UNKNOWN_SOURCE"


def test_detail_not_found_errors_to_stderr_with_exit_1(capsys):
    registry = FakeRegistry({"fake": FakeConnector()})
    exit_code = cli.main(["connectors", "detail", "missing", "--source", "fake"], registry=registry)

    assert exit_code == 1
    out, err = capsys.readouterr()
    assert out == ""
    payload = json.loads(err)
    assert payload["code"] == "NOT_FOUND"


def test_connector_exception_errors_to_stderr_with_exit_1(capsys):
    registry = FakeRegistry({"fake": ExplodingConnector()})
    exit_code = cli.main(["connectors", "search", "--source", "fake"], registry=registry)

    assert exit_code == 1
    out, err = capsys.readouterr()
    assert out == ""
    payload = json.loads(err)
    assert payload["code"] == "CONNECTOR_ERROR"


def test_list_prints_active_and_blocked_sources(capsys):
    from rolesherpa.connectors.registry import BlockedSource

    registry = FakeRegistry(
        {"linkedin": FakeConnector(), "computrabajo": FakeConnector()},
        blocked=[BlockedSource(name="buscojobs", blocked_reason="robots.txt disallows Claude-derived agents.")],
    )

    exit_code = cli.main(["connectors", "list"], registry=registry)

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert set(payload["active"]) == {"linkedin", "computrabajo"}
    assert payload["blocked"] == [{"name": "buscojobs", "reason": "robots.txt disallows Claude-derived agents."}]


def test_list_with_no_blocked_sources_returns_empty_list(capsys):
    registry = FakeRegistry({"linkedin": FakeConnector()})

    cli.main(["connectors", "list"], registry=registry)

    payload = json.loads(capsys.readouterr().out)
    assert payload["active"] == ["linkedin"]
    assert payload["blocked"] == []


def _write_postings(path, postings):
    from dataclasses import asdict

    path.write_text(json.dumps([asdict(p) for p in postings]))


def test_dedup_filter_separates_new_from_duplicates(tmp_path, capsys):
    existing = tmp_path / "existing.json"
    candidates = tmp_path / "candidates.json"

    _write_postings(
        existing,
        [
            JobPosting(
                id="1",
                title="Data Engineer",
                company="Acme S.A.",
                url="https://linkedin.com/jobs/1",
                source="linkedin",
            )
        ],
    )
    _write_postings(
        candidates,
        [
            JobPosting(
                id="2",
                title="Different Title Entirely",
                company="Acme S.A.",
                url="https://linkedin.com/jobs/1?utm=x",
                source="computrabajo",
            ),
            JobPosting(
                id="3",
                title="Backend Engineer",
                company="Globex S.A.",
                url="https://computrabajo.com/jobs/9",
                source="computrabajo",
            ),
        ],
    )

    exit_code = cli.main(["dedup", "filter", str(candidates), "--against", str(existing)])

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert [j["id"] for j in payload["new"]] == ["3"]
    assert len(payload["duplicates"]) == 1
    assert payload["duplicates"][0]["candidate"]["id"] == "2"
    assert payload["duplicates"][0]["matched"]["id"] == "1"


def test_dedup_filter_without_against_only_dedupes_within_batch(tmp_path, capsys):
    candidates = tmp_path / "candidates.json"
    _write_postings(
        candidates,
        [
            JobPosting(id="a", title="Data Engineer", company="Acme S.A.", url="https://x.com/1", source="linkedin"),
            JobPosting(id="b", title="Sales Manager", company="Globex S.A.", url="https://x.com/2", source="linkedin"),
        ],
    )

    exit_code = cli.main(["dedup", "filter", str(candidates)])

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert len(payload["new"]) == 2
    assert payload["duplicates"] == []


def test_dedup_filter_missing_file_errors_to_stderr_with_exit_1(tmp_path, capsys):
    missing = tmp_path / "does-not-exist.json"

    exit_code = cli.main(["dedup", "filter", str(missing)])

    assert exit_code == 1
    out, err = capsys.readouterr()
    assert out == ""
    payload = json.loads(err)
    assert payload["code"] == "DEDUP_ERROR"


@pytest.mark.integration
def test_real_entrypoint_against_a_live_connector():
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "rolesherpa.cli",
            "connectors",
            "search",
            "--source",
            "computrabajo",
            "--query",
            "programador montevideo",
            "--jobage",
            "30",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload["meta"]["count"] > 0
    assert payload["results"][0]["title"]
