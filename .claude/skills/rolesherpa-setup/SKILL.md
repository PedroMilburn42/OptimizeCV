---
name: rolesherpa-setup
version: 1.0.0
description: >
  Onboards a candidate into RoleSherpa: builds the career-profile reference
  docs, the scrape search queries, and detects or records which AI host is
  assisting. Triggers on: setup, onboarding, get started, build my profile,
  configure job search, /rolesherpa-setup
context: fork
allowed-tools: Read, Write, Edit, Glob, Bash(python -m rolesherpa.cli *), AskUserQuestion
---

# Setup — Candidate Onboarding

## Context and role

You are onboarding a new candidate into RoleSherpa. Every other skill in
this repo — `scrape`, `rank`, `apply`, `interview`, `outcome`, `upskill`
— depends on the files this skill produces. Nothing downstream works
correctly if this skill fabricates data instead of asking, so when
information is missing, ask; never guess a skill, a date, or an
achievement.

## Task

### Step 0 — bootstrap profile files from templates

`data/profile/` is gitignored — a fresh checkout has none of
`candidate-profile.md`, `behavioral-profile.md`, `search-queries.md`
yet. Before doing anything else (including Step 1, which may need to
write into `candidate-profile.md`), for each of the three files below:
if the `data/profile/` target doesn't already exist, create it by
copying the matching template verbatim. If it already exists, leave it
untouched — never overwrite an existing populated profile with the
blank template.

- `templates/profile/candidate-profile.md` → `data/profile/candidate-profile.md`
- `templates/profile/behavioral-profile.md` → `data/profile/behavioral-profile.md`
- `templates/profile/search-queries.md` → `data/profile/search-queries.md`

### Step 1 — detect the assisting host

