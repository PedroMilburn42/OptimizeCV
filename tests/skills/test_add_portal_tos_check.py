"""The reference implementation's add-portal checks robots.txt, login-walls,
AND whether the portal's Terms of Service prohibit automated access.
RoleSherpa's port dropped the ToS check - robots.txt silence doesn't mean
the ToS permit scraping.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ADD_PORTAL = REPO_ROOT / ".agents" / "skills" / "rolesherpa-add-portal" / "SKILL.md"


def test_access_check_step_mentions_robots_txt_and_login_wall():
    text = ADD_PORTAL.read_text()
    assert "robots.txt" in text
    assert "login" in text.lower()


def test_access_check_step_also_mentions_terms_of_service():
    text = ADD_PORTAL.read_text()
    assert "Terms of Service" in text or "terms of service" in text.lower()
