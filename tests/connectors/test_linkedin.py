from pathlib import Path
from urllib.parse import parse_qs, urlparse

import httpx
import pytest

from rolesherpa.connectors.linkedin import LinkedInConnector, parse_detail_html, parse_search_html

FIXTURES = Path(__file__).parent / "fixtures" / "linkedin"


def test_parse_search_html_extracts_all_cards():
    html = (FIXTURES / "search.html").read_text()
    results = parse_search_html(html)
    assert len(results) > 0


def test_parse_search_html_extracts_expected_fields_for_known_card():
    html = (FIXTURES / "search.html").read_text()
    results = parse_search_html(html)
    job = next(r for r in results if r.id == "1111111111")
    assert job.title == "Data Engineer"
    assert job.company == "Example Tech Inc"
    assert job.location == "Montevideo, Uruguay"
    assert job.date == "2026-07-24"
    assert "1111111111" in job.url
    assert job.source == "linkedin"


def test_parse_detail_html_extracts_description():
    html = (FIXTURES / "detail.html").read_text()
    job = parse_detail_html(html, job_id="1111111111", url="https://example.com/jobs/view/1111111111")
    assert job.title == "Data Engineer"
    assert job.company == "Example Tech Inc"
    assert job.location == "Montevideo, Uruguay"
    assert "Data Engineer" in job.description
    assert "<" not in job.description or "<strong>" not in job.description


def _mock_client(fixture_name):
    html = (FIXTURES / fixture_name).read_text()

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=html, request=request)

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_search_sends_expected_query_params_and_returns_results():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = request.url
        html = (FIXTURES / "search.html").read_text()
        return httpx.Response(200, text=html, request=request)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    connector = LinkedInConnector(client=client)

    result = connector.search(query="data engineer", location="Montevideo, Uruguay", jobage=30, page=2)

    params = parse_qs(urlparse(str(captured["url"])).query)
    assert params["keywords"] == ["data engineer"]
    assert params["location"] == ["Montevideo, Uruguay"]
    assert params["start"] == ["10"]
    assert "f_TPR" in params
    assert result.meta.count == len(result.results)
    assert len(result.results) > 0


def test_search_requires_location():
    connector = LinkedInConnector(client=_mock_client("search.html"))
    with pytest.raises(ValueError):
        connector.search(query="data engineer", location="")


def test_detail_fetches_and_parses():
    connector = LinkedInConnector(client=_mock_client("detail.html"))
    job = connector.detail("1111111111")
    assert job.id == "1111111111"
    assert job.company == "Example Tech Inc"
