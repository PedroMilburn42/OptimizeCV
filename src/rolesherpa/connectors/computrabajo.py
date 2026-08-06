"""Computrabajo Uruguay connector — public, server-rendered HTML, scoped
to uy.computrabajo.com. Parsing anchors reconfirmed live against the
site during this port.
"""

from urllib.parse import quote

import httpx
from selectolax.parser import HTMLParser

from rolesherpa.domain.models import JobPosting, SearchMeta, SearchResult

BASE_URL = "https://uy.computrabajo.com"

_DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}


def _query_slug(query: str) -> str:
    return "-".join(quote(token.lower()) for token in query.split())


def parse_search_html(html: str) -> list[JobPosting]:
    tree = HTMLParser(html)
    postings = []
    for card in tree.css("article.box_offer"):
        job_id = card.attributes.get("data-id", "")
        link = card.css_first("a.js-o-link")
        company = card.css_first("[offer-grid-article-company-url]")
        location = card.css_first("p.fs16.fc_base.mt5 span.mr10")
        date = card.css_first("p.fs13.fc_aux.mt15")
        href = link.attributes.get("href", "") if link else ""
        postings.append(
            JobPosting(
                id=job_id,
                title=link.text(strip=True) if link else "",
                company=company.text(strip=True) if company else "",
                location=location.text(strip=True) if location else None,
                date=date.text(strip=True) if date else None,
                url=f"{BASE_URL}{href}" if href.startswith("/") else href,
                source="computrabajo",
            )
        )
    return postings


def parse_detail_html(html: str, job_id: str, url: str) -> JobPosting:
    tree = HTMLParser(html)
    title = tree.css_first("h1.box_detail")
    company_location = None
    if title is not None:
        node = title.next
        while node is not None and node.tag != "p":
            node = node.next
        company_location = node
    company, _, location = (company_location.text(strip=True).partition(" - ") if company_location else ("", "", ""))

    description_parts = []
    heading = tree.css_first("h3")
    if heading is not None:
        node = heading.next
        while node is not None:
            if node.tag in ("p", "ul"):
                description_parts.append(node.text(strip=True, deep=True))
            node = node.next

    return JobPosting(
        id=job_id,
        title=title.text(strip=True) if title else "",
        company=company,
        location=location or None,
        url=url,
        source="computrabajo",
        description="\n".join(part for part in description_parts if part) or None,
    )


class ComputrabajoConnector:
    def __init__(self, client: httpx.Client | None = None):
        self._client = client or httpx.Client(headers=_DEFAULT_HEADERS, timeout=15)

    def search(
        self,
        query: str = "",
        *,
        jobage: int | None = None,
        page: int = 1,
        **filters: object,
    ) -> SearchResult:
        if not query:
            raise ValueError("Computrabajo search requires a query (fold location into it)")

        url = f"{BASE_URL}/trabajo-de-{_query_slug(query)}"
        params: dict[str, object] = {}
        if page > 1:
            params["p"] = page
        if jobage is not None:
            params["pubdate"] = jobage

        response = self._client.get(url, params=params)
        response.raise_for_status()
        results = parse_search_html(response.text)
        return SearchResult(meta=SearchMeta(count=len(results), page=page), results=results)

    def detail(self, job_id: str) -> JobPosting:
        url = f"{BASE_URL}/ofertas-de-trabajo/oferta-de-trabajo-de-oferta-{job_id}"
        response = self._client.get(url)
        response.raise_for_status()
        return parse_detail_html(response.text, job_id=job_id, url=url)
