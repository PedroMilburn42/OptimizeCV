# Agent Skills Specification

## Purpose
Behavioral requirements every AI-agent skill in this repo must satisfy — what each skill is required to do, with a scenario per requirement showing the expected behavior. This is the durable reference for "does this skill behave correctly," independent of any particular change-proposal history.

## Requirements
### Requirement: Skills load natively across all three hosts
Every AI-reasoning workflow SHALL be defined as `.agents/skills/<name>/SKILL.md` with YAML frontmatter (`name`, `version`, `description` with trigger phrases, `context`, `allowed-tools`), in a single location — not split between a host-specific command format and `.agents/skills/`.

#### Scenario: A skill file is discoverable by its trigger phrases
- **WHEN** a `SKILL.md` file exists under `.agents/skills/<name>/` with a `description` containing trigger phrases
- **THEN** the host loading it can match a user request against those phrases without any host-specific duplicate of the same content existing elsewhere in the repo

### Requirement: Deterministic steps delegate to the Python library
Wherever a skill needs a deterministic result (connector search/detail, document render/verify, dedup lookup), it SHALL invoke the `rolesherpa` CLI rather than instructing the model to perform the equivalent steps in prose.

#### Scenario: A scrape skill step is a CLI invocation, not a prose instruction
- **WHEN** `rolesherpa-scrape/SKILL.md` searches a job portal
- **THEN** its documented step is a `python -m rolesherpa.cli connectors search ...` invocation, not prose describing how to parse HTML or call an external API directly

### Requirement: Generated documents attribute the actual assisting host
Any skill that generates a CV or cover letter mentioning agentic coding/AI tooling SHALL name whichever host (Claude Code, Antigravity, or Codex) actually assisted for that application, read from stored profile data rather than hardcoded.

#### Scenario: A cover letter names the host recorded in the profile
- **WHEN** the stored profile data records the current host as "Antigravity" and `rolesherpa-apply/SKILL.md` drafts a cover letter mentioning agentic tooling
- **THEN** the generated text names "Antigravity", not a hardcoded "Claude Code" string

### Requirement: Fit evaluation always precedes document drafting
`rolesherpa-apply/SKILL.md` SHALL present a fit evaluation (skills match, experience match, behavioral/culture match, overall verdict) and obtain explicit user confirmation before drafting a CV or cover letter.

#### Scenario: Drafting stops without confirmation
- **WHEN** the user responds "no" to the post-evaluation "should I proceed with drafting?" prompt
- **THEN** no CV or cover letter file is created

### Requirement: Drafter and reviewer run as isolated passes
`rolesherpa-apply/SKILL.md` SHALL dispatch the content-critique reviewer as a separate agent invocation that receives drafts inline in its prompt (not via re-reading files), keeping drafting and adversarial review as isolated steps.

#### Scenario: The reviewer never re-reads draft files from disk
- **WHEN** the reviewer agent is dispatched
- **THEN** its prompt already contains the full CV and cover letter draft text, and it is not instructed to `Read` those files itself

### Requirement: Excluded portals are always surfaced
`rolesherpa-scrape/SKILL.md` SHALL always print a "Portals not included in this search" section listing every entry from `ConnectorRegistry.blocked_sources()` (and any disabled-but-installed connector) with its reason, on every run — never silently implying full coverage.

#### Scenario: A run with all connectors enabled still lists structurally blocked portals
- **WHEN** `/rolesherpa-scrape` runs with all three v1 connectors enabled
- **THEN** its output still includes the "Portals not included in this search" section naming BuscoJobs, Indeed UY, and Get on Board with their reasons

### Requirement: Generated documents pass a verification checklist before presentation
`rolesherpa-apply/SKILL.md` SHALL run a verification checklist (factual accuracy including anti-fabrication claim-diff against the profile, targeting, consistency, quality, compiled-PDF checks) after drafting and before presenting the result to the user, reporting pass/fail per item.

#### Scenario: A failed page-count check blocks presentation
- **WHEN** the rendered CV fails the exact-page-count check
- **THEN** `rolesherpa-apply/SKILL.md` iterates on the template/content rather than presenting the non-compliant PDF as final

