"""LinkedIn jobs-guest connector — public, unauthenticated endpoints.
Personal use only; keep volume low. Parsing anchors reconfirmed live
against the site during this port (design.md Migration Plan step 1).
"""

import httpx
from selectolax.parser import HTMLParser

from rolesherpa.domain.models import JobPosting, SearchMeta, SearchResult

SEARCH_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
DETAIL_URL = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
PAGE_SIZE = 10

_DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}


def _job_id_from_urn(urn: str) -> str:
    return urn.rsplit(":", 1)[-1]


def parse_search_html(html: str) -> list[JobPosting]:
    tree = HTMLParser(html)
    postings = []
    for card in tree.css("div.base-card[data-entity-urn]"):
        job_id = _job_id_from_urn(card.attributes.get("data-entity-urn", ""))
        link = card.css_first("a.base-card__full-link")
        title = card.css_first("h3.base-search-card__title")
        company = card.css_first("h4.base-search-card__subtitle a")
        location = card.css_first("span.job-search-card__location")
        date = card.css_first("time.job-search-card__listdate")
        postings.append(
            JobPosting(
                id=job_id,
                title=title.text(strip=True) if title else "",
                company=company.text(strip=True) if company else "",
                location=location.text(strip=True) if location else None,
                date=date.attributes.get("datetime") if date else None,
                url=link.attributes.get("href", "") if link else "",
                source="linkedin",
            )
        )
    return postings


def parse_detail_html(html: str, job_id: str, url: str) -> JobPosting:
    tree = HTMLParser(html)
    title = tree.css_first("h2.top-card-layout__title")
    company = tree.css_first("a.topcard__org-name-link")
    location = tree.css_first("span.topcard__flavor--bullet")
    description = tree.css_first("div.show-more-less-html__markup")
    return JobPosting(
        id=job_id,
        title=title.text(strip=True) if title else "",
        company=company.text(strip=True) if company else "",
        location=location.text(strip=True) if location else None,
        url=url,
        source="linkedin",
        description=description.text(strip=True, deep=True) if description else None,
    )


class LinkedInConnector:
    def __init__(self, client: httpx.Client | None = None):
        self._client = client or httpx.Client(headers=_DEFAULT_HEADERS, timeout=15)

    def search(
        self,
        query: str = "",
        *,
        location: str,
        jobage: int | None = None,
        page: int = 1,
        **filters: object,
    ) -> SearchResult:
        if not location:
            raise ValueError("LinkedIn search requires an explicit location")

        params = {
            "keywords": query,
            "location": location,
            "start": (page - 1) * PAGE_SIZE,
        }
        if jobage is not None:
            params["f_TPR"] = f"r{jobage * 86400}"

        response = self._client.get(SEARCH_URL, params=params)
        response.raise_for_status()
        results = parse_search_html(response.text)
        return SearchResult(meta=SearchMeta(count=len(results), page=page), results=results)

    def detail(self, job_id: str) -> JobPosting:
        url = DETAIL_URL.format(job_id=job_id)
        response = self._client.get(url)
        response.raise_for_status()
        return parse_detail_html(response.text, job_id=job_id, url=url)
