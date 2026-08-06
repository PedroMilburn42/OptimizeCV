---
name: rolesherpa-audit
version: 1.0.0
description: >
  Audits career-profile chronology for employment gaps, overlaps, and
  impossible date ranges, and optionally checks whether a specific
  generated CV silently dropped a role the profile still records.
  Classifies every finding as Case A (a drafting/rendering issue — the
  profile has it, this CV doesn't) or Case B (a real fact recorded in
  the profile itself, needing honest framing rather than a fabricated
  fix). Never states a conclusion — every finding is evidence plus a
  question plus a path to resolve. Triggers on: audit my CV, check for
  gaps, chronology check, /rolesherpa-audit
allowed-tools: Read, Write, Edit, Bash(python -m rolesherpa.cli profile *), Bash(grep *)
---

# Audit — Chronology and Consistency Check

## Context and role

This skill exists because a real CV (before this skill existed) silently
dropped an entire employment period during drafting, and nothing in the
pipeline caught it. The gap/overlap math
here is deterministic (pure date arithmetic, in
`rolesherpa.domain.chronology`, TDD'd) — this skill's job is the part
that isn't deterministic: deciding what a finding means and routing it
to the right fix, always with the user, never alone.

**Scope discipline:** this skill checks chronology and CV-vs-profile
fidelity only — not writing quality, buzzwords, or achievement
verifiability. Those are already governed by `03-writing-style.md`'s
backtrack test and `rolesherpa-apply/SKILL.md`'s Step 3 reviewer and
Step 5.4 anti-fabrication check. Don't duplicate them here.

**The Case A / Case B distinction — the core of this skill:**
- **Case A (drafting issue):** `data/profile/candidate-profile.md` has continuous,
  complete coverage for a period; a specific generated CV just doesn't
  show it (a silent cut, most often from page-budget trimming before
  `05-cv-templates.md`'s protected-content rule existed). Fixable by
  restoring the content — no new information needed.
- **Case B (a real fact):** the gap or overlap exists in the profile
  itself — there is no earlier, more complete record to restore from.
  Never fabricate an explanation to paper over it. The only honest
  moves are: log the true reason if the user has one, or prepare an
  honest answer for the interview.

## Task

### Step 0 — parse arguments

`$ARGUMENTS` may contain a path to a specific rendered CV (e.g.
`data/applications/acme_corp-software_engineer-260101/CV-acme_corp-software_engineer-260101.html`) to also
run the Case A check against, or nothing (profile-only chronology
audit).

### Step 1 — run the deterministic audit

```
python -m rolesherpa.cli profile audit-chronology data/profile/candidate-profile.md --gap-threshold-days 30
```

Present the raw JSON findings as-is first — entries parsed, gaps (with
exact day counts and which two roles bound them), overlaps, and
impossible ranges. This is evidence, not interpretation; state it
before any judgment.

### Step 2 — route each gap (Case B by construction)

A gap in the profile itself has no "restore from elsewhere" fix — the
profile is the thing being audited. For each gap, ask the user
directly: is there real, unrecorded activity for this period (freelance
work, studies, a project never logged), or is it a genuine unaccounted
period?

- **Unrecorded activity exists:** offer to add it to
  `data/profile/candidate-profile.md` under Professional Experience — exactly
  what the user says, nothing invented, same discipline as everywhere
  else in this project. This isn't really "Case A," it's simply
  completing a record that was never finished.
- **Genuine unaccounted period:** offer both, non-exclusive:
  1. A brief, honest note the CV could show if the user wants one
     (e.g. "Career transition — [reason in the user's own words]") —
     never invent the reason.
  2. A stub in `07-interview-prep.md`'s "Tough Questions" section
     (it already has a "Why leaving / gap in employment" category) so
     the user has a prepared, honest answer if it comes up.
- Never leave a gap finding unresolved without an explicit user
  decision — "no action" is a valid decision, but it must be the
  user's, stated, not a default from silence.

### Step 3 — route each overlap (usually informational, not a problem)

Most overlaps are normal — a part-time/adjunct/freelance/consulting
role alongside a full-time one (an adjunct teaching role held alongside
a full-time industry role is exactly this pattern; see
`data/profile/behavioral-profile.md`'s note on this being genuine,
evidenced work, not padding). Look at both
entries' titles for a part-time/independent signal
(Freelance, Independent, Consultant, Adjunct, Associate Professor)
before flagging anything.

- **One side reads as part-time/independent, the other full-time:**
  state this reading and ask the user to confirm it's accurate — don't
  assert it unprompted as fact, since the title text is a signal, not
  proof.
- **Both sides read as full-time, unrelated employers:** this is
  chronologically unusual — flag it explicitly as worth double-checking
  the dates for a data-entry error, or confirming it really happened
  that way (e.g. an overlapping notice period).

### Step 4 — route each impossible range

An end date before a start date is almost always a typo, not a real
fact. State which entry and which two dates conflict, propose the fix
(most often swapping them), and confirm with the user — never edit
`data/profile/candidate-profile.md` before they confirm which date is correct.

### Step 5 — Case A check (only if a CV path was given)

For each top-level entry `parse_profile_experience` found in the
profile, `grep` the target CV file for that entry's company name.

- **Company name absent from the CV entirely:** surface it — "The
  profile has a role at [Company] ([dates]) that doesn't appear
  anywhere in `data/applications/<slug>/CV-<slug>.html`. Was that an
  accidental cut, or a deliberate choice to leave it out as not
  relevant to this posting?" Never assume which.
  (`<slug>` here is whatever `data/applications/<company>-<role>-<YYMMDD>/`
  folder the CV path argument points at.)
  - **Accidental:** restore it — same bullet content as the profile,
    tailored per `05-cv-templates.md`'s rules — then re-render and
    re-verify (`python -m rolesherpa.cli render pdf ...` /
    `render verify ... --pages 2 --max-pages 3`).
  - **Deliberate:** leave it out, but note in the summary that this
    omission was reviewed and consciously accepted — not silently
    unflagged.

### Step 6 — summary

State, per finding: what was found (with the deterministic evidence),
what was decided, and what (if anything) is still open because the
user wants to think about it before deciding. Never mark something
resolved that the user didn't actually confirm.

## Quality criteria

- Every finding leads with deterministic evidence (exact dates/day
  counts from `rolesherpa.domain.chronology`) before any interpretation.
- No finding is ever presented as a conclusion about the candidate —
  always "this could be a signal worth checking," paired with a
  concrete question and a way to resolve it.
- Nothing is written to `data/profile/candidate-profile.md`,
  `07-interview-prep.md`, or any CV file without the user confirming
  the exact content first.
- A part-time/independent-vs-full-time overlap reading is stated as a
  reading to confirm, never asserted as settled fact from title text
  alone.
- This skill's `.agents/` and `.claude/` copies stay byte-identical
  per `AGENTS.md`'s mirroring rule — re-copy after any edit.

## Output format

See Step 6.

## Final check

Before presenting the summary, confirm every gap/overlap/impossible-range
finding from Step 1's raw output was actually routed to a decision in
Steps 2-4 — none silently dropped from the report.
