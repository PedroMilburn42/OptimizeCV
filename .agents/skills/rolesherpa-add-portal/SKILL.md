---
name: rolesherpa-add-portal
version: 1.0.0
description: >
  Scaffolds a new job-portal connector outside the three shipped in v1
  (LinkedIn, Freehire, Computrabajo Uruguay) - investigates the portal,
  generates a JobSourcePort implementation with tests, and requires a
  live test pass before registering it. Triggers on: add a job portal,
  new job board, add a connector, /rolesherpa-add-portal
allowed-tools: Read, Write, Edit, WebFetch, Bash(curl *), Bash(uv run pytest *), Bash(python -m rolesherpa.cli connectors *)
---

# Add Portal — Scaffold a New Job-Source Connector

## Context and role

The three shipped connectors (LinkedIn, Freehire, Computrabajo Uruguay)
are the confirmed v1 set — this skill exists to extend *past* that set
for a market or board RoleSherpa doesn't cover yet, not to reintroduce
BuscoJobs, Indeed UY, or Get on Board (`config/sources.yaml`'s blocked
entries exist for documented, investigated reasons — see their
`blocked_reason`; don't route around them here).

`$ARGUMENTS` may contain `--list`, a portal URL, or nothing.

## Task

### Step 0 — parse arguments

`--list` → run `python -m rolesherpa.cli connectors list`, print it,
stop. A URL → carry it into Step 1. Otherwise start the interview.

### Step 1 — interview

Ask what `$ARGUMENTS` didn't already answer:

1. **Portal URL.**
2. **Connector name** — snake_case, e.g. `seek`, `stepstone`. Must not collide with an existing module under `src/rolesherpa/connectors/`.
3. **Market and language** — which country/region, what language its postings use.
4. **A realistic test query** — used for the mandatory live test in Step 4.

### Step 2 — investigate before writing any code

Do reconnaissance first — never generate a parser from a guess.

1. Load the portal's search page; identify the search endpoint, query parameter, and any location/recency/pagination parameters. **Prefer a JSON API** if one backs the site (check for `/api/` XHR calls in the page); otherwise plan to parse server-rendered HTML.
2. Fetch one real search response for the test query. Identify the per-result fields: id, title, company, location, posting date, URL. For HTML, note the anchoring class names/attributes; for JSON, note the field paths.
3. Find the detail-page pattern — where the full description, deadline, and apply link live.
4. **Check access:**
   - Fetch `robots.txt`. If the search/detail paths are disallowed, tell the user plainly and let them decide for personal use — if they proceed, the generated connector's docstring must carry a prominent personal-use-only warning.
   - If the portal requires login to view listings, **stop** — this pattern only works on public pages. Suggest checking for an official API instead.
   - Check the portal's Terms of Service for a clause prohibiting automated access/scraping — robots.txt being silent or permissive doesn't mean the ToS allow it. If the ToS prohibit it, **decline to scaffold a connector** and tell the user why.

Record everything found — you'll need it for Step 3 and for the
connector's own docstring (the equivalent of a `url-reference.md`, so a
future maintainer knows what to update if the markup changes).

### Step 3 — scaffold (test-first)

**Canonical reference:** read whichever of `src/rolesherpa/connectors/{linkedin,freehire,computrabajo}.py`
matches the new portal's shape — `freehire.py` for a JSON API,
`linkedin.py` or `computrabajo.py` for HTML. Copy the *architecture*
(a `JobSourcePort` implementation with `search`/`detail`, pure parsing
functions separate from the HTTP fetch, `httpx.Client` injected for
testability), never the source-specific parsing logic.

1. Write `tests/connectors/test_<name>.py` first, against real fixture HTML/JSON saved under `tests/connectors/fixtures/<name>/` (fetched live in Step 2) — parsing tests before any implementation exists, per this repo's TDD discipline.
2. Implement `src/rolesherpa/connectors/<name>.py`: a `<Name>Connector` class implementing `JobSourcePort` (`search`/`detail`), pure `parse_search_*`/`parse_detail_*` functions for the HTML case, and a module docstring recording the endpoints/parameters/quirks from Step 2.
3. Add an entry to `config/sources.yaml`: `enabled: true`, `module: rolesherpa.connectors.<name>:<Name>Connector`.

### Step 4 — mandatory live test (never skip)

1. `uv run pytest tests/connectors/test_<name>.py -q` — must pass against the fixtures.
2. Run the connector's `search()` with the test query against the **real live endpoint** (not the fixture) and confirm real, complete results — non-null id/title/company/url, resolvable URLs, parseable dates. Fix and re-run until clean; markup assumptions from Step 2 routinely miss quirks that only show up live.
3. Run `detail()` on one real result's id and confirm the description is readable text.
4. `python -m rolesherpa.cli connectors list` — confirm the new connector appears under `active`.
5. Keep volume low during iteration — a handful of requests, not a crawl.

Do not proceed to Step 5 until search, detail, and the test suite all pass.

### Step 5 — offer to wire into search

Ask whether to add the new portal to `data/profile/search-queries.md`'s
priority tiers. `rolesherpa-scrape/SKILL.md` picks up any `enabled: true` connector
automatically via `connectors list` — no other wiring is needed.

### Step 6 — confirm

Summarize: files created, live test results (result count, one detail
verified), and the personal-use warning if Step 2 found access
restrictions.

## Quality criteria

- Never scaffolds a connector for an auth-walled portal.
- robots.txt/ToS restrictions are surfaced to the user, never silently bypassed.
- Nothing is registered without a passing live test against the real endpoint — fixtures alone are not enough.
- The new connector's docstring records the endpoints/parsing anchors well enough for a future maintainer to update it when markup changes.

## Output format

See Step 6.

## Final check

Before confirming, re-run `python -m rolesherpa.cli connectors search --source <name> --query "<test query>"` one more time against the live endpoint and confirm it still returns results — not just what Step 4 showed a few edits ago.
