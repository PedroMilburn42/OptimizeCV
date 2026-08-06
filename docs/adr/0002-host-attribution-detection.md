# Dynamic tool attribution: environment-variable detection, ask-and-store as fallback

`PROJECT_BRIEF.md` §4a point 3 requires generated documents to name
whichever host actually assisted (Claude Code, Antigravity, or Codex)
when mentioning agentic tooling — replacing the reference
implementation's hardcoded "Claude Code" string, since RoleSherpa runs
under all three. The
initial design (first draft of `design.md` D7) proposed asking the user
once during `rolesherpa-setup/SKILL.md`, since no *confirmed, documented*
environment signal was known to distinguish the three hosts.

That draft was revisited with a quick empirical check on the machine
where all three CLIs are installed, rather than shipping the
ask-always fallback as the primary mechanism on an untested
assumption either way:

- **Claude Code:** `CLAUDECODE=1` is **live-confirmed** — present in this repo's own session environment (`env | grep CLAUDECODE`), alongside `CLAUDE_CODE_ENTRYPOINT` and others.
- **Codex CLI:** `strings` on the installed binary (`codex` v0.133.0, resolved through its Nix wrapper to `.codex-wrapped`) contains the literal string `CODEX_SANDBOX` among a family of `CODEX_*` names (`CODEX_HOME`, `CODEX_THREAD_ID`, `CODEX_SANDBOX_NETWORK_DISABLED`, ...) — a named marker whose purpose (flagging that a command runs inside Codex's sandbox) matches exactly what's needed here.
- **Antigravity:** `strings` on the installed `agy` binary (v1.1.7) contains `ANTIGRAVITY_AGENT`, `ANTIGRAVITY_CONVERSATION_ID`, `ANTIGRAVITY_PROJECT_ID` — same category of evidence.

Static-string presence in a binary is not the same confidence level as
`CLAUDECODE`'s live confirmation — no Codex or Antigravity agent
session was actually run in this project to observe the variable set
in a live subprocess. The decision made here is deliberately calibrated
to that gap.

**Decision:** `detect_host()` (`src/rolesherpa/domain/host.py`) checks
`CLAUDECODE`, `CODEX_SANDBOX`, `ANTIGRAVITY_AGENT`, in that order, and
returns the first match. `rolesherpa-setup/SKILL.md` calls this first and only
falls back to asking the user — storing the answer in
`data/profile/candidate-profile.md`'s "Assisting tool" field, with a
per-invocation override available — when none of the three match.

## Consequences

- If `CODEX_SANDBOX` or `ANTIGRAVITY_AGENT` turn out not to be set the way their presence in the binary suggests (e.g. only set in some execution modes, or named differently in the version actually installed on a user's machine), `detect_host()` simply returns `None` and the system degrades to the ask-and-store path — it never silently mis-attributes a document to the wrong host.
- The first real skill run under Codex or under Antigravity should confirm the corresponding variable empirically (`env | grep -E 'CODEX_|ANTIGRAVITY_'` from within a running skill) and this ADR should be updated with the result — live-confirmed like `CLAUDECODE`, or corrected if the variable differs.
- `data/profile/candidate-profile.md` still carries the "Assisting tool" field even though detection is now the primary path — it doubles as the override for the rare case of switching hosts mid-project, and as the storage location if detection ever needs to fall back.
