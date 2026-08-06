---
name: rolesherpa-expand
version: 1.0.0
description: >
  Discovers competencies hidden in onboarding documents and public online
  presence (GitHub, portfolio sites) and proposes additive-only enrichments
  to the candidate profile. Triggers on: expand my profile, find more
  skills, mine my GitHub, competency discovery, /rolesherpa-expand
allowed-tools: Read, Write, Edit, Glob, WebFetch, WebSearch
---

# Expand — Competency Discovery from Documents and Online Presence

## Context and role

This skill only adds — it never modifies existing profile content.
Every addition is source-traceable so a future run stays idempotent and
the user can verify or remove any item later.

## Task

### Step 0 — read existing profile

Read `data/profile/candidate-profile.md` and
`data/profile/behavioral-profile.md` in parallel, hold in context for the rest of
this skill — you need to know what's already there to avoid proposing
duplicates.

### Step 1 — discover, source by source

**`documents/cv/`** — every course/module (including university
coursework), every certification (issuer, date), every job
responsibility bullet (tools, methods, outcomes), independent/side
projects, volunteer or extracurricular roles.

**`documents/linkedin/`** — courses/certifications, skills and
endorsements, volunteer experience, projects, anything not already
found in the CV.

**`documents/diplomas/`** — course/module names on transcripts, thesis
title and subject area, specialization tracks.

**`documents/references/`** — competency language the referee uses,
specific projects/tools/methods named.

**GitHub** — if `data/profile/candidate-profile.md` has a GitHub URL/username,
fetch the public profile and repo list (not just pinned repos —
unpinned repos often carry real signal). For each: name, description,
primary language(s), topics, frameworks/libraries mentioned in the
README.

**Other profile URLs** (portfolio site, Kaggle, Google Scholar,
ResearchGate) — fetch and extract tools, methods, datasets, awards,
skills mentioned.

### Step 2 — web enrichment

For every item found, apply **both** of these — not one or the other:

- **Direct lookup** (named courses, certifications, tools, frameworks): search `"[item] syllabus learning outcomes"` / `"[cert] skills covered exam guide"` / `"[tool] skills what you learn"`, fetch the most relevant result, extract the competency list.
- **Inference** (always, regardless of what direct lookup found): what problem domain does this address, what skills/knowledge does someone doing this work need, what's the standard toolchain.

Prioritize direct lookup for named online courses/certifications and
GitHub repos with a README naming specific tech; rely on inference
alone for generic bullets, vague project descriptions, and reference
letter language (already phrased as competency — just record it).

### Step 3 — build the competency map

Deduplicate into: Technical Skills — Primary, Technical Skills —
Secondary, Domain Knowledge, Methods and Practices, Soft/Behavioral.
For each: the competency, its source item, and whether it came from
direct lookup, inference, or both. Remove anything already present in
`data/profile/candidate-profile.md` or `data/profile/behavioral-profile.md`.

### Step 4 — present and confirm

Show every new competency, grouped by source, before writing anything:

```
## expand found [N] new competency signals across [M] sources

**COURSES & CERTIFICATIONS**
Source: [name — provider]
  + [competency]

**GITHUB — [repo-name]**
Source: README + inferred from tech stack
  + [competency]
```

Then ask: **`all`** (add everything), **`review`** (walk through each
source group), or **`skip`** (cancel, write nothing) — or list specific
groups to skip.

### Step 5 — write confirmed additions

`Edit` only, never a full rewrite. Technical/domain/methods findings →
append to `data/profile/candidate-profile.md`'s matching sections, each with a
source annotation (`(GitHub — project-name)`, `(Coursera — course
name)`) so future runs stay idempotent. Behavioral signals → append to
`data/profile/behavioral-profile.md`'s "Strongest Behavioral Traits" or "How I
Work Best", always labeled `[Inferred from <source> — review before
relying on this]`.

### Step 6 — summary

What was added per file with sources, sources processed and how many
competencies each yielded, sources skipped (missing/empty/nothing new)
with a brief reason, and anything ambiguous flagged for manual review.

## Quality criteria

- Additive only — never touches existing profile content.
- Every addition is source-traceable.
- Both direct lookup and inference are applied together for named items, never one substituted for the other.
- Behavioral additions are always labeled as inferred.
- Nothing is written before the user confirms in Step 4.

## Output format

See Step 6.

## Final check

Before writing, re-count the confirmed items against what Step 4
actually showed the user — never write an item the user didn't
explicitly confirm or that fell under a group they chose to skip.
