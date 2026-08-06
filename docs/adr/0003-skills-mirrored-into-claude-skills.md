# Skills mirrored into `.claude/skills/`, not `.agents/skills/` alone

`PROJECT_BRIEF.md` §4a asserted that Claude Code, Antigravity, and Codex
CLI all natively discover skills from `.agents/skills/` — the basis for
building all eleven of RoleSherpa's skills in one shared location.
Discovered live, via a real user report ("restarted Claude Code, `/setup`
not recognized") followed by primary-source verification, that this was
only two-thirds true.

**What was actually verified** (not assumed — official docs and a
hands-on-tested source, checked directly):

- **Codex CLI** (`learn.chatgpt.com/docs/build-skills`, official): `.agents/skills/` at the repo root and `$HOME/.agents/skills/`, scanned from cwd up to the repo root. Confirmed.
- **Antigravity** (Mete Atamel, hands-on tested across AGY/AGY CLI/AGY IDE, July 2026): `<workspace-root>/.agents/skills/`. Confirmed.
- **Claude Code** (`code.claude.com/docs/en/skills.md`, official): only `~/.claude/skills/` and `.claude/skills/` (project-level). `.agents/` does not appear anywhere in Claude Code's documentation. Typing `/setup` literally is a slash-command lookup, which — like skill auto-invocation — only reads `.claude/skills/`/`.claude/commands/`.

An earlier research pass (a subagent checking Claude Code docs only) had
concluded `.agents/skills/` "isn't a Claude Code convention" and implied
the whole cross-host premise was broken. That framing was too broad —
re-verifying Antigravity and Codex specifically against dated,
primary sources showed both were fine as originally built. Worth noting
for future investigations in this repo: a single subagent's research
pass answering the literal question asked doesn't mean it checked the
adjacent claims that motivated the question.

**Decision:** keep `.agents/skills/` as the canonical source (it
already serves Antigravity and Codex correctly), and mirror every skill
directory byte-for-byte into `.claude/skills/` for Claude Code. This
mirrors the same pattern other multi-host CLI scaffolding tools use to
generate one copy of skill files per supported host — real per-host
duplication, not symlinks (symlinks need Developer Mode/admin on Windows and
special git config, ruled out earlier in this project for the same
reason `CLAUDE.md`/`AGENTS.md` aren't symlinked) and not thin pointer
files (a pointer wouldn't give Claude Code the actual trigger-phrase
description or instructions needed to invoke the skill).

## Consequences

- Every skill edit must be applied to both `.agents/skills/<name>/` and `.claude/skills/<name>/` — a real, ongoing duplication cost.
- `tests/skills/test_skill_mirrors_stay_in_sync.py` makes drift a test failure, not a silent bug: it diffs every file in both trees and fails the suite if they disagree.
- If Codex's `/setup`-style literal slash invocation turns out to behave differently from its "implicit invocation via description match" path (not fully verified here — search results were inconsistent on this specific point), that's a smaller follow-up, not a repeat of this ADR's finding.
