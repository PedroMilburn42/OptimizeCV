"""rolesherpa-outcome/SKILL.md archives each application to
data/applications/<company>-<role>-<YYMMDD>/. rolesherpa-setup/SKILL.md and
rolesherpa-reset/SKILL.md must reference that same directory - a stray
reference to documents/applications/ (a leftover from an earlier,
simpler single-bucket layout) means setup silently mines nothing and
reset silently leaves the real archive untouched.

The folder is also the *only* place an active draft or submitted document
lives - rolesherpa-apply used to stage drafts in separate cv/ and
cover_letters/ working directories before rolesherpa-outcome copied the
submitted pair into the archive. That split meant rolesherpa-setup's Path A
mining step (which already assumed a single data/applications/*/cv.html per
application) silently found nothing, since rolesherpa-apply never wrote
there. Consolidating into one folder, created at draft time, fixes that
latent bug as a side effect.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS = REPO_ROOT / ".agents" / "skills"

CANONICAL_PATH = "data/applications/"
STALE_PATH = "documents/applications/"
STALE_STAGING_PATHS = ["cv/main_", "cover_letters/cover_"]


def test_outcome_writes_to_the_canonical_archive_path():
    text = (SKILLS / "rolesherpa-outcome" / "SKILL.md").read_text()
    assert CANONICAL_PATH in text


def test_setup_references_the_canonical_archive_path_not_the_stale_one():
    text = (SKILLS / "rolesherpa-setup" / "SKILL.md").read_text()
    assert CANONICAL_PATH in text
    assert STALE_PATH not in text


def test_reset_references_the_canonical_archive_path_not_the_stale_one():
    text = (SKILLS / "rolesherpa-reset" / "SKILL.md").read_text()
    assert CANONICAL_PATH in text
    assert STALE_PATH not in text


def test_apply_writes_drafts_directly_into_the_unified_application_folder():
    text = (SKILLS / "rolesherpa-apply" / "SKILL.md").read_text()
    assert "data/applications/" in text
    assert "<company>-<role>-" in text or "-<role>-<" in text


def test_no_skill_references_the_old_split_staging_directories():
    for skill_name in ["rolesherpa-apply", "rolesherpa-outcome", "rolesherpa-interview", "rolesherpa-setup", "rolesherpa-reset"]:
        text = (SKILLS / skill_name / "SKILL.md").read_text()
        for stale in STALE_STAGING_PATHS:
            assert stale not in text, f"{skill_name}/SKILL.md still references stale staging path {stale!r}"
