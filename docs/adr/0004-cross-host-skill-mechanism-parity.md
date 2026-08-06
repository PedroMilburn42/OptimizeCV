# `allowed-tools` and `context: fork` are not portable across the three hosts

`PROJECT_BRIEF.md` §4a and `AGENTS.md` assert that RoleSherpa's skills
work natively across Claude Code, Antigravity, and Codex CLI via the
`.agents/skills/` + `.claude/skills/` mirror. ADR 0003 verified this for
*discovery* — all three hosts find and trigger the right skill by
description/trigger phrase. This ADR examines a narrower, previously
unverified question: are the specific frontmatter mechanisms
RoleSherpa's skills actually rely on — `allowed-tools` (10 of 11
skills) and `context: fork` (`rolesherpa-setup/SKILL.md` only) —
equally portable, or only enforced by Claude Code?

**What was actually verified** (primary sources, checked directly, not
assumed):

- **The open Agent Skills specification** (`agentskills.io/specification`,
  fetched directly): its frontmatter table defines exactly six fields —
  `name`, `description`, `license`, `compatibility`, `metadata`,
  `allowed-tools`. `context` does not appear anywhere in the spec — it
  is not an optional/experimental field of the open standard, it simply
  isn't part of it. `allowed-tools` is real but explicitly flagged:
  *"Experimental. Support for this field may vary between agent
  implementations."*
- **Antigravity's own skills documentation** (`antigravity.google/docs/skills`,
  fetched directly): documents only `name` and `description` as skill
  frontmatter fields. Neither `allowed-tools` nor `context` is
  mentioned as something Antigravity's skill loader reads.
- **Codex CLI's own skills documentation** (`learn.chatgpt.com/docs/build-skills`,
  fetched directly): same pattern — only `name` and `description` are
  documented as required. Additional configuration (invocation
  preferences, tool dependencies) goes through a separate
  `agents/openai.yaml` file, not `SKILL.md` frontmatter. Neither
  `allowed-tools` nor `context` appears.
- **Secondary corroboration** (a hands-on Antigravity skills guide,
  RuleSell): states plainly that Claude Code (and OpenClaw) enforce the
  `allowed-tools` restriction, while other agents silently ignore it —
  each host uses its own tool-access/approval model instead.
- **Subagent dispatch capability check** (both hosts' own docs): unlike
  `allowed-tools`/`context`, the underlying *capability* referenced in
  skill bodies via prose ("dispatch a general-purpose agent") does
  exist on both other hosts, just under different names — Codex CLI has
  `spawn_agent`/`send_message`/`wait_agent`, Antigravity has
  `invoke_subagent`/`start_subagent`. Since RoleSherpa's skills
  reference this in natural-language instructions rather than a literal
  API call, this specific gap is expected to be low-risk in practice.

**Decision:** keep `allowed-tools` and `context: fork` in the affected
skills' frontmatter as-is — removing them would regress real, currently
working protection under Claude Code (the host most of this project's
actual usage runs on). No skill-body rewrite is needed. What changes is
documentation: this ADR records that these two fields are a
Claude-Code-only guarantee, not a cross-host one, so a future reader
doesn't extend ADR 0003's discovery-parity finding to cover them.

## Consequences

- On Antigravity and Codex CLI, `rolesherpa-setup/SKILL.md`'s
  `context: fork` isolation is silently ignored — onboarding runs
  inline in the main conversation instead of in a forked subagent. The
  documented Task steps are still followed either way, so this is a
  context-window hygiene difference, not a correctness regression.
- On Antigravity and Codex CLI, the `allowed-tools` restriction
  declared by the other 10 skills is not enforced by that field itself.
  Each host substitutes its own tool-approval model. Concretely: the
  narrow `Bash(rm -f documents/cv/*)`-style allowlist
  `rolesherpa-reset/SKILL.md` declares to bound a destructive skill is
  a Claude-Code-specific guarantee — Antigravity/Codex users get
  whatever native tool-approval behavior that host provides, not this
  project's declared scope.
- Tool names referenced in skill bodies (`Agent`, `AskUserQuestion`,
  `WebFetch`, `WebSearch`) are prose a model interprets, not literal
  API calls the spec routes by name — both other hosts have their own
  real equivalents for subagent dispatch and web fetch/search, so no
  functional gap is expected there.
- Not yet done, and a reasonable follow-up if this project ever
  prioritizes non-Claude-Code usage: an empirical run of
  `rolesherpa-setup` and `rolesherpa-reset` under Antigravity and Codex
  CLI to directly observe (not just infer from docs) whether isolation
  and tool-approval behave as this ADR predicts.
