import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import httpx
import pytest

from rolesherpa.connectors.freehire import FreehireConnector

FIXTURES = Path(__file__).parent / "fixtures" / "freehire"


def _handler_for(fixture_name, status_code=200, capture=None):
    payload = json.loads((FIXTURES / fixture_name).read_text())

    def handler(request: httpx.Request) -> httpx.Response:
        if capture is not None:
            capture["url"] = request.url
        return httpx.Response(status_code, json=payload, request=request)

    return handler


def test_search_parses_results_and_meta():
    client = httpx.Client(transport=httpx.MockTransport(_handler_for("search.json")))
    connector = FreehireConnector(client=client)

    result = connector.search(query="python")

    assert result.meta.count == 3
    assert len(result.results) == 3
    first = result.results[0]
    assert first.id == "python-example-tech-abc123"
    assert first.title == "Python"
    assert first.company == "Example Tech"
    assert first.source == "freehire"
    assert first.date == "2026-07-31T00:00:00Z"


def test_search_sends_facet_params():
    captured = {}
    client = httpx.Client(transport=httpx.MockTransport(_handler_for("search.json", capture=captured)))
    connector = FreehireConnector(client=client)

    connector.search(query="go", country=["DE", "GB"], remote="remote", jobage=14, page=2, limit=10)

    params = parse_qs(urlparse(str(captured["url"])).query)
    assert params["q"] == ["go"]
    assert params["countries"] == ["DE", "GB"]
    assert params["work_mode"] == ["remote"]
    assert params["posted_within_days"] == ["14"]
    assert params["limit"] == ["10"]
    assert params["offset"] == ["10"]


def test_search_passes_through_arbitrary_facet_escape_hatch():
    captured = {}
    client = httpx.Client(transport=httpx.MockTransport(_handler_for("search.json", capture=captured)))
    connector = FreehireConnector(client=client)

    connector.search(query="go", salary_min=100000)

    params = parse_qs(urlparse(str(captured["url"])).query)
    assert params["salary_min"] == ["100000"]


def test_detail_strips_html_description():
    client = httpx.Client(transport=httpx.MockTransport(_handler_for("detail.json")))
    connector = FreehireConnector(client=client)

    job = connector.detail("python-example-tech-abc123")

    assert job.id == "python-example-tech-abc123"
    assert "<" not in job.description
    assert "Software Requirements" in job.description


def test_detail_raises_lookup_error_on_404():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"error": "not found"}, request=request)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    connector = FreehireConnector(client=client)

    with pytest.raises(LookupError):
        connector.detail("not-a-real-slug")


def test_base_url_override(monkeypatch):
    monkeypatch.setenv("FREEHIRE_API_URL", "http://localhost:8080")
    captured = {}
    client = httpx.Client(transport=httpx.MockTransport(_handler_for("search.json", capture=captured)))
    connector = FreehireConnector(client=client)

    connector.search(query="x")

    assert str(captured["url"]).startswith("http://localhost:8080")
