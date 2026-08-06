---
name: rolesherpa-apply
version: 1.0.0
description: >
  Full job-application workflow: fit evaluation, then (with explicit user
  approval) a drafted CV and cover letter, an isolated adversarial review
  pass, revision, rendering, and automated verification before anything
  is presented. Triggers on: apply to this job, evaluate this posting,
  write my CV, write a cover letter, job application, /rolesherpa-apply
allowed-tools: Read, Write, Edit, WebFetch, WebSearch, Agent, Bash(python -m rolesherpa.cli render *), Bash(python -m rolesherpa.cli profile *)
---

# Apply — Drafter-Reviewer Job Application Workflow

## Context and role

You are running a two-pass workflow: you draft, then a separately
dispatched reviewer agent critiques with fresh eyes and real company
research, then you revise. The posting is `$ARGUMENTS` (a URL or pasted
text). Follow the steps in order — the user gate in Step 1 and the
verification pass in Step 5 are not optional.

**Token efficiency:** don't re-`Read` a file already in context from an
earlier step. Pass draft content inline to the reviewer agent rather
than making it re-read files you already have. Run verification exactly
once, at the end.

## Task

### Step 0 — parse the posting

Fetch (`WebFetch` for a URL) or use the pasted text directly. Extract
company, role title, department (if given), location, and the
posting's language. Hold these for the rest of the workflow.

### Step 1 — evaluate fit (drafter)

