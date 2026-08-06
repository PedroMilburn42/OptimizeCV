"""rolesherpa-expand/SKILL.md's Step 5 instructs an Edit-only update to
a career-profile file, but its frontmatter allowed-tools list didn't
include Edit - the skill couldn't execute its own instructions.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
EXPAND_SKILL = REPO_ROOT / ".agents" / "skills" / "rolesherpa-expand" / "SKILL.md"


def _allowed_tools(text):
    match = re.search(r"^allowed-tools:\s*(.+)$", text, re.MULTILINE)
    assert match, "no allowed-tools frontmatter field found"
    return match.group(1)


def test_expand_body_mentions_edit():
    text = EXPAND_SKILL.read_text()
    assert "`Edit`" in text or "Edit tool" in text


def test_expand_allowed_tools_grants_edit():
    text = EXPAND_SKILL.read_text()
    assert "Edit" in _allowed_tools(text)
