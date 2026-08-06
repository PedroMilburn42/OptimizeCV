---
name: rolesherpa-outcome
version: 1.0.0
description: >
  Records what happened to an application - progress updates and final
  resolutions - into the tracker and the per-application archive.
  Triggers on: log outcome, record application result, update
  application status, got an interview, got rejected, got an offer,
  /rolesherpa-outcome
allowed-tools: Read, Write, WebFetch
---

# Outcome — Record an Application's Result

## Context and role

This skill writes data; it never interprets it. `rolesherpa-setup/SKILL.md` (Path
A) later mines what's written here to calibrate the fit framework and
surface STAR candidates — duplicating that logic here would race it, so
don't.

## Task

### Step 0 — resolve the application

`$ARGUMENTS` may be empty (list open applications, ask which) or a
company name, optionally with a role (match case-insensitively on
`data/job_search_tracker.csv`; several matches → list and ask; no
match → this was applied outside the workflow, collect company, role,
date, channel, and posting URL and add a tracker row via `CsvStore`).

Once the company/role are known, locate the existing application
folder by globbing `data/applications/<company_slug>-<role_slug>-*/`
(slugs are lowercase, underscores for internal word separation — the
same convention `rolesherpa-apply/SKILL.md` used to create it).
Several matches (re-applied to the same role later) → list dates and
ask. No match (applied outside `rolesherpa-apply/SKILL.md`, so no
folder was ever created) → create
`data/applications/<company_slug>-<role_slug>-<YYMMDD>/` now, using
today's date, and note in Step 5 that no draft files exist in it.

### Step 1 — collect what happened

Classify:

- **Progress** (still open): interview invitation/stage
  scheduled-or-completed, or an offer not yet accepted/declined.
- **Resolution** (closed) — matches the `outcome.md` status enum:
  `hired`, `offer_declined`, `rejected`, `no_response` (if the user is
  unsure, note how long since last contact and let them decide — no
  imposed cutoff), `interview_only` (reached interviews, process
  stalled or abandoned without an explicit rejection).

Also ask, without interrogating: dates for stages reached, any feedback
received (verbatim where remembered), what the user would do
differently, any signal about what the company valued. Concrete beats
polished — this feeds `setup`'s calibration and STAR mining.

### Step 2 — confirm the materials, add what's missing

`data/applications/<company>-<role>-<YYMMDD>/` (already gitignored —
see `data/README.md`) is the same folder `rolesherpa-apply/SKILL.md`
created at draft time and wrote directly into — there is no separate
copy step anymore:

1. **`CV-<slug>.pdf`/`CV-<slug>.html`, `CL-<slug>.pdf`/`CL-<slug>.html`** — these already exist if the application went through `rolesherpa-apply/SKILL.md`; leave them exactly as they are, they're what was actually submitted. No draft files found (applied outside `rolesherpa-apply/SKILL.md`, folder created fresh in Step 0) → skip with a note; nothing to reconstruct.
2. **`job_posting.md`** — if present, leave it. Otherwise `WebFetch` the tracker row's `source` URL. Dead link (postings expire fast — this is exactly why the archive matters) → ask the user to paste it, or write an explicit "unavailable" stub. **Never reconstruct a posting from memory.**
3. **`outcome.md`** — write or update in this exact format:

```markdown
# Outcome: <Company> — <Role>

**Status:** in_progress | hired | offer_declined | rejected | no_response | interview_only

**Date resolved:** YYYY-MM-DD   <- only when resolved

## Interview stages reached
- [x] Phone screen (YYYY-MM-DD)
- [ ] Technical interview
- [ ] Case interview
- [ ] Final round
- [ ] Offer received

## Notes
<feedback, what to do differently, signals about what they valued —
appended per update with a date, never overwritten>
```

Tick stages as reached (with dates), append dated Notes entries, only
move `Status` from `in_progress` to a final value on resolution.
Re-running is idempotent — append, never duplicate or rewrite history.

### Step 3 — update the tracker

Update the matched row's `status` column and append a short dated note
to `notes`. Never restructure the CSV, reorder rows, or touch other
rows — use `CsvStore.save()` with the full row set only if you're
genuinely rewriting one row's fields, never to reorder.

### Step 4 — calibration handoff

Count `outcome.md` files with a **final** status. 3+ resolved, or 2+
sharing a pattern (same role type rejected twice, same sector going
silent) → suggest running `rolesherpa-setup/SKILL.md` to fold them into the
evaluation framework. **Never write to `04-job-evaluation.md` or other
`career-profile` files yourself** — that's `setup`'s job, and duplicating
it here would race it.

### Step 5 — confirm

Summarize what was recorded, what was archived vs. skipped and why,
and the tracker's new status. If an interview stage was newly
scheduled, point at `rolesherpa-interview/SKILL.md`. If the status is `hired`,
congratulate warmly first, then — once only, never for any other
status or on re-runs for the same application — mention that feedback
on the framework is always welcome.

## Quality criteria

- The archived version is always the submitted version — existing archive files are never overwritten by a fresher draft.
- Nothing is ever fabricated: a dead posting URL gets a pasted copy or an explicit "unavailable" stub.
- Re-running on the same application appends; it never duplicates folders, rows, or history.
- This skill never edits `career-profile/` files.

## Output format

See Step 5.

## Final check

Before confirming, re-read the written `outcome.md` and confirm the
`Status` line and the tracker's `status` column agree — they should
never drift apart.
