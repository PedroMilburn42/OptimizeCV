"""candidate-profile.md, behavioral-profile.md, and search-queries.md
moved out of the tracked skills tree (career-profile/, rolesherpa-scrape/)
into gitignored data/profile/ - see decouple-profile-data-from-skills.
Every skill that reads this personal data must reference its new
data/profile/ location; a stray reference to the old
career-profile/01-candidate-profile.md, career-profile/02-behavioral-profile.md,
or a bare (non-data/profile/) search-queries.md path means that skill
silently reads nothing (or the wrong thing) once the old files are
replaced by stub pointers.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS = REPO_ROOT / ".agents" / "skills"

STALE_CANDIDATE_PATH = "01-candidate-profile.md"
STALE_BEHAVIORAL_PATH = "02-behavioral-profile.md"
CANONICAL_CANDIDATE_PATH = "data/profile/candidate-profile.md"
CANONICAL_BEHAVIORAL_PATH = "data/profile/behavioral-profile.md"
CANONICAL_SEARCH_QUERIES_PATH = "data/profile/search-queries.md"

FILES = [
    "career-profile/04-job-evaluation.md",
    "career-profile/05-cv-templates.md",
    "career-profile/07-interview-prep.md",
    "rolesherpa-apply/SKILL.md",
    "rolesherpa-audit/SKILL.md",
    "rolesherpa-expand/SKILL.md",
    "rolesherpa-interview/SKILL.md",
    "rolesherpa-rank/SKILL.md",
    "rolesherpa-scrape/SKILL.md",
    "rolesherpa-add-portal/SKILL.md",
    "rolesherpa-upskill/SKILL.md",
]


def _read(relative_path):
    return (SKILLS / relative_path).read_text()


def test_no_referencing_file_uses_the_stale_candidate_profile_path():
    offenders = [f for f in FILES if STALE_CANDIDATE_PATH in _read(f)]
    assert offenders == [], f"still reference {STALE_CANDIDATE_PATH}: {offenders}"


def test_no_referencing_file_uses_the_stale_behavioral_profile_path():
    offenders = [f for f in FILES if STALE_BEHAVIORAL_PATH in _read(f)]
    assert offenders == [], f"still reference {STALE_BEHAVIORAL_PATH}: {offenders}"


def test_no_referencing_file_uses_a_bare_search_queries_path():
    offenders = []
    for f in FILES:
        text = _read(f)
        if "search-queries.md" in text and CANONICAL_SEARCH_QUERIES_PATH not in text:
            offenders.append(f)
    assert offenders == [], f"reference search-queries.md without the data/profile/ prefix: {offenders}"


def test_files_that_reference_candidate_profile_use_the_canonical_path():
    files_mentioning_candidate = [
        f for f in FILES
        if "candidate-profile.md" in _read(f)
    ]
    offenders = [f for f in files_mentioning_candidate if CANONICAL_CANDIDATE_PATH not in _read(f)]
    assert offenders == [], f"mention candidate-profile.md without the canonical data/profile/ path: {offenders}"


def test_files_that_reference_behavioral_profile_use_the_canonical_path():
    files_mentioning_behavioral = [
        f for f in FILES
        if "behavioral-profile.md" in _read(f)
    ]
    offenders = [f for f in files_mentioning_behavioral if CANONICAL_BEHAVIORAL_PATH not in _read(f)]
    assert offenders == [], f"mention behavioral-profile.md without the canonical data/profile/ path: {offenders}"
