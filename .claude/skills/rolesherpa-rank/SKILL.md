---
name: rolesherpa-rank
version: 1.0.0
description: >
  Batch-scores every new job in seen_jobs.json against the evaluation
  framework and returns a ranked shortlist. Triage only — no company
  research, no salary lookup; apply always re-evaluates before drafting
  anything. Triggers on: rank jobs, shortlist, triage jobs, score my
  matches, /rolesherpa-rank
allowed-tools: Read, Write, Agent, AskUserQuestion
---

# Rank — Triage Scraped Jobs

## Context and role

`rolesherpa-scrape/SKILL.md` finds and dedupes postings; `rolesherpa-apply/SKILL.md` evaluates
one posting in depth, with company research, before anything gets
drafted. This skill is the bridge: cheap enough to run after every
scrape, scoring from posting text and the profile only. A rank score is
never a substitute for `apply`'s full evaluation — it decides what's
worth spending `apply` effort on.

## Task

### Step 0 — parse input

- No argument → rank every entry in `data/seen_jobs.json` with `status: "new"`.
- A focus area (e.g. "data science") → rank only entries whose title or fit notes match.
- `--all` → re-rank every non-applied entry, including previously ranked ones (useful after the profile changes).
- `--top <N>` → shortlist size, default 5.

### Step 1 — load state

1. Read `data/seen_jobs.json`. No entries → tell the user to run `rolesherpa-scrape/SKILL.md` first and stop.
2. Read `data/job_search_tracker.csv`; any company+role already there is out of scope regardless of flags.
3. Select candidates: `new` (or all non-applied with `--all`) minus the tracker exclusion set, filtered by focus area if given. Nothing left → say so and stop.
4. Read `.agents/skills/career-profile/04-job-evaluation.md` and `data/profile/candidate-profile.md` once — hold them in context, don't re-read per candidate.

### Step 2 — batch-score

Dispatch parallel agents, roughly 5 jobs per agent (one agent is fine
for ≤5 jobs). Each agent gets, inline in its prompt — not by re-reading
files:

- The job list (title, company, URL) for its batch
- A compact rubric extracted from Step 1's files: strong/moderate/weak skill areas, direct/adjacent experience domains, behavioral thrive/drain factors, career goals, deal-breakers, location constraints

Each agent fetches every posting URL itself and scores strictly from
what it actually fetched — a dead URL, a redirect to a listing page, or
an expired posting gets marked `expired`, never scored from the title
alone. No company research, no salary lookup at this stage — that
belongs to `apply`.

Each agent returns one JSON object per job:

```json
{
  "key": "<seen_jobs.json key>",
  "status": "scored" | "expired",
  "scores": {"technical": 0-100, "experience": 0-100, "behavioral": 0-100, "career": 0-100},
  "location": "PASS" | "FAIL" | "FLAG",
  "deadline": "YYYY-MM-DD" | null,
  "strengths": ["1-3 bullets, grounded in the posting text"],
  "gaps": ["1-3 bullets, honest"],
  "language": "<posting language>"
}
```

### Step 3 — aggregate and rank

For each scored job: overall = weighted sum per `04-job-evaluation.md`
(Technical 30%, Experience 25%, Behavioral 15%, Career 30%); map to the
verdict bands. `FAIL` location excludes the job from the ranked list
regardless of score — list it separately with the reason. `FLAG`
location stays ranked with a visible marker. A deadline within 7 days
gets a priority marker and wins ties on equal scores; a passed deadline
becomes `expired`.

### Step 4 — update state

In `data/seen_jobs.json`, additively: ranked jobs get
`"status": "ranked"`, `"rank_score"`, `"rank_verdict"`, `"rank_date"`;
dead/expired jobs get `"status": "expired"`. Never touch
`job_search_tracker.csv` — this skill only ranks, it never applies.
Re-running is idempotent: already-`ranked` entries are skipped unless
`--all`.

### Step 5 — present

Shortlist table (score, verdict, title, company, location, deadline),
2-3 strength bullets per shortlisted job with the honest gap, a
below-threshold table, and an excluded list (location `FAIL` /
expired, with reasons). State plainly that these are triage scores from
posting text only and `apply` will re-evaluate with company research
before drafting anything. Ask which number(s), if any, the user wants
to run through `rolesherpa-apply/SKILL.md` — pass the triage verdict as context,
but always re-run `apply`'s Step 1 evaluation in full.

## Quality criteria

- Never score an unfetched posting — a dead link is `expired`, not guessed.
- A deal-breaker (location `FAIL`) excludes a job from the ranking regardless of how high it scores otherwise.
- Gaps are stated per job, never smoothed over to make a prestigious-looking posting rank higher than it should.
- `seen_jobs.json` fields are only ever added to, never restructured.

## Output format

See Step 5.

## Final check

Before presenting, confirm every shortlisted job's score traces back to
an agent result keyed to that job — never a number invented in the
aggregation step itself.
