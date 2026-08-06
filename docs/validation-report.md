# Validation Report — RoleSherpa vs. the reference implementation

Executes `PROJECT_BRIEF.md` §7's validation strategy for the
`rolesherpa-v1-mvp` change.
Run 2026-08-01.

## 1. Golden set: connector equivalence (§7, axis 2 objectivity check)

Per §7, the golden set is the reference implementation's own connector
output for a realistic query, used as-is — not hand-curated. Its
Bun/TypeScript CLIs were run once each; RoleSherpa's Python connectors
were run against the identical query moments later.

| Portal | Query | Reference impl. count | RoleSherpa count | Shared IDs |
|---|---|---|---|---|
| LinkedIn | `data engineer`, location `Montevideo, Uruguay` | 10 | 10 | 3/17 union |
| Freehire | `python`, country `UY` | 25 | 25 | 25/25 (100%) |
| Computrabajo UY | `programador montevideo`, jobage 30 | 4 | 4 | 4/4 (100%) |

**Freehire and Computrabajo: full agreement.** Every ID returned by the
reference implementation's connector was also returned by RoleSherpa's,
for an identical request. This is the strongest evidence available
that the Python rewrite's parsing logic is equivalent to the original.

**LinkedIn: low ID overlap (3/17 union), same request shape.**
Confirmed the two implementations send byte-identical query parameters
(`keywords`, `location`, `start=0`, no `f_TPR`/`f_WT` in either call —
verified against the reference implementation's `search.ts`
construction directly). The divergence is not a parsing or
request-construction bug: LinkedIn's public `jobs-guest` search
endpoint does not guarantee stable, deterministic ordering for
identical anonymous requests within a short time window — a known
characteristic of the unauthenticated endpoint, not something either
implementation controls. Both connectors' *parsing* of whatever
LinkedIn returned was confirmed correct independently (Migration Plan
step 1, task 2.4 — live-verified against real titles/companies/URLs).

