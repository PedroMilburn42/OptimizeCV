# Contributing

RoleSherpa is a personal project shared publicly as a portfolio piece. I'm not
actively seeking contributions, and there's no roadmap of "help wanted"
issues — but the code is MIT-licensed, so forking, adapting, and opening pull
requests are all welcome.

## Before opening a pull request

- Small, focused fixes (a bug, a broken link, a typo, a test gap) are the
  easiest to review and merge.
- Larger changes (a new connector, a new skill, an architectural change) are
  more likely to get merged if you open an issue first to discuss the
  approach — this project follows a spec-driven, test-first process (see
  [`AGENTS.md`](AGENTS.md)), and a shared understanding of the "why" before
  the "what" avoids wasted work on both sides.
- Match the existing conventions: TDD (a failing test before the
  implementation), hexagonal separation between the deterministic Python
  layer (`src/rolesherpa/`) and the AI-reasoning layer (`.agents/skills/`),
  and an ADR (`docs/adr/`) for any non-obvious decision.

## Development setup

```bash
git clone https://github.com/c-ibarra/rolesherpa-portfolio.git
cd rolesherpa-portfolio
uv sync
uv run pytest
```

## Reporting issues

Bug reports and feature suggestions are welcome via GitHub Issues. Since this
project handles personal data (a candidate's own profile, job-search state),
please don't include any of your own real personal data in an issue —
describe the behavior, not the specific data that triggered it.