### Requirement: The application archive path is consistent across every skill that reads or writes it
Every skill that references the per-application archive SHALL use `data/applications/<company>-<role>-<YYMMDD>/` (company and role fields internally underscore-joined; a single dash separates the company, role, and date blocks; date is the application folder's creation date) — the single folder `rolesherpa-apply/SKILL.md` creates and every other skill that touches this application (`rolesherpa-outcome/SKILL.md`, `rolesherpa-interview/SKILL.md`, `rolesherpa-setup/SKILL.md`, `rolesherpa-reset/SKILL.md`) reads or writes into. No skill SHALL reference `documents/applications/` as the archive location, and no skill SHALL reference a separate `cv/` or `cover_letters/` staging directory as the location of an active or submitted document — those directories SHALL NOT be created.

#### Scenario: Setup can read what apply and outcome wrote
- **WHEN** `rolesherpa-apply/SKILL.md` creates `data/applications/acme_corp-software_engineer-260101/CV-acme_corp-software_engineer-260101.html`, and `rolesherpa-outcome/SKILL.md` later writes `outcome.md` into that same folder
- **THEN** `rolesherpa-setup/SKILL.md`'s Path A scan of `data/applications/*/CV-*.html` finds it, and `rolesherpa-reset/SKILL.md`'s documents-reset path does not silently skip it

#### Scenario: A single folder covers the full application lifecycle
- **WHEN** an application progresses from drafted, to submitted, to interviewed
- **THEN** the CV, cover letter, job posting, outcome record, and every interview-prep pack for that application all live in the same `data/applications/<company>-<role>-<YYMMDD>/` folder created at draft time — no file is ever copied between a working-draft location and a separate archive location

### Requirement: Pasted user text is scanned against writing-style hard bans before insertion
When a user pastes text to be inserted verbatim into a CV, cover letter, or other generated document, `rolesherpa-apply/SKILL.md`'s drafting/revision step SHALL scan that text against `03-writing-style.md`'s Hard Bans list and automatically convert any purely punctuational violation (e.g. an em-dash) to a compliant equivalent before applying the edit, without asking the user to confirm the conversion. This automatic conversion SHALL NOT extend to wording changes that would alter the sentence's claimed meaning — those remain subject to the existing framing-strength flag-to-user flow.

#### Scenario: An em-dash in pasted text is converted automatically
- **WHEN** the user pastes replacement text for a CV bullet that contains an em-dash
- **THEN** the applied edit contains the em-dash converted to a comma or parenthetical instead, and the user is not asked to approve the punctuation conversion

### Requirement: Accented characters are written literally and verified against rendered output
Generated CV, cover letter, and interview-prep documents SHALL encode accented and special Spanish-language characters as literal UTF-8 text, not HTML character entities. Before presenting a rendered document to the user, its text SHALL be verified by extracting the actual rendered PDF's text layer, not by inspecting the HTML/template source alone.

#### Scenario: A generated Spanish-language CV uses literal accents
- **WHEN** `rolesherpa-apply/SKILL.md` writes a CV bullet containing the word "actúo"
- **THEN** the HTML source contains the literal character "ú", not the entity `&uacute;`

#### Scenario: Verification reads the rendered PDF, not the source
- **WHEN** `rolesherpa-apply/SKILL.md` verifies a rendered document containing accented characters
- **THEN** the verification step extracts and inspects the PDF's text layer (e.g. via the `render verify --contains` check) rather than relying on a visual read of the HTML source

### Requirement: Ambiguous quantifiable facts are confirmed with the user, never inherited silently
When drafting or evaluating fit, any quantifiable fact that depends on how it is counted (years of experience, team size, budget figures, and similar figures) and is not already stated verbatim in `data/profile/candidate-profile.md` SHALL be confirmed explicitly with the user before being used in a score, a CV, or a cover letter — it SHALL NOT be computed from other dates, assumed, or silently carried over from a prior document (an old CV, a cached score, etc.).

#### Scenario: Years of experience is confirmed, not computed
- **WHEN** `data/profile/candidate-profile.md` records a career start date but no explicit "years of experience" figure, and a CV profile statement needs a total-years claim
- **THEN** `rolesherpa-apply/SKILL.md` asks the user which figure to use rather than computing it from the start date and today's date unprompted

#### Scenario: A team-size figure from a prior document is not reused without confirmation
- **WHEN** an older CV or reference document states a team size for a role that differs from, or is absent in, `data/profile/candidate-profile.md`
- **THEN** `rolesherpa-apply/SKILL.md` asks the user to confirm the correct figure before it appears in a newly generated document

### Requirement: Overreaching bullet framing is flagged before drafting continues
`career-profile/03-writing-style.md` SHALL define a framing-strength check for CV/cover-letter bullets, and `rolesherpa-apply/SKILL.md`'s drafting step SHALL present any bullet that fails the check to the user for a keep/soften/drop decision before the reviewer pass runs.

#### Scenario: A stretched bullet is flagged, not silently drafted
- **WHEN** a drafted bullet reframes a real achievement in a way that fails `03-writing-style.md`'s framing-strength check
- **THEN** `rolesherpa-apply/SKILL.md` asks the user to keep, soften, or drop it before proceeding to the reviewer pass

### Requirement: Template verification exercises the template's actual styling
`rolesherpa-add-template/SKILL.md`'s mandatory test-render step SHALL pass the template's CSS file to `render pdf` via `--css` whenever the template being verified ships one, so the verification gate cannot pass unstyled output.

#### Scenario: A template with separate CSS is verified with its styling applied
- **WHEN** a custom template registered via `rolesherpa-add-template/SKILL.md` ships an HTML file plus a separate CSS file
- **THEN** the mandatory test-render command includes `--css <path-to-css>`, not just the HTML file

### Requirement: A skill's allowed-tools frontmatter grants what its own body requires
Every `SKILL.md`'s `allowed-tools` frontmatter field SHALL include every tool its body instructs the model to use.

#### Scenario: expand can execute its own Edit step
- **WHEN** `rolesherpa-expand/SKILL.md`'s Step 5 instructs an `Edit`-only update to a career-profile file
- **THEN** `rolesherpa-expand/SKILL.md`'s `allowed-tools` frontmatter includes `Edit`

### Requirement: Portal access checks cover Terms of Service, not just robots.txt
`rolesherpa-add-portal/SKILL.md`'s access-check step SHALL verify robots.txt, the absence of a login wall, AND that the portal's Terms of Service do not prohibit automated access, before scaffolding a connector.

#### Scenario: A portal whose ToS prohibits scraping is declined
- **WHEN** a candidate portal's Terms of Service explicitly prohibit automated access, even if robots.txt does not disallow the relevant paths
- **THEN** `rolesherpa-add-portal/SKILL.md` declines to scaffold a connector for it

### Requirement: Interview outcomes feed the skill that actually consumes them
`rolesherpa-interview/SKILL.md` SHALL direct post-interview outcome logging toward the skill that mines resolved-application data for calibration (`rolesherpa-setup/SKILL.md`), not toward a skill that does not read it.

#### Scenario: Closing the loop points at the real consumer
- **WHEN** `rolesherpa-interview/SKILL.md`'s Step 5 tells the user what to do after an interview concludes
- **THEN** it names `rolesherpa-setup/SKILL.md`'s calibration step as the consumer of the resulting outcome data, not `rolesherpa-upskill/SKILL.md`

### Requirement: Scrape never presents expired, closed, or out-of-range postings
`rolesherpa-scrape/SKILL.md` SHALL skip postings with expired deadlines or marked closed, and postings outside the configured commute/location range, before presenting results — and SHALL flag any posting whose date cannot be determined as "date unknown" rather than silently including or excluding it.

#### Scenario: A closed posting never reaches the results table
- **WHEN** a connector returns a posting marked closed or past its application deadline
- **THEN** `rolesherpa-scrape/SKILL.md` excludes it from the presented results

#### Scenario: An undated posting is flagged, not silently dropped or kept
- **WHEN** a posting's publish date cannot be determined from the connector's response
- **THEN** `rolesherpa-scrape/SKILL.md` includes it in the results but labels it "date unknown"

### Requirement: Reset's blank-template step is self-contained
`rolesherpa-reset/SKILL.md` SHALL restore `data/profile/candidate-profile.md` and `data/profile/behavioral-profile.md` by copying the corresponding file from `templates/profile/` (`candidate-profile.md`, `behavioral-profile.md`) verbatim, not by inferring a blank state from those files' current (non-blank) content, and not by maintaining a separately-defined inline skeleton.

#### Scenario: Reset produces a known-clean copy regardless of prior drift
- **WHEN** `rolesherpa-reset/SKILL.md` resets `data/profile/candidate-profile.md` or `data/profile/behavioral-profile.md`
- **THEN** the resulting file is byte-identical to `templates/profile/candidate-profile.md` or `templates/profile/behavioral-profile.md` respectively, independent of what sections the file held before the reset

### Requirement: Personal profile and search data lives outside the skills tree
`candidate-profile.md`, `behavioral-profile.md`, and `search-queries.md` SHALL live under `data/profile/` (gitignored), never inside `.agents/skills/` or `.claude/skills/`. A skill needing this data SHALL reference `data/profile/<file>` directly; no skill SHALL read or write a `career-profile/<file>` or `rolesherpa-scrape/search-queries.md` path for this data.

#### Scenario: A skill reads the candidate profile from its data location, not the skill tree
- **WHEN** `rolesherpa-apply/SKILL.md` needs the candidate's profile to evaluate a job posting
- **THEN** it reads `data/profile/candidate-profile.md`, not any path under `.agents/skills/` or `.claude/skills/`

#### Scenario: The old skill-tree locations carry a pointer, not the data
- **WHEN** a user or agent opens `career-profile/candidate-profile.md`, `career-profile/behavioral-profile.md`, or `rolesherpa-scrape/search-queries.md`
- **THEN** they find a short stub pointing at the corresponding file under `data/profile/`, not the actual profile content and not a silently-missing file

### Requirement: Setup bootstraps profile data from tracked templates on a fresh checkout
`rolesherpa-setup/SKILL.md` SHALL copy the corresponding file from `templates/profile/` to `data/profile/` for any of `candidate-profile.md`, `behavioral-profile.md`, `search-queries.md` that doesn't already exist, before beginning Path A/B/C data collection.

#### Scenario: A fresh checkout with no data/profile/ files bootstraps cleanly
- **WHEN** `rolesherpa-setup/SKILL.md` runs and `data/profile/candidate-profile.md` does not yet exist
- **THEN** it is created from `templates/profile/candidate-profile.md` before `rolesherpa-setup/SKILL.md` asks the user anything or writes collected data into it

#### Scenario: An existing profile is never overwritten by the bootstrap step
- **WHEN** `rolesherpa-setup/SKILL.md` runs and `data/profile/candidate-profile.md` already exists with real data
- **THEN** the bootstrap step does not copy over it or reset any of its content
