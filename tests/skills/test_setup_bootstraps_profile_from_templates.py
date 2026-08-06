"""Personal profile/search data used to live inside the skill tree
(career-profile/01-candidate-profile.md, 02-behavioral-profile.md,
rolesherpa-scrape/search-queries.md), tracked in git. That coupling
caused a real PII leak in this project's history. Moving the data to
gitignored data/profile/ means a fresh checkout starts with nothing
there - rolesherpa-setup/SKILL.md must explicitly bootstrap each file
from templates/profile/ before it asks the user anything, or a fresh
clone silently has no candidate-profile.md at all. Today this only
"works" by accident, via the old tracked-placeholder content this
change removes.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SETUP_SKILL = REPO_ROOT / ".agents" / "skills" / "rolesherpa-setup" / "SKILL.md"

PROFILE_FILES = ["candidate-profile.md", "behavioral-profile.md", "search-queries.md"]


def test_setup_documents_copying_each_template_into_data_profile():
    text = SETUP_SKILL.read_text()
    for filename in PROFILE_FILES:
        assert f"templates/profile/{filename}" in text, (
            f"setup does not reference templates/profile/{filename}"
        )
        assert f"data/profile/{filename}" in text, (
            f"setup does not reference data/profile/{filename}"
        )


def test_setup_bootstrap_step_only_fires_when_the_target_is_missing():
    text = SETUP_SKILL.read_text()
    assert "doesn't already exist" in text or "does not already exist" in text or "doesn't exist yet" in text


def test_setup_bootstrap_never_overwrites_an_existing_populated_profile():
    text = SETUP_SKILL.read_text()
    assert "never overwrite" in text.lower() or "does not overwrite" in text.lower() or "not overwrite" in text.lower()


def test_setup_no_longer_references_the_old_skill_tree_profile_paths():
    text = SETUP_SKILL.read_text()
    assert "career-profile/01-candidate-profile.md" not in text
    assert "career-profile/02-behavioral-profile.md" not in text
    assert "rolesherpa-scrape/search-queries.md" not in text
