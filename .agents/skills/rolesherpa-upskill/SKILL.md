---
name: rolesherpa-upskill
version: 1.0.0
description: >
  Compares tracked postings (or a single posting) against the candidate
  profile to find skill gaps and produce a prioritized learning plan with
  real, web-searched resources. Triggers on: upskill, skill gaps, what
  should I learn, learning plan, /rolesherpa-upskill
allowed-tools: Read, Write, Glob, WebFetch, WebSearch
---

# Upskill — Gap Analysis and Learning Plan

## Context and role

Two modes. **Aggregate** (`/rolesherpa-upskill`, no argument): analyze every row
in `data/job_search_tracker.csv`, weighted by how poor a fit each was —
a low `fit_rating` job contributes more to the gap signal, since it
exposed more gaps. **Targeted** (`/rolesherpa-upskill <URL>`): analyze one fetched
posting in isolation; the tracker is not consulted in this mode.

## Task

### Step 1 — load data

**Aggregate:** read `data/job_search_tracker.csv` — each row's `role`,
`company`, `fit_rating` (0-100, lower means more gap-weight). Read
`data/profile/candidate-profile.md`. Check
`upskill/` (create if missing) for the most recent
`report-YYYY-MM-DD.md` to diff against later.

**Targeted:** `WebFetch` the posting, extract title, company, required
and preferred skills, responsibilities. Read `data/profile/candidate-profile.md`.
No tracker data in this mode.

### Step 2 — hard skill diff (Pass 1)

**Aggregate:** the tracker doesn't carry full posting text — infer
likely required skills from `role`/`sector`/`notes`; optionally
`WebFetch` the row's `source` if present and not dead, skip if missing.
Build a skill-frequency map, then weight each job's contribution by
`(100 - fit_rating) / 100` before summing per skill.

**Targeted:** extract the posting's explicit required/preferred skills
directly, equal weight each (only one job, no fit-weighting needed).

**Both modes:** drop any skill already present in the profile in any
form — be generous (a profile mentioning "Python" covers "Python
scripting"). What remains is the hard-skill gap list.

### Step 3 — synthesis (Pass 2)

Reason past the mechanical diff for gaps it would miss: domain
knowledge (industry/problem-space familiarity), soft skills (ways of
working, communication, leadership expectations the postings emphasize
but the profile doesn't address), tooling/process (frameworks, cloud
services, methodologies appearing across postings but absent from the
profile), credentials (a certification repeatedly listed as preferred).
Tag each: `[domain]`, `[soft]`, `[tooling]`, `[credential]`. Don't
duplicate Pass 1 findings — only add what it missed.

### Step 4 — gap heatmap

Priority: **Critical** (high-frequency/weight hard skills, or a domain
gap appearing across most tracked jobs) → **High** (moderate hard-skill
scores, or consistent soft/tooling gaps) → **Medium** (lower-frequency
hard skills, or synthesized gaps in fewer roles) → **Low** (one-off
mentions). Targeted mode maps required-skill gaps to Critical/High,
preferred-skill gaps to Medium, synthesized gaps to Medium/Low. Print
this table before continuing — the user should see what you're working
from before resource search starts.

### Step 5 — learning plan

For every Critical/High gap (and Medium too if fewer than 5 total
gaps): `WebSearch` for current resources —
`"best <skill> course <current year> site:reddit.com OR coursera.org OR fast.ai"`
style queries, current year included to avoid stale results. Pick 2-3:
prefer hands-on labs over lecture-only, official docs for tooling gaps,
books for domain gaps. For each: name, URL, one-line reason it fits.
Add a study direction tailored to the candidate's existing background
(be specific about what to skip, where to start) and a realistic time
estimate — err toward more, not less. Group by theme (Cloud &
Infrastructure, MLOps, Domain Knowledge, Security, Ways of Working,
Certifications), not alphabetically. **Never cite a resource you didn't
actually find via `WebSearch`** — no invented course names, URLs, or
authors.

### Step 6 — suggested study order

Dependencies first (note the dependency explicitly); within a
dependency tier, Critical before High before Medium; a fast (~5h)
Medium win can go early for momentum; domain/soft gaps generally go
last, better studied alongside a real project than up front.

### Step 7 — write the report

Assemble in order: (aggregate mode only, omit entirely otherwise or if
no prior report exists) **Since Last Report** — gaps closed (now
present in the profile) and new gaps since the prior report's date —
then **Gap Heatmap**, **Learning Plan**, **Suggested Study Order** with
a total time estimate. Save via `Write`:

- Aggregate: `upskill/report-YYYY-MM-DD.md`
- Targeted: `upskill/report-YYYY-MM-DD-<company-slug>-<role-slug>.md`

Confirm the saved path to the user.

## Quality criteria

- Every cited resource came from an actual `WebSearch` result this run — nothing invented.
- A skill present in the profile in any form is never flagged as a gap.
- The heatmap prints before the learning plan, every run.
- Low-priority gaps appear in the heatmap for completeness but get no learning-plan entry unless asked.
- The report is always saved, even if the terminal output alone would have satisfied the user.

## Output format

See Step 7's assembly order.

## Final check

Before saving, confirm every URL in the learning plan actually appeared
in a `WebSearch` result from this run — not recalled from general
knowledge.
