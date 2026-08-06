from pathlib import Path
from urllib.parse import urlparse

import httpx
import pytest

from rolesherpa.connectors.computrabajo import ComputrabajoConnector, parse_detail_html, parse_search_html

FIXTURES = Path(__file__).parent / "fixtures" / "computrabajo"


def test_parse_search_html_extracts_all_cards():
    html = (FIXTURES / "search.html").read_text()
    results = parse_search_html(html)
    assert len(results) > 0


def test_parse_search_html_extracts_expected_fields_for_known_card():
    html = (FIXTURES / "search.html").read_text()
    results = parse_search_html(html)
    job = next(r for r in results if r.id == "AAAA1111BBBB2222CCCC3333DDDD4444")
    assert job.title == "Desarrollador Backend Junior"
    assert job.company == "Ejemplo Software SA"
    assert job.location == "Montevideo, Montevideo"
    assert job.date == "Ayer"
    assert job.source == "computrabajo"
    assert job.url.startswith("https://uy.computrabajo.com/")


def test_parse_detail_html_extracts_description():
    html = (FIXTURES / "detail.html").read_text()
    job = parse_detail_html(
        html,
        job_id="AAAA1111BBBB2222CCCC3333DDDD4444",
        url="https://uy.computrabajo.com/ofertas-de-trabajo/x-AAAA1111BBBB2222CCCC3333DDDD4444",
    )
    assert "Desarrollador Backend Junior" in job.title
    assert job.company == "Ejemplo Software SA"
    assert "Python" in job.description


def test_search_folds_location_into_query_slug():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = request.url
        html = (FIXTURES / "search.html").read_text()
        return httpx.Response(200, text=html, request=request)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    connector = ComputrabajoConnector(client=client)

    result = connector.search(query="programador montevideo", jobage=7)

    path = urlparse(str(captured["url"])).path
    assert path == "/trabajo-de-programador-montevideo"
    assert "pubdate=7" in str(captured["url"])
    assert len(result.results) > 0


def test_search_includes_page_param_when_beyond_first_page():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = request.url
        html = (FIXTURES / "search.html").read_text()
        return httpx.Response(200, text=html, request=request)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    connector = ComputrabajoConnector(client=client)

    connector.search(query="vendedor", page=3)

    assert "p=3" in str(captured["url"])


def test_search_requires_query():
    connector = ComputrabajoConnector(client=httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(200, text="", request=r))))
    with pytest.raises(ValueError):
        connector.search(query="")


def test_detail_fetches_and_parses():
    html = (FIXTURES / "detail.html").read_text()

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=html, request=request)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    connector = ComputrabajoConnector(client=client)

    job = connector.detail("AAAA1111BBBB2222CCCC3333DDDD4444")
    assert job.company == "Ejemplo Software SA"
