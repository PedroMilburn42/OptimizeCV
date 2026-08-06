"""freehire.dev connector — public JSON API, no HTML parsing. Facet
filters and envelope shape confirmed against the live API.
"""

import os

import httpx
from selectolax.parser import HTMLParser

from rolesherpa.domain.models import JobPosting, SearchMeta, SearchResult

DEFAULT_BASE_URL = "https://freehire.dev"

_FACET_PARAMS = {
    "region": "regions",
    "country": "countries",
    "city": "cities",
    "seniority": "seniority",
    "category": "category",
    "skill": "skills",
    "company": "company_slug",
    "remote": "work_mode",
}


def _strip_html(html: str) -> str:
    return HTMLParser(html).text(strip=True, deep=True)


def _job_from_json(data: dict, *, with_description: bool) -> JobPosting:
    return JobPosting(
        id=data["public_slug"],
        title=data.get("title", ""),
        company=data.get("company", ""),
        location=data.get("location"),
        date=data.get("posted_at"),
        url=data.get("url", ""),
        source="freehire",
        description=_strip_html(data["description"]) if with_description and data.get("description") else None,
    )


class FreehireConnector:
    def __init__(self, client: httpx.Client | None = None, base_url: str | None = None):
        self._client = client or httpx.Client(timeout=15)
        self._base_url = base_url or os.environ.get("FREEHIRE_API_URL", DEFAULT_BASE_URL)

    def search(
        self,
        query: str = "",
        *,
        jobage: int | None = None,
        page: int = 1,
        limit: int = 25,
        **facets: object,
    ) -> SearchResult:
        params: dict[str, object] = {"limit": limit, "offset": (page - 1) * limit, "semantic_ratio": 0}
        if query:
            params["q"] = query
        if jobage is not None:
            params["posted_within_days"] = jobage

        for flag, api_param in _FACET_PARAMS.items():
            if flag in facets and facets[flag] is not None:
                params[api_param] = facets.pop(flag)
        for key, value in facets.items():
            params[key] = value

        response = self._client.get(f"{self._base_url}/api/v1/jobs/search", params=params)
        response.raise_for_status()
        envelope = response.json()
        results = [_job_from_json(job, with_description=False) for job in envelope["data"]]
        return SearchResult(meta=SearchMeta(count=len(results), page=page), results=results)

    def detail(self, job_id: str) -> JobPosting:
        response = self._client.get(f"{self._base_url}/api/v1/jobs/{job_id}")
        if response.status_code == 404:
            raise LookupError(f"freehire job not found: {job_id}")
        response.raise_for_status()
        return _job_from_json(response.json()["data"], with_description=True)
