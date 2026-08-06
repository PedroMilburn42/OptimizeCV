---
name: rolesherpa-interview
version: 1.0.0
description: >
  Builds a stage-specific interview prep pack for a real, tracked
  application, and optionally runs a mock interview. Triggers on:
  interview prep, prepare for interview, mock interview, upcoming
  interview, /rolesherpa-interview
allowed-tools: Read, Write, WebFetch, WebSearch
---

# Interview — Stage-Specific Prep

## Context and role

`rolesherpa-apply/SKILL.md` optimized what the company reads; this skill optimizes
what the company hears. The bridge is consistency — the interviewer has
read the submitted CV and cover letter, so nothing prepared here may
contradict what those documents claim. This preps a **specific tracked
application** — there is no generic no-target practice mode; if asked
for that, prep against a real application instead.

## Task

### Step 0 — resolve the application

`$ARGUMENTS` may name a company (optionally a role). Match against
`data/job_search_tracker.csv` rows, case-insensitive on company then
role. One match → proceed. Several → list and ask. None → the
application isn't tracked; suggest `rolesherpa-outcome/SKILL.md` first, or accept
posting/role details directly to prep anyway. No argument → list
tracker rows with a status suggesting a live process (`interview`,
`offer`, recently `applied`) and ask which.

Once the company/role are known, locate the application folder by
globbing `data/applications/<company_slug>-<role_slug>-*/` (same
lowercase, underscore-internally slug convention `rolesherpa-apply/SKILL.md`
and `rolesherpa-outcome/SKILL.md` use). Several matches → list dates and
ask.

### Step 1 — load context

1. **Application folder:** `job_posting.md`, the submitted `CV-*.pdf`/`CL-*.pdf` (or `.html` sources), and `outcome.md` for the stage reached and any earlier-round feedback — feedback from stage N is the highest-value input for stage N+1 — all in the same `data/applications/<company>-<role>-<YYMMDD>/` folder located in Step 0.
2. **Fallback** if no folder exists yet (application predates `rolesherpa-apply`/`rolesherpa-outcome`): fetch the posting via `WebFetch` on the tracker row's `source`, or ask the user to paste it; ask the user for the CV/cover letter directly. State plainly what's missing rather than guessing, and suggest running `rolesherpa-outcome/SKILL.md` to build the folder going forward.
3. Ask what's not already in `outcome.md`: stage (phone screen / technical / case / final), date, format, interviewer names/titles if known.
4. Read once, hold in context: `.agents/skills/career-profile/07-interview-prep.md`, `data/profile/candidate-profile.md`, `data/profile/behavioral-profile.md`, `04-job-evaluation.md`.

### Step 2 — research (interview-focused)

Run `04`'s Company Research Checklist, plus: if interviewer names are
known, look up their public professional profile — a hiring manager
probes team fit and motivation, a senior engineer probes technical
depth, HR probes the CV timeline; note the likely angle per person from
public information only, never speculation. Find 2-3 recent, verifiable
company specifics usable as natural conversation hooks. **Every claim
that ends up in the pack must be independently confirmed** — an
unverified "fact" delivered confidently in an interview is worse than
no fact.

### Step 3 — build the prep pack

1. **Likely questions**, priority order: recorded feedback from earlier stages → the fit evaluation's gaps (each gets an honest bridge answer: acknowledge, connect adjacent experience, show the learning path — never invented experience) → the posting's stated requirements → stage-type defaults (phone screens: motivation/timeline; technical: the posting's stack; final: values/salary/reservations).
2. **STAR mapping:** match `07`'s ready-made examples to the likely questions via their "Use for" tags. For a likely question nothing covers, draft a new STAR answer grounded strictly in `data/profile/candidate-profile.md` facts — offer to append it to `07` only with explicit user approval. Surface any incomplete STAR stubs relevant to this role.
3. **Consistency brief:** the specific claims the submitted CV/cover letter make that an interviewer is likely to probe. Rule: no claim in the room that isn't on the paper, and every claim on the paper must be defensible in depth.
4. **Tough questions, customized:** from `07`'s categories, with per-application answers — "why this company" must use a verified hook from Step 2, never a generic line.
5. **Questions to ask:** 4-6 from `07`'s categories, matched to the stage; cut anything the research already answered publicly.
6. **Logistics:** phone/video tips from `07` if relevant, plus date and interviewer names as a header.

Save to `data/applications/<company>-<role>-<YYMMDD>/interview_prep_<stage>.md`
(the same folder located in Step 0; create it if this predates
`rolesherpa-apply`/`rolesherpa-outcome`) — one file per stage, so
earlier packs stay as history. Present the pack in chat too; the file
is the artifact, the conversation is the delivery.

### Step 4 — offer a mock interview

If the user wants to practice, run it in this conversation per `07`'s
Roleplay Guidelines: warm-up → role-specific technical questions → 1-2
behavioral questions tied to the posting's competencies → one tough
question or curveball. After each answer: brief feedback — what
worked, what to sharpen, which STAR example would have served better.
Calibrate tone against `data/profile/behavioral-profile.md` — coach toward the
candidate's natural register, not a generic ideal.

### Step 5 — close the loop

Tell the user to run `rolesherpa-outcome/SKILL.md` after the interview to log the
stage and any feedback — it sharpens the next round's prep and, once
enough applications resolve, feeds `rolesherpa-setup/SKILL.md`'s
calibration of the evaluation framework (`04-job-evaluation.md`'s
"Calibration from Past Applications" section).

## Quality criteria

- Nothing prepared here contradicts the submitted CV/cover letter.
- Every company-specific claim is independently verified before it appears in the pack.
- Weak matches get honest bridge answers, never invented experience.
- The prep pack is stage-appropriate — a phone-screen pack and a final-round pack are different documents.

## Output format

See Step 3's six sections, in order, saved to the archive and shown in chat.

## Final check

Before presenting, re-read the pack's "Consistency brief" against the
actual submitted files one more time — confirm nothing prepared here
would surprise an interviewer who has both documents open.
