from rolesherpa.documents.render import render


def test_render_returns_nonempty_pdf_bytes():
    pdf = render("<h1>Test</h1><p>WeasyPrint smoke test.</p>")
    assert isinstance(pdf, bytes)
    assert len(pdf) > 0
    assert pdf.startswith(b"%PDF")


def test_render_applies_supplied_css():
    pdf = render("<h1>Styled</h1>", css="h1 { color: red; }")
    assert pdf.startswith(b"%PDF")
