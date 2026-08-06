"""The reference implementation hardcoded the exact blank section-header
skeleton reset.md writes back to 01-candidate-profile.md and
02-behavioral-profile.md. RoleSherpa's port carried an inline copy of that same skeleton in
rolesherpa-reset/SKILL.md - which then drifted from the separately
maintained tracked-placeholder content rolesherpa-setup/SKILL.md
implicitly relied on as its fresh-clone bootstrap (two independently
maintained "blank" definitions, no mechanism keeping them in sync).

decouple-profile-data-from-skills replaces both with a single tracked
template under templates/profile/, referenced by both setup (bootstrap)
and reset (return-to-blank) - "self-contained" now means "defined once,
in a tracked file untouched by normal usage", not "defined inline in
reset's own instructions".
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RESET_SKILL = REPO_ROOT / ".agents" / "skills" / "rolesherpa-reset" / "SKILL.md"
MAIN_SPEC = REPO_ROOT / "docs" / "agent-skills-spec.md"


def test_reset_no_longer_defers_to_the_files_own_current_structure():
    text = RESET_SKILL.read_text()
    assert "same shape as when" not in text


def test_reset_copies_candidate_profile_from_the_tracked_template():
    text = RESET_SKILL.read_text()
    assert "templates/profile/candidate-profile.md" in text
    assert "data/profile/candidate-profile.md" in text


def test_reset_copies_behavioral_profile_from_the_tracked_template():
    text = RESET_SKILL.read_text()
    assert "templates/profile/behavioral-profile.md" in text
    assert "data/profile/behavioral-profile.md" in text


def test_reset_no_longer_inlines_its_own_blank_skeleton():
    text = RESET_SKILL.read_text()
    # The old inline skeleton was a fenced ```markdown block containing
    # every candidate-profile header, written directly into reset's own
    # instructions. That block must be gone now that reset copies from
    # templates/profile/ instead.
    assert "```markdown" not in text


def test_reset_no_longer_references_the_old_skill_tree_profile_paths():
    text = RESET_SKILL.read_text()
    assert "01-candidate-profile.md" not in text
    assert "02-behavioral-profile.md" not in text


def test_main_spec_describes_the_template_copy_approach_not_the_inline_skeleton():
    text = MAIN_SPEC.read_text()
    assert "templates/profile/" in text
    assert "separately-defined inline skeleton" in text or "inline skeleton" in text
