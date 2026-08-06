---
name: rolesherpa-scrape
version: 1.0.0
description: >
  Finds new job postings across the installed portal connectors, dedupes
  against previous runs and the tracker, and presents new matches with a
  quick fit signal. Always reports which portals were not searched and
  why. Triggers on: job scrape, find jobs, search jobs, new jobs, job
  search, scrape jobs, /rolesherpa-scrape
allowed-tools: Read, Write, Bash(python -m rolesherpa.cli connectors *), Bash(python -m rolesherpa.cli dedup *), AskUserQuestion
---

# Scrape — Find New Job Postings

## Context and role

You are running a search across every enabled job-source connector,
using the deterministic `rolesherpa` CLI for every fetch and every
dedup decision — never re-derive dedup logic in prose, and never
fabricate a posting that didn't come back from an actual CLI call.

## Task

### Step 0 — load state

1. `python -m rolesherpa.cli connectors list` — this is also what
   drives Step 5's mandatory "not searched" section; keep the blocked
   list from this call, don't re-derive it from `config/sources.yaml`
   by hand.
2. Read `data/seen_jobs.json` (if missing, treat as `{"seen": {}}`).
3. Read `data/job_search_tracker.csv` (if missing, treat as no rows) to build the exclusion set of already-applied company+role pairs.
4. Read `data/profile/search-queries.md` for the search strategy. If it's still unpopulated placeholders, stop and point the user at `rolesherpa-setup/SKILL.md`.

### Step 1 — search each active connector

By default run the top 3 priority query categories from
`data/profile/search-queries.md`; run all categories if the user said "broad"; if
the user gave a focus area, prioritize that category's queries.

For each connector in `connectors list`'s `active` array, translate the
relevant query terms into that connector's flags (see its module
docstring under `src/rolesherpa/connectors/` — don't guess flags) and
run:

```
python -m rolesherpa.cli connectors search --source <name> --query "<terms>" [--location "<place>"] --jobage 14 --limit 20 --format json
```

**Language matters, not just terms.** Computrabajo Uruguay is a
Spanish-only market — an English query (`"data engineer montevideo"`)
returns zero results even when Spanish-language postings for that
exact role exist; use the Spanish equivalent (`"ingeniero de datos
montevideo"`). LinkedIn and Freehire tolerate English queries in
Uruguay. Confirmed empirically during integration testing — this
isn't a guess.

Run these in parallel across connectors where the host supports it. If
a connector call exits non-zero, log the error and continue with the
others — one portal failing never aborts the run.

### Step 2 — fetch detail for promising results

Pre-filter by title/snippet before spending a `detail` call. For jobs
worth a closer look:

```
python -m rolesherpa.cli connectors detail <id> --source <name> --format json
```

### Step 3 — dedup

Combine every fetched result (not just the promising ones) into one
JSON array file, then run:

```
python -m rolesherpa.cli dedup filter <this-run.json> --against <previous-seen.json>
```

where `<previous-seen.json>` is `data/seen_jobs.json`'s stored postings
converted to the same array shape. Anything reported as a duplicate is
already seen — don't present it. Anything in `job_search_tracker.csv`'s
exclusion set (Step 0.3) is also excluded, even if `dedup filter` calls
it new (the CLI doesn't know about the tracker).

Before presenting, also exclude:
- Postings whose title/description text marks them closed or past their
  application deadline — never present a listing the user can't
  actually apply to.
- Postings whose location falls in `data/profile/search-queries.md`'s "Too far /
  excluded" location tier.

If a posting's date can't be determined at all, keep it but mark it
"date unknown" in Step 5's table — never silently drop or silently
include it as if the date were known.

### Step 4 — quick fit signal

For each genuinely new job, a rapid signal only — not the full
`04-job-evaluation.md` evaluation, which is `rolesherpa-apply/SKILL.md`'s job:

- **High** — role directly involves core skills from `data/profile/candidate-profile.md`
- **Medium** — role is adjacent to recorded experience
- **Low** — role requires skills the profile doesn't show

### Step 5 — persist and present

1. Update `data/seen_jobs.json` (`Write`/`Edit`) with every fetched job (new and duplicate), adding entries under `"seen"` keyed by the connector's `id`: `{"title", "company", "url", "first_seen": "<today>", "fit": "high|medium|low", "status": "new"}`. Never drop `rank_score`/`rank_verdict`/`rank_date` fields on entries `rolesherpa-rank/SKILL.md` already scored.
2. Present a table of new jobs sorted by fit (high first), columns: fit, title, company, location, deadline if known, URL.
3. **Always** print a "Portals not included in this search" line listing every entry from `connectors list`'s `blocked` array with its reason — even when every active connector ran cleanly. Never let the output imply full market coverage.
4. For each high/medium-fit job, add two LinkedIn people-search links (URL-encoded `"<Company> recruiter"` and `"<Company> <role keyword>"`) as referral/warm-intro starting points — links only, never scrape or fetch LinkedIn people-search results.

### Step 6 — offer next steps

Ask if the user wants any job evaluated in full (hands off to
`rolesherpa-apply/SKILL.md`). If 8+ new jobs were found, suggest `rolesherpa-rank/SKILL.md`
instead of manually reading a long table.

## Quality criteria

- Every presented job traces to an actual CLI `search`/`detail` call — nothing invented.
- Dedup always runs before presentation; the tracker's exclusion set is always honored even where `dedup filter` alone wouldn't catch it.
- The "not included" section appears on every single run, unconditionally.
- A connector failure narrows the run; it never crashes it.

## Output format

See Step 5 — table + not-included section + referral links block, in
that order.

## Final check

Before presenting, re-read the blocked list from Step 0.1 and confirm
the printed "not included" section names every one of them by name and
reason — not a paraphrase, not "some portals were skipped."
