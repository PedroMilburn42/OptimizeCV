# Changelog

All notable changes to this project are documented in this file.

## [0.1.0] — Initial public release

- Fit evaluation, drafting (CV + cover letter), isolated adversarial review,
  and verification workflow via `rolesherpa-apply`.
- Job-portal connectors: LinkedIn, Freehire, Computrabajo Uruguay.
- Deterministic document pipeline: WeasyPrint HTML/CSS → PDF rendering,
  `pypdf`-based verification (page count, keyword coverage, text-layer
  extraction).
- Chronology auditing (`rolesherpa-audit`) for employment gaps, overlaps, and
  impossible date ranges.
- Skills load natively across Claude Code, Google Antigravity, and OpenAI
  Codex CLI via the open Agent Skills format.
