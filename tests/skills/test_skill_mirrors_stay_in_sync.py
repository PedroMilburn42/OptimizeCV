"""Claude Code only discovers skills from .claude/skills/ (confirmed
against official docs) - it does not read .agents/skills/, even though
Antigravity and Codex CLI both do (confirmed against their own official/
tested docs). RoleSherpa's 11 skills + career-profile/ are therefore
duplicated into both trees. This test catches drift between the two
copies - it is not testing skill *content*, only that the two mirrors
agree, since a silent divergence would mean Claude Code users see
different behavior than Antigravity/Codex users.
"""

import filecmp
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_SKILLS = REPO_ROOT / ".agents" / "skills"

# .agents/skills/ is the source of truth for the directory names compared;
# iterate from there so any extra, unrelated content later added under
# .claude/skills/ doesn't need to be excluded explicitly.
MIRRORED_SKILL_NAMES = [p.name for p in AGENTS_SKILLS.iterdir() if p.is_dir()]


def test_agents_and_claude_mirrors_contain_the_same_skill_directories():
    claude_names = {p.name for p in (REPO_ROOT / ".claude" / "skills").iterdir() if p.is_dir()}
    assert set(MIRRORED_SKILL_NAMES) <= claude_names


def test_every_mirrored_file_is_byte_identical_between_agents_and_claude():
    mismatches = []
    for name in MIRRORED_SKILL_NAMES:
        agents_dir = AGENTS_SKILLS / name
        claude_dir = REPO_ROOT / ".claude" / "skills" / name
        comparison = filecmp.dircmp(agents_dir, claude_dir)
        if comparison.left_only or comparison.right_only or comparison.diff_files:
            mismatches.append((name, comparison.left_only, comparison.right_only, comparison.diff_files))

    assert mismatches == [], (
        f"Skill mirrors have drifted between .agents/skills/ and .claude/skills/: {mismatches}. "
        "Claude Code only reads .claude/skills/, Antigravity/Codex only read .agents/skills/ - "
        "re-sync both trees (copy .agents/skills/<name>/ over .claude/skills/<name>/) before committing."
    )
