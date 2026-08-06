from rolesherpa.domain.host import detect_host


def test_detects_claude_code(monkeypatch):
    monkeypatch.delenv("CODEX_SANDBOX", raising=False)
    monkeypatch.delenv("ANTIGRAVITY_AGENT", raising=False)
    monkeypatch.setenv("CLAUDECODE", "1")
    assert detect_host() == "Claude Code"


def test_detects_codex(monkeypatch):
    monkeypatch.delenv("CLAUDECODE", raising=False)
    monkeypatch.delenv("ANTIGRAVITY_AGENT", raising=False)
    monkeypatch.setenv("CODEX_SANDBOX", "seatbelt")
    assert detect_host() == "Codex"


def test_detects_antigravity(monkeypatch):
    monkeypatch.delenv("CLAUDECODE", raising=False)
    monkeypatch.delenv("CODEX_SANDBOX", raising=False)
    monkeypatch.setenv("ANTIGRAVITY_AGENT", "1")
    assert detect_host() == "Antigravity"


def test_returns_none_when_no_signal_present(monkeypatch):
    monkeypatch.delenv("CLAUDECODE", raising=False)
    monkeypatch.delenv("CODEX_SANDBOX", raising=False)
    monkeypatch.delenv("ANTIGRAVITY_AGENT", raising=False)
    assert detect_host() is None


def test_claude_code_takes_precedence_when_multiple_signals_present(monkeypatch):
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CODEX_SANDBOX", "seatbelt")
    assert detect_host() == "Claude Code"


def test_empty_string_value_does_not_count_as_present(monkeypatch):
    monkeypatch.delenv("CODEX_SANDBOX", raising=False)
    monkeypatch.delenv("ANTIGRAVITY_AGENT", raising=False)
    monkeypatch.setenv("CLAUDECODE", "")
    assert detect_host() is None