Read `.agents/skills/career-profile/04-job-evaluation.md` and
`data/profile/candidate-profile.md`. Score the posting per the framework, present
the evaluation table (see `04`'s Output Format). If Experience Match
scores below 50, warn before asking to proceed that this posting will
need heavy reframing to draft honestly — see `03-writing-style.md`'s
backtrack test. Then ask: "Should I proceed with drafting the CV and
cover letter for this role?" **If the user declines, stop here — do not
draft anything.**

### Step 2 — draft (drafter)

You already have `data/profile/candidate-profile.md` and `04-job-evaluation.md`
in context — don't re-read them. Read only what you don't have yet:
`03-writing-style.md`, `05-cv-templates.md`, `06-cover-letter-templates.md`.
Read one existing `data/applications/*/CV-*.html` and one
`data/applications/*/CL-*.html` if any exist, as concrete
structural reference.

Create the application folder now, before writing anything:
`data/applications/<company>-<role>-<YYMMDD>/` — company and role slugs
are lowercase with underscores for internal word separation, a single
dash separates the company/role/date blocks, and the date is today's
date (the folder is created once, at draft time, and reused through
submission, outcome, and interview prep — never copied elsewhere). E.g.
`data/applications/acme_corp-software_engineer-260101/`. `<slug>` below
always means that same `<company>-<role>-<YYMMDD>` string.

- **CV** (`data/applications/<slug>/CV-<slug>.html`, e.g. `CV-acme_corp-software_engineer-260101.html`): English always, follow `05-cv-templates.md` (the active template if one is registered via `rolesherpa-add-template/SKILL.md`, otherwise `templates/cv/stock/`). Open with whichever profile-statement arc in `data/profile/cv-profile-arcs.md` (see `05-cv-templates.md`) fits this posting better (Arc A governance/compliance, Arc B AI/data-science pivot) — state which one you picked and why in Step 6, don't blend them. Tailor bullets to this posting; 2 pages target, 3 tolerated per `05`'s Structure section.
- **Cover letter** (`data/applications/<slug>/CL-<slug>.html`): match the posting's language, follow `06-cover-letter-templates.md`, address a named contact if given or "Dear Hiring Manager"/its equivalent; 1 page. Any mention of agentic tooling names whichever host is recorded in `data/profile/candidate-profile.md`'s "Assisting tool" field (or `detect_host()`'s result) — never a hardcoded name.

Before finalizing a bullet, run `03-writing-style.md`'s backtrack test.
Anything in the "flag it" zone goes to the user: "This bullet is a
stretch because X. Keep, soften, or drop?" — resolve it before writing
the file, not after.

**New information not in the profile:** if the user mentions an
achievement, skill, role detail, or fact anywhere in this conversation
that isn't in `data/profile/candidate-profile.md`, don't just use it in
this document and let it disappear afterward — that's exactly how a
real past achievement (an AI voice-cloning fraud-detection project)
ended up baked into one old CV and nowhere in any structured profile.
Before writing the final files, ask once: "You mentioned [X], which
isn't in your profile yet. Want me to add it to
`data/profile/candidate-profile.md` so it's available for future
applications too?" On yes, `Edit` `data/profile/candidate-profile.md`
with exactly what the user said (same anti-fabrication discipline as
everywhere else — nothing embellished) and note the addition in Step
6. On no, use it in this document only, as before.

Write both files. Keep the exact text in working memory for Step 3 and Step 4 — don't re-read them either.

### Step 3 — research and critique (reviewer, isolated)

Dispatch a `general-purpose` agent with the Agent tool. It gets a fresh
context — pass the drafts **inline in the prompt**, do not have it
`Read` the files. Scope its own reads to
`data/profile/candidate-profile.md`, `data/profile/behavioral-profile.md`,
`03-writing-style.md`, `04-job-evaluation.md` only — it doesn't need the
template/structural files (`05`, `06`), those govern formatting the
drafter already applied.

The reviewer's job:
1. Research the company (`WebSearch`/`WebFetch`) — website, mission, recent news, the specific team if named, culture signals.
2. Critique the drafts against the four files above, especially checking whether the cover letter's voice matches `data/profile/behavioral-profile.md`'s natural register (a collaborator profile shouldn't read as a lone-wolf pitch; a persuader profile shouldn't read as over-hedged).
3. Return two parts:
   - **Part A — structured edits:** a JSON array of `{"file", "old_string", "new_string", "reason"}` objects, only where `old_string` can be quoted exactly and uniquely from the drafts provided inline.
   - **Part B — narrative suggestions**, one entry per category even when the finding is "no issues" (silence reads as skipped, not clean): missed keywords/requirements, company-specific angles from the research, action-oriented reframing, tone/style issues against `03` and `02`.
4. **Never suggest fabricating** a skill, achievement, or experience. A gap is stated honestly with a suggestion to frame adjacent experience — never papered over.

The reviewer does not run verification — that's Step 5, once, by the drafter.

### Step 4 — revise (drafter)

Apply Part A edits directly with `Edit` — the reviewer's `old_string`
values were quoted from the same draft text you already have, no
re-read needed. Skip any edit whose rationale would require inventing
content. Work through every Part B category: weave keywords into
experience bullets over the profile statement where possible; verify
every company claim independently via `WebFetch`/`WebSearch` before
including it — don't trust the reviewer's research at face value;
rewrite passive/generic phrasing; apply `03-writing-style.md`'s hard
bans. Never incorporate a suggestion that would fabricate anything —
acknowledge a genuine gap and frame adjacent experience instead.

### Step 5 — render and verify (drafter, mandatory, never skip)

Never present a `.html` source as "probably fine" — page-break behavior
depends on actual rendered content, not the markup alone.

1. Render each HTML source to PDF, then verify it (`<slug>` is the `<company>-<role>-<YYMMDD>` folder created in Step 2):
   ```
   python -m rolesherpa.cli render pdf data/applications/<slug>/CV-<slug>.html data/applications/<slug>/CV-<slug>.pdf
   python -m rolesherpa.cli render verify data/applications/<slug>/CV-<slug>.pdf --pages 2 --max-pages 3 --contains "<keyword>" ...

   python -m rolesherpa.cli render pdf data/applications/<slug>/CL-<slug>.html data/applications/<slug>/CL-<slug>.pdf
   python -m rolesherpa.cli render verify data/applications/<slug>/CL-<slug>.pdf --pages 1
   ```
2. If page count fails, the CV and the cover letter are governed by different rules — don't apply one document's logic to the other:
   - **CV:** apply `05-cv-templates.md`'s relevance-weighted cutting, but check every candidate cut against its "Protected content" rules (employment continuity, top-tier quantified achievements) first.
     - *Routine cut* (doesn't touch protected content): apply it, add a one-line entry (what was cut, why) to a running list for Step 6's report, re-render, re-verify.
     - *Structural cut* (would break employment continuity or drop a protected achievement) **at 2 pages**: don't apply it — re-render/re-verify targeting 3 pages instead (still `--max-pages 3`), since this is exactly what the escape valve is for.
     - *Structural cut still required at 3 pages*: stop and ask the user, the same gate as Step 2's backtrack test — name the specific role or achievement that would have to go and why, and wait for their decision before re-rendering. Never decide this one unilaterally.
   - **Cover letter:** apply `06-cover-letter-templates.md`'s trimming order (redundant sentences, then non-keyword bullets). It stays a hard 1 page — there is no page-2 escape valve. If even a keyword-relevant bullet would have to be cut to fit, stop and ask the user per `06`'s last-resort rule before cutting it.

   Iterate until it passes — do not proceed on a failing verification.
3. **Keyword coverage:** pass the posting's required/preferred keywords (extracted in Step 0/1) as `--contains` flags. `missing_keywords` in the output is informational, not a hard failure — for each one, decide: the profile genuinely supports it (add it to an experience bullet, preferring concrete evidence over the profile statement, then re-verify) or it's a genuine gap (leave it missing — never keyword-stuff).
4. **Anti-fabrication check (this skill's responsibility, not the library's — see `design.md` D9):** re-read both final documents and confirm every factual claim traces to `data/profile/candidate-profile.md` or an independently verified company fact from Step 3/4. This is a semantic judgment call, not something `render verify`'s deterministic checks can catch.
5. **Chronology check (always run — cheap and deterministic):**
   ```
   python -m rolesherpa.cli profile audit-chronology data/profile/candidate-profile.md
   ```
   A clean result (no gaps/overlaps/impossible ranges) needs no further action. Any finding — don't resolve it inline here. Run `rolesherpa-audit/SKILL.md`'s Case A/B routing before presenting, passing this CV's path (`data/applications/<slug>/CV-<slug>.html`) so it also runs its Step 5 Case A check (a profile role silently missing from this specific CV — exactly what happened before this skill existed).

### Step 6 — present

Run the full verification checklist as a pass/fail report:

- **Factual accuracy:** every claim matches the profile; no fabricated skill/experience/achievement; company claims independently verified; contact details correct.
- **Targeting:** profile statement and bullets tailored, not generic; key requirements addressed; genuine nice-to-have matches surfaced.
- **Consistency:** CV and cover letter don't contradict each other; tone consistent; both follow their template's structure.
- **Quality:** no spelling/grammar errors; agentic tooling mention (if any) names the correct host; cover letter addressed correctly.
- **Rendering (Step 5):** exact page counts, clean text-layer extraction, keyword coverage table.
- **Content changes:** every routine cut applied during Step 5, listed with a one-line reason — state "no content was cut" explicitly if the list is empty, don't omit the line. Any structural cut goes here too, along with the user's decision from the Step 5 pause.
- **Profile updates:** any new information added to `data/profile/candidate-profile.md` during Step 2, or "no profile updates" explicitly if none came up.
- **Chronology:** the Step 5.5 audit's findings, if any, and how each was resolved via `rolesherpa-audit/SKILL.md` — or "no chronology issues found" if the audit was clean.

Then: 3-5 key tailoring decisions and why, files written, and next
steps — `rolesherpa-outcome/SKILL.md` once submitted, `rolesherpa-interview/SKILL.md` once an
interview is scheduled.

## Quality criteria

- Step 1's user gate is never skipped — no draft exists before explicit approval.
- The reviewer never re-reads files already provided inline; the drafter never re-reads files already in context.
- Nothing in either document states a skill, achievement, or company fact that isn't in the profile or independently verified.
- Verification (Step 5) runs exactly once, after all edits, and blocks presentation until it passes.
- A structural cut (breaks employment continuity or drops a protected top-tier achievement, per `05-cv-templates.md`) is never applied without pausing to ask the user first, at any page count — mirrors the Step 2 backtrack-test gate. Routine cuts don't require a pause, but always appear in Step 6's content-changes report.
- New information surfaced during drafting that isn't yet in `data/profile/candidate-profile.md` is never silently left out of the profile — the user is offered a chance to persist it (Step 2) before the workflow ends.

## Output format

See Step 6.

## Final check

Before presenting, confirm the checklist in Step 6 was actually run
against the files currently on disk — not your mental model from before
Step 4's edits. Re-read both final files once here if there's any doubt.
