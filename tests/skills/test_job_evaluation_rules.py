"""A comparative audit (2026-08-03) of a similar agent's session found a
generated CV that carried a team-size figure never confirmed with the
user, which turned out to be wrong - the number came from an old CV the
agent treated as ground truth without asking. 04-job-evaluation.md needs
an explicit rule that any quantifiable fact depending on how it's
counted - years of experience, team size, budget figures - gets
confirmed with the user rather than computed or inherited silently.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

JOB_EVALUATION = REPO_ROOT / ".agents" / "skills" / "career-profile" / "04-job-evaluation.md"


def test_ambiguous_quantifiable_facts_are_confirmed_with_the_user():
    text = JOB_EVALUATION.read_text().lower()
    assert "years of experience" in text
    assert "team size" in text
    assert "confirm" in text


def test_ambiguous_facts_are_never_silently_computed_or_inherited():
    text = JOB_EVALUATION.read_text().lower()
    assert "silently" in text
