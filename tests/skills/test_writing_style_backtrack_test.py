"""The reference implementation's 03-writing-style.md defines an "interview
backtrack test" for CV/cover-letter bullets - reframing a real achievement
is fine, inventing or implying experience that isn't there is not - plus a
user-facing keep/soften/drop gate for anything that falls in the
"flag it" zone. RoleSherpa's port dropped this mechanism entirely.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

WRITING_STYLE = REPO_ROOT / ".agents" / "skills" / "career-profile" / "03-writing-style.md"
APPLY_SKILL = REPO_ROOT / ".agents" / "skills" / "rolesherpa-apply" / "SKILL.md"


def test_writing_style_defines_a_backtrack_test():
    text = WRITING_STYLE.read_text()
    assert "backtrack test" in text.lower()


def test_writing_style_backtrack_test_names_its_three_tiers():
    text = WRITING_STYLE.read_text().lower()
    assert "ok" in text
    assert "flag" in text
    assert "never" in text


def test_apply_gates_flagged_bullets_on_a_keep_soften_or_drop_decision():
    text = APPLY_SKILL.read_text().lower()
    assert "keep" in text and "soften" in text and "drop" in text
