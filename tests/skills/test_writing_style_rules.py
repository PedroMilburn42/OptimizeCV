"""Three drafting/verification behaviors were being applied by operator
judgment during a live rolesherpa-apply session rather than being written
into 03-writing-style.md, the file the drafter and reviewer steps actually
read: converting hard-banned punctuation in user-pasted text before
inserting it, writing accented characters as literal UTF-8 instead of HTML
entities, and verifying accented characters against the rendered PDF's
text layer rather than the HTML source alone. Undocumented, these don't
reliably survive to the next session or a different acting agent.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

WRITING_STYLE = REPO_ROOT / ".agents" / "skills" / "career-profile" / "03-writing-style.md"


def test_pasted_text_is_auto_scanned_against_hard_bans():
    text = WRITING_STYLE.read_text().lower()
    assert "pasted" in text
    assert "hard ban" in text
    assert "automatic" in text or "without asking" in text


def test_accented_characters_are_literal_utf_8_not_html_entities():
    text = WRITING_STYLE.read_text().lower()
    assert "html entit" in text
    assert "literal" in text and ("utf-8" in text or "utf8" in text)


def test_verification_reads_the_rendered_pdf_text_not_just_the_source():
    text = WRITING_STYLE.read_text().lower()
    assert "rendered pdf" in text
    assert "text layer" in text or "extract" in text
