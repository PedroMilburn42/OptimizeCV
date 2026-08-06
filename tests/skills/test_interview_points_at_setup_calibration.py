"""rolesherpa-interview/SKILL.md claimed outcome data feeds
rolesherpa-upskill's gap analysis, but upskill only reads
job_search_tracker.csv's fit_rating column - it never reads outcome
data. The real consumer of resolved-outcome data for calibration is
rolesherpa-setup/SKILL.md.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INTERVIEW_SKILL = REPO_ROOT / ".agents" / "skills" / "rolesherpa-interview" / "SKILL.md"
UPSKILL_SKILL = REPO_ROOT / ".agents" / "skills" / "rolesherpa-upskill" / "SKILL.md"


def test_upskill_does_not_actually_read_outcome_data():
    # Sanity-check the premise: upskill never reads outcome.md today.
    text = UPSKILL_SKILL.read_text()
    assert "outcome.md" not in text


def test_interview_step_5_points_at_setup_not_upskill():
    text = INTERVIEW_SKILL.read_text()
    step5_start = text.index("Step 5")
    step5_text = text[step5_start:step5_start + 400]
    assert "rolesherpa-setup" in step5_text
    assert "rolesherpa-upskill" not in step5_text
