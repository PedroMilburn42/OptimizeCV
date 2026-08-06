"""Detects which AI coding host is currently running a skill, for dynamic
tool attribution in generated documents (design.md D7).

CLAUDECODE is live-verified. CODEX_SANDBOX and ANTIGRAVITY_AGENT are
confirmed present as literal strings in their installed CLI binaries
(strings inspection) but not yet observed live in a running agent session
— if either assumption proves wrong, detect_host() simply returns None
and the caller falls back to asking the user (never mis-attributes).
"""

import os

_ENV_SIGNALS = [
    ("CLAUDECODE", "Claude Code"),
    ("CODEX_SANDBOX", "Codex"),
    ("ANTIGRAVITY_AGENT", "Antigravity"),
]


def detect_host() -> str | None:
    for env_var, host_name in _ENV_SIGNALS:
        if os.environ.get(env_var):
            return host_name
    return None
