# RoleSherpa

Personal job-search automation for Carlos Ibarra (AI Engineer, Uruguay-based, targeting Uruguay + remote roles). Evaluates job postings, drafts tailored CVs and cover letters, and preps for interviews. See `PROJECT_BRIEF.md` (where present — see this repo's README for whether it ships here) for the confirmed requirements this project was built from.

This is a personal-use project that doubles as an AI Engineer portfolio piece. All generated material (code, docs, comments, commit messages) must be written in English.

## Stack and architecture

- **Runtime model:** interactive-only, human-initiated from inside Claude Code, Antigravity, or Codex CLI — no scheduler, no headless driving, no web UI. See `docs/adr/` for the architecture decisions.
- **AI-reasoning workflows** (fit evaluation, CV/cover-letter drafting, interview prep, upskill analysis) live as `.agents/skills/<name>/SKILL.md` (Antigravity, Codex CLI) **and** are mirrored byte-for-byte at `.claude/skills/<name>/SKILL.md` (Claude Code only reads `.claude/skills/`, confirmed against official docs — it does not discover `.agents/skills/`). `tests/skills/test_skill_mirrors_stay_in_sync.py` fails the suite if the two trees drift; re-copy `.agents/skills/<name>/` over `.claude/skills/<name>/` after editing a skill.
- **Deterministic logic** (job-portal connectors, document render+verify pipeline, application tracker/dedup) is a real Python package under `src/rolesherpa/`, hexagonal (ports & adapters), TDD from the start, storage as JSON/CSV — no SQLite, no database engine.
- **Portal connectors (v1):** LinkedIn, Freehire, Computrabajo Uruguay only, rewritten in Python. See `PROJECT_BRIEF.md` §5 and `docs/validation-report.md` for the excluded portals and why.
- **Tooling:** Python 3.14 via `uv`, `httpx` + `selectolax` for connectors, `weasyprint` + `pypdf` for the document pipeline, `pyyaml` for the connector registry config, `pytest` for TDD.

## Agent skills

### Issue tracker

Issues live as GitHub issues on `c-ibarra/RoleSherpa`. See `docs/agents/issue-tracker.md`.

### Domain docs

Single-context layout — `CONTEXT.md` + `docs/adr/` at the repo root, created lazily as concepts get resolved. See `docs/agents/domain.md`.

## `README.md` standard

The repo-root `README.md` is the project's front door — for a recruiter,
a hiring manager, or an international collaborator, it's the first (and
often only) thing they read before deciding whether to look further. It
must always be in English (see the rule above), written in natural,
professional prose — not a literal translation of anything drafted in
another language — and scannable in under two minutes.

**Required sections, at minimum:**

- Project title
- Elevator pitch — the problem this solves, in under 30 seconds of reading
- Key Features
- Architecture overview — a diagram, not a screenshot (RoleSherpa has no
  UI to screenshot; see "Runtime model" above)
- Technology Stack
- Installation
- Quick Start
- Usage Examples
- Common Use Cases
- Project Structure
- Configuration
- Roadmap
- Testing
- Contributing
- License
- FAQ
- Contact information
- **"Why this project?"** — the motivation and the problem it solves
- **"What this project demonstrates"** — written for recruiters/hiring
  managers, calling out the technical competencies actually evidenced
  (AI/agentic workflows, LLM integration, hexagonal architecture, TDD,
  spec-driven development, documentation discipline, etc.)
- **"Design Decisions"** — the main architecture decisions and the
  trade-offs weighed while building, in enough detail to show real
  engineering judgment, not just a features list

**What it must never contain:** Carlos's personal contact details
(email, phone) — link to his public LinkedIn instead — and nothing
about real, in-progress job applications (target companies, specific
postings, tracker contents). See `data/README.md` for why: this project
already had a real PII leak caused by personal data landing in a
tracked file (see the `decouple-profile-data-from-skills` change and
`tests/skills/test_profile_data_outside_skills_tree.py`); the README is
exactly the kind of high-visibility, always-tracked file where that
mistake matters most.

**Quality bar:** a recruiter can scan it in under two minutes and come
away knowing what the project does and why it's impressive; a new user
can install and run it end-to-end using only the README, no other docs
required; it follows the conventions of well-regarded open-source
READMEs rather than reading like an internal spec. It should also
reference `PROJECT_BRIEF.md` (the original requirements/planning
record — frozen, historical, not updated after initial scaffolding) and
this file, `AGENTS.md` (the living project conventions), for anyone who
wants to go deeper.