`detect_host()` (`src/rolesherpa/domain/host.py`) is a library function,
not a CLI command — check its three signals directly:
`env | grep -E 'CLAUDECODE|CODEX_SANDBOX|ANTIGRAVITY_AGENT'`. If exactly
one matches, note the corresponding host (Claude Code / Codex /
Antigravity) silently — do not ask the user. If none matches, ask once:
"Which tool is running this session — Claude Code, Antigravity, or
Codex?" and record the answer in `data/profile/candidate-profile.md`'s
"Assisting tool" field (created by Step 0 if it didn't already exist).
This value is what `rolesherpa-apply/SKILL.md` names when a generated
document mentions agentic tooling — never hardcode a tool name
elsewhere.

### Step 2 — choose an onboarding path

If invoked with `--section <name>` (`profile`, `behavioral`,
`writing-style`, `goals`, `cv-templates`, `cover-letter-templates`,
`interview-prep`, or `search`), skip straight to collecting and writing
that one section under Step 3/4 — skip the path-selection prompt below,
and touch no other file.

Scan `documents/` (`cv/`, `linkedin/`, `diplomas/`, `references/`) and
`data/applications/` with Glob. Greet the user and offer three paths,
leading with **Path A** if any of those has files, otherwise leading
with **Path C**:

- **Path A — read `documents/`:** read everything present, cross-reference
  for consistency, propose changes before writing. Idempotent — safe to
  re-run as more documents are added.
- **Path B — single CV paste:** the user pastes or `@`-mentions one CV;
  extract it, then ask follow-up questions for what's missing.
- **Path C — interview mode:** walk through structured questions
  conversationally, section by section. Best when starting from
  nothing.

### Step 3 — collect the data

Whichever path, the destination is `data/profile/candidate-profile.md`
and `data/profile/behavioral-profile.md`, plus five remaining
`career-profile` files, plus search configuration:

1. Identity, education, experience, skills, publications, awards, references → `data/profile/candidate-profile.md`
2. Behavioral traits → `data/profile/behavioral-profile.md`. Formal-assessment scores are authoritative: cite the raw score where the source reports one, and never overwrite an existing formal-assessment finding — append new information as a dated note instead. Anything synthesized from a non-formal source (LinkedIn About, conversational answers) gets `[Inferred — review before relying on this]`.
3. Recurring cover-letter patterns *(Path A only, once 2+ real applications exist under `data/applications/`)* → `03-writing-style.md`'s "Patterns Observed" section. A single letter is not a pattern — wait for 2+ before adding.
4. Career goals, motivation filters, life-situation constraints, skill-match self-assessment → `04-job-evaluation.md`'s placeholder fields
5. Reusable profile-statement openers *(Path A only, from past `data/applications/*/CV-*.html`)* → `05-cv-templates.md`, each labeled `[Used for: <company>-<role>-<YYMMDD>]`.
6. Structurally distinct opening/closing patterns *(Path A only, same source as 3)* → `06-cover-letter-templates.md` — skip anything that duplicates what's already there.
7. STAR-candidate stubs for achievements without a full write-up *(Path A only, from CV/LinkedIn/reference-letter text)* → `07-interview-prep.md`'s "STAR Candidates" section. Never draft the full STAR — only the stub, exactly this shape:

   ```markdown
   ### [Achievement title]
   **Source:** [CV / LinkedIn / Reference letter — role/company]
   **What happened:** [one sentence]
   **Why it matters:** [interview question types this could answer]
   **S/T/A/R stub:**
   - Situation:
   - Task:
   - Action:
   - Result:
   ```

Search configuration (below) → `data/profile/search-queries.md`.

**Path A specifics:** read the existing `data/profile/candidate-profile.md`,
`data/profile/behavioral-profile.md`, and the remaining `career-profile`
files first — you need to know what's already there before proposing
anything. Process `documents/` subfolders in order `cv/` → `linkedin/`
→ `diplomas/` → `references/`, then `data/applications/`. Flag any date, title,
or employer mismatch across documents as a numbered list and wait for
the user to resolve each one before writing. Split findings into
**additive** (new content, safe to batch-confirm) and **conflicting**
(disagrees with something already recorded, confirm one at a time:
keep / replace / I'll edit myself). Label anything inferred from tone
or indirect signal (e.g. behavioral traits from a LinkedIn About
section) as `[Inferred — review before relying on this]`.

**Path B / C specifics:** ask naturally, not as a rigid form; the
user answers in their own words, you structure it. Skip optional
sections (publications, awards, references) if the user has none.

**Search configuration** (all paths, drives `rolesherpa-scrape/SKILL.md`):

- 3-8 role titles to search for.
- 3-5 distinctive, searchable skills.
- Target companies to monitor (optional).
- Geographic scope and commute tolerance — defines location filter tiers (ideal / acceptable / borderline / too far).
- Confirm the three installed connectors (LinkedIn, Freehire, Computrabajo Uruguay — see `config/sources.yaml`) fit the user's market; if they need a portal outside this set, point them at `rolesherpa-add-portal/SKILL.md`.

Also proactively suggest adjacent role types the skill profile supports
but the user may not have considered — this is a real value-add, not
filler.

### Step 4 — write the files

For Path A, write only confirmed changes via `Edit`, never a full
rewrite of a `career-profile` or `data/profile/` file. State per file
which changes were applied, or "no changes made" if none were
confirmed. For Path B/C, write full sections via `Write`/`Edit` as data
is collected.

Populate `data/profile/search-queries.md` with the collected role
titles, skills, and location tiers, organized into priority tiers
(strongest direction first, then domain expertise, then adjacent
pivots, then a broad net).

If Path A found nothing under `data/applications/`, leave
`03-writing-style.md`, `05-cv-templates.md`, `06-cover-letter-templates.md`,
and `07-interview-prep.md`'s stub section untouched — there's nothing
to mine yet, and that's the correct outcome, not a gap to fill with
invented content.

## Quality criteria

- Nothing in `career-profile/` or `data/profile/` states a skill, role, or achievement the user didn't actually provide.
- Path A never silently overwrites conflicting data — every conflict gets an explicit user decision.
- The bootstrap step (Step 0) never overwrites an existing populated `data/profile/` file with the blank template.
- `data/profile/behavioral-profile.md` never loses a formal-assessment finding to an overwrite — new information is appended and dated, not substituted in.
- `03/05/06-*.md` additions come only from real application history (2+ examples for `03`), never invented from a single data point or from zero data.
- `07-interview-prep.md` gets STAR stubs during onboarding, never a fully drafted STAR example — that's the candidate's or `rolesherpa-interview/SKILL.md`'s job later, with real S/T/A/R detail.
- Search queries are specific enough to be useful (not "software engineer" with no skill/location qualifiers) and cover the user's real range, including adjacent roles.

## Output format

End with a short confirmation: which files were written or updated,
and what to try next — `rolesherpa-scrape/SKILL.md` to search now, `rolesherpa-apply/SKILL.md`
with a posting URL to see the full workflow end to end, or
`--section <name>` later to refresh just one section (e.g. `--section search`)
without repeating full onboarding. If Path A left any STAR stubs in
`07-interview-prep.md`, mention how many and that they need
Situation/Task/Action/Result detail before use in an interview.

## Final check

Before finishing, re-read `data/profile/candidate-profile.md` and
confirm every placeholder token you were supposed to fill is gone
(`grep -n '\[.*populated' data/profile/*.md .agents/skills/career-profile/*.md`
should show nothing for sections the user actually answered). If a
section is legitimately still empty because the user skipped it, say
so explicitly rather than leaving it silently blank.
