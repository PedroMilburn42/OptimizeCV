---
name: rolesherpa-reset
version: 1.0.0
description: >
  Destructively clears candidate profile data and/or onboarding documents
  so the user can start fresh with rolesherpa-setup/SKILL.md. Nothing is deleted
  without explicit confirmation. Triggers on: reset my profile, start
  over, clear my data, wipe onboarding, /rolesherpa-reset
allowed-tools: Read, Write, Edit, Bash(rm -f documents/cv/*), Bash(rm -f documents/linkedin/*), Bash(rm -f documents/diplomas/*), Bash(rm -f documents/references/*), Bash(rm -rf data/applications/*/)
---

# Reset — Clear Candidate Profile Data

## Context and role

This is a destructive skill. Nothing is deleted until the user types
the exact confirmation string. Treat every step as gated on that
confirmation, not as a formality.

## Task

### Step 0 — parse scope

`$ARGUMENTS`: `profile` (clears `data/profile/` candidate data plus
STAR examples/profile statements in `career-profile/`, keeps
framework/structure), `documents` (deletes files under `documents/`'s
subfolders and the per-application archive under `data/applications/`,
keeps folder structure and `README.md` files), `all` (both). No
recognized scope → ask:

> **What would you like to reset?**
> - **`profile`** — candidate data in `data/profile/` (candidate profile, behavioral profile) plus STAR examples and profile statements in `career-profile/`. Framework and writing rules are preserved.
> - **`documents`** — everything in `documents/`'s subfolders, plus the archived CVs/cover letters/outcomes under `data/applications/`. The folder structure and READMEs are preserved.
> - **`all`** — both.

Wait for the response before continuing.

### Step 1 — show exactly what will be cleared

**If scope includes `profile`:** read the current state of
`data/profile/candidate-profile.md`, `data/profile/behavioral-profile.md`,
`05-cv-templates.md` (profile-statements section only),
`07-interview-prep.md` (STAR examples/candidates sections only) and
report has-content vs. already-empty for each. State plainly that
`03-writing-style.md`, `04-job-evaluation.md`, `06-cover-letter-templates.md`
are **not** touched — they're framework rules, not candidate data.

**If scope includes `documents`:** Glob-list every file present under
`documents/{cv,linkedin,diplomas,references}` and `data/applications/`.
If every one of those is already empty, say so and skip confirmation
for this scope entirely.

### Step 2 — require explicit confirmation

> **This cannot be undone.**
> Type **`RESET`** (all caps) to confirm, or anything else to cancel.

Exactly `RESET` → Step 3. Anything else → stop: "Reset cancelled.
Nothing was changed."

### Step 3 — execute

**Profile reset** — `Read`/`Write`, targeted:

- `data/profile/candidate-profile.md`: replace the whole file with the
  contents of `templates/profile/candidate-profile.md`, read fresh at
  reset time — never a skeleton defined inline here, so this always
  matches the tracked template regardless of drift.
- `data/profile/behavioral-profile.md`: replace the whole file with the
  contents of `templates/profile/behavioral-profile.md`, same approach.
- `05-cv-templates.md`: replace only the "Profile statement templates" section with a placeholder comment; leave the rest (structure, tailoring rules, cutting rules) intact.
- `07-interview-prep.md`: remove the "Ready-Made STAR Examples" content and any "STAR Candidates (Complete Manually)" section; leave the STAR-format explanation, tough questions, questions-to-ask, logistics, and roleplay guidelines intact.

**Documents reset** — for each non-empty subfolder:

```bash
rm -f documents/cv/*
rm -f documents/linkedin/*
rm -f documents/diplomas/*
rm -f documents/references/*
rm -rf data/applications/*/
```

Never delete `documents/README.md`, `data/README.md`, or the folders themselves.

### Step 4 — confirm and next steps

Report what was actually cleared vs. already empty/preserved. Then:
profile reset → run `rolesherpa-setup/SKILL.md` to repopulate (it auto-detects
`documents/` or walks through CV import / interview mode); documents
reset → add files to `documents/` (see its `README.md`) then run
`rolesherpa-setup/SKILL.md`; both → do the documents step first, then setup.

## Quality criteria

- Nothing is deleted before the user types the exact string `RESET`.
- Framework/structural content (`03`, `04`, `06`, and the non-profile-statement parts of `05`/`07`) is never touched by a `profile` reset.
- `documents/README.md`, `data/README.md`, and the folder structure survive a `documents` reset.
- If a scope's target is already empty, that's reported plainly — no confirmation prompt for nothing to clear.

## Final check

Before executing Step 3, re-confirm the user's literal last message was
exactly `RESET` — not "ok", not "yes", not "reset" lowercase.
