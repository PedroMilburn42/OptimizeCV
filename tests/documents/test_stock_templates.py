import re
from pathlib import Path

from rolesherpa.documents.render import render
from rolesherpa.documents.verify import verify

TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates"

CV_PLACEHOLDERS = {
    "[YOUR_NAME]": "Jane Doe",
    "[YOUR_CITY]": "Montevideo",
    "[YOUR_COUNTRY]": "Uruguay",
    "[YOUR_EMAIL]": "jane.doe@example.com",
    "[YOUR_PHONE]": "+598 00 000 000",
    "[YOUR_LINKEDIN_URL]": "linkedin.com/in/janedoe",
    "[PROFILE_STATEMENT]": "AI Engineer with five years of experience building data products.",
    "[JOB_TITLE]": "AI Engineer",
    "[COMPANY]": "Acme S.A.",
    "[START_DATE]": "2023",
    "[END_DATE]": "Present",
    "[LOCATION]": "Montevideo, Uruguay",
    "[BULLET_1]": "Built a job-matching pipeline serving 10k users.",
    "[BULLET_2]": "Reduced inference latency by 40 percent.",
    "[BULLET_3]": "Mentored two junior engineers.",
    "[DEGREE]": "MSc Data Science",
    "[INSTITUTION]": "UTEC",
    "[YEAR_START]": "2024",
    "[YEAR_END]": "2026",
    "[YOUR_PRIMARY_SKILLS]": "Python, PyTorch, SQL",
    "[YOUR_SECONDARY_SKILLS]": "Docker, AWS",
}

COVER_LETTER_PLACEHOLDERS = {
    "[YOUR_NAME]": "Jane Doe",
    "[YOUR_CITY]": "Montevideo",
    "[YOUR_COUNTRY]": "Uruguay",
    "[YOUR_EMAIL]": "jane.doe@example.com",
    "[YOUR_PHONE]": "+598 00 000 000",
    "[DATE]": "2026-08-01",
    "[RECIPIENT_NAME_OR_HIRING_MANAGER]": "Hiring Manager",
    "[COMPANY]": "Acme S.A.",
    "[OPENING_PARAGRAPH]": "I am writing to apply for the AI Engineer role at Acme S.A.",
    "[BODY_PARAGRAPH_1]": "My background in data engineering and Python aligns closely with your requirements.",
    "[HIGHLIGHT_BULLET_1]": "Built and shipped three production ML pipelines.",
    "[HIGHLIGHT_BULLET_2]": "Led a cross-functional team of four engineers.",
    "[CLOSING_PARAGRAPH]": "Thank you for your consideration; I look forward to speaking with you.",
}


def _fill(html: str, placeholders: dict) -> str:
    for token, value in placeholders.items():
        html = html.replace(token, value)
    return html


def test_cv_stock_template_has_no_unresolved_placeholders_after_fill():
    html = (TEMPLATES_DIR / "cv" / "stock" / "template.html").read_text()
    filled = _fill(html, CV_PLACEHOLDERS)
    remaining = re.findall(r"\[[A-Z_0-9]+\]", filled)
    assert remaining == []


def test_cv_stock_template_renders_within_declared_page_limit():
    html = (TEMPLATES_DIR / "cv" / "stock" / "template.html").read_text()
    pdf = render(_fill(html, CV_PLACEHOLDERS))
    result = verify(pdf, required_text=["Python"])
    assert result.page_count <= 2
    assert result.text_length > 0
    assert result.missing_keywords == []


def test_cover_letter_stock_template_has_no_unresolved_placeholders_after_fill():
    html = (TEMPLATES_DIR / "cover_letters" / "stock" / "template.html").read_text()
    filled = _fill(html, COVER_LETTER_PLACEHOLDERS)
    remaining = re.findall(r"\[[A-Z_0-9]+\]", filled)
    assert remaining == []


def test_cover_letter_stock_template_renders_to_exactly_one_page():
    html = (TEMPLATES_DIR / "cover_letters" / "stock" / "template.html").read_text()
    pdf = render(_fill(html, COVER_LETTER_PLACEHOLDERS))
    result = verify(pdf, expected_pages=1, required_text=["Acme S.A."])
    assert result.passed is True
    assert result.missing_keywords == []