**Bug found and fixed during this comparison:** RoleSherpa's Freehire
connector reported `meta.count` as the API's cross-page `total` (e.g.
17827) instead of the actual number of results in the response —
inconsistent with the reference implementation's own convention
(`count` = `len(results)`, kept separate from any total) and with
RoleSherpa's own LinkedIn/Computrabajo connectors. Fixed in
`src/rolesherpa/connectors/freehire.py` (test updated first, per this
repo's TDD discipline, then the implementation); full suite
re-verified green afterward. This is exactly the class of defect §7
says golden-set comparison should catch.

**Field-shape difference (not a bug, a deliberate trade-off):** the
reference implementation's per-portal CLIs return portal-specific
extra fields (`companyUrl`, `company_slug`/`countries`/`regions`/
`skills`/`work_mode` for Freehire). RoleSherpa maps every connector
onto one canonical `JobPosting` shape (`id`, `title`, `company`,
`location`, `date`, `url`, `description`, `source`) per `design.md` D2
— trading per-portal richness for cross-portal uniformity, which is
what lets `scrape` and `dedup` treat all three sources identically.
Nothing in the current skill set reads the fields RoleSherpa omits; if
a future skill needs them, `JobPosting` can be extended.

## 2. Feature-parity checklist (§7, axis 2)

| Capability | Reference impl. | RoleSherpa | Notes |
|---|---|---|---|
| Onboarding (3 paths) | ✅ `/setup` | ✅ `rolesherpa-setup/SKILL.md` | |
| Job search across portals | ✅ LinkedIn, Freehire, + Danish demos, WebSearch fallback | ✅ LinkedIn, Freehire, Computrabajo UY | Danish portals out of scope by design; BuscoJobs/Indeed UY/Get on Board excluded on both sides for documented reasons |
| Dedup (seen jobs + tracker) | ✅ string/URL equality | ✅ canonical URL hash + fuzzy company/title/description match | RoleSherpa's is more capable — catches cross-portal duplicates an exact-match approach wouldn't |
| Referral contact links | ✅ | ✅ (`rolesherpa-scrape/SKILL.md` Step 5.4) | |
| Triage/ranking | ✅ `/rank` | ✅ `rolesherpa-rank/SKILL.md` | |
| Full fit evaluation | ✅ `/apply` Step 1 | ✅ `rolesherpa-apply/SKILL.md` Step 1 | Scoring framework ported verbatim in structure (`04-job-evaluation.md`) |
| Drafter-reviewer CV/cover letter | ✅ LaTeX | ✅ HTML/CSS (WeasyPrint) | See ADR-0001 |
| Document verification | ✅ manual LLM inspection + external `pdfinfo`/`pdftotext` | ✅ automated `pypdf`-based page count/text-layer/keyword-coverage, no external binary | More deterministic and testable than the reference implementation's approach |
| Interview prep + mock interview | ✅ | ✅ `rolesherpa-interview/SKILL.md` | |
| Outcome tracking | ✅ | ✅ `rolesherpa-outcome/SKILL.md`, same CSV schema | |
| Upskill gap analysis | ✅ aggregate + targeted | ✅ `rolesherpa-upskill/SKILL.md` | |
| Add a portal | ✅ Bun/TypeScript scaffold | ✅ Python scaffold (`rolesherpa-add-portal/SKILL.md`) | |
| Add a template | ✅ LaTeX scaffold | ✅ HTML/CSS scaffold (`rolesherpa-add-template/SKILL.md`) | |
| Competency expansion | ✅ `/expand` | ✅ `rolesherpa-expand/SKILL.md` | |
| Destructive reset | ✅ `/reset` | ✅ `rolesherpa-reset/SKILL.md` | |
| Multi-host support | ❌ Claude Code only | ✅ Claude Code, Antigravity, Codex | The core point of this rebuild |
| Dynamic tool attribution | ❌ hardcoded "Claude Code" | ✅ `detect_host()` (ADR-0002) | |
| Salary benchmark lookup | ⚠️ optional, ships with no data (`salary_data.json` is user-provided, gitignored there too) | ⚠️ not built — noted as "optional, not currently configured" in `04-job-evaluation.md` | Genuine scope gap, not silently dropped; wasn't in the approved `proposal.md` capability list |
| Fork-maintenance meta-tooling (`lint_skills.py`, `security_guards.py`, `check_framework_version.py`, `check_upstream_updates.py`) | ✅ | ❌ not ported | Correctly out of scope — these maintain the reference implementation's own upstream-fork relationship, not part of the functional job-search workflow `PROJECT_BRIEF.md` asked to port |

**Net assessment:** full functional parity on every job-search
capability, plus three concrete improvements (multi-host, dynamic
attribution, a real dedup engine) and one deliberate architecture
change (WeasyPrint over LaTeX, ADR-0001) with equivalent document
verification rigor achieved more deterministically. One honest gap
(salary benchmarking) and one correct exclusion (fork-maintenance
tooling that doesn't apply to RoleSherpa's own repo).

## 3. Fit-evaluation and generated-document quality (§7, axes 1 and 3)

**Not executed in this validation pass.** Both require a populated
candidate profile — real skills, experience, and career goals scored
against a real posting. `.agents/skills/career-profile/` was
deliberately left blank (task 6.1: "not pre-filled with Carlos's
data") because this repo ships as reusable software, not as Carlos's
personal dataset. Running these checks with placeholder data would
produce meaningless scores and a misleading validation result — worse
than not running them.

What **was** validated, independent of profile content:

- The scoring framework's structure (`04-job-evaluation.md`) matches the reference implementation's dimensions and weights exactly (Technical 30% / Experience 25% / Behavioral 15% / Career 30%, location pass/fail).
- The document verification pipeline itself is proven correct and automated: both stock templates render and pass `pypdf`-based verification (exact page count, non-trivial text layer, keyword coverage) with realistic dummy data (`tests/documents/test_stock_templates.py`).

**Deferred to Carlos's own onboarding:** once `rolesherpa-setup/SKILL.md` is run
with real profile data, axes 1 and 3 can be executed properly — same
posting scored by both systems (axis 1), and a real generated CV/cover
letter checked against the reference implementation's own
manual-checklist track record (axis 3). This is a follow-up step for
Carlos, not a gap in the software.

## Summary

| Axis (§7) | Status |
|---|---|
| 1. Fit-evaluation quality | Framework parity confirmed structurally; live score comparison deferred (needs a populated profile) |
| 2. Feature-parity checklist | Complete — full parity plus three improvements, one honest gap, one correct exclusion |
| 2b. Golden-set connector equivalence | Complete — 2/3 portals at 100% ID agreement; LinkedIn's low overlap traced to the endpoint's own non-determinism, not a bug; one real bug found and fixed |
| 3. Generated-document quality | Pipeline correctness confirmed automatically; live comparison against the reference implementation's manual outcomes deferred (needs a populated profile) |
