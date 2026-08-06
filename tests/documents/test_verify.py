from rolesherpa.documents.render import render
from rolesherpa.documents.verify import verify

ONE_PAGE_HTML = "<h1>Data Engineer CV</h1><p>Experienced with Python and SQL.</p>"
TWO_PAGE_HTML = (
    '<div style="break-after: page;">Page one content.</div>'
    "<div>Page two content.</div>"
)


def test_page_count_passes_when_it_matches_expected():
    pdf = render(ONE_PAGE_HTML)
    result = verify(pdf, expected_pages=1)
    assert result.passed is True
    assert result.page_count == 1
    assert result.errors == []


def test_page_count_fails_when_it_does_not_match_expected():
    pdf = render(TWO_PAGE_HTML)
    result = verify(pdf, expected_pages=1)
    assert result.passed is False
    assert result.page_count == 2
    assert any("expected 1" in e and "found 2" in e for e in result.errors)


def test_text_layer_is_extracted():
    pdf = render(ONE_PAGE_HTML)
    result = verify(pdf)
    assert result.text_length > 0
    assert result.passed is True


def test_text_layer_below_min_chars_fails():
    pdf = render(ONE_PAGE_HTML)
    result = verify(pdf, min_chars=100_000)
    assert result.passed is False
    assert any("text layer" in e for e in result.errors)


def test_missing_keyword_is_reported_without_failing_verification():
    pdf = render(ONE_PAGE_HTML)
    result = verify(pdf, required_text=["Kubernetes"])
    assert result.missing_keywords == ["Kubernetes"]
    assert result.passed is True


def test_present_keyword_is_not_reported_as_missing():
    pdf = render(ONE_PAGE_HTML)
    result = verify(pdf, required_text=["Python"])
    assert result.missing_keywords == []


def test_keyword_match_is_whitespace_normalized():
    pdf = render("<p>Python   and\nSQL</p>")
    result = verify(pdf, required_text=["Python and SQL"])
    assert result.missing_keywords == []


def test_max_pages_passes_at_target():
    pdf = render(ONE_PAGE_HTML)
    result = verify(pdf, expected_pages=1, max_pages=2)
    assert result.passed is True
    assert result.errors == []


def test_max_pages_passes_within_tolerance():
    pdf = render(TWO_PAGE_HTML)
    result = verify(pdf, expected_pages=1, max_pages=2)
    assert result.passed is True
    assert result.errors == []


def test_max_pages_fails_above_tolerance():
    THREE_PAGE_HTML = (
        '<div style="break-after: page;">Page one.</div>'
        '<div style="break-after: page;">Page two.</div>'
        "<div>Page three.</div>"
    )
    pdf = render(THREE_PAGE_HTML)
    result = verify(pdf, expected_pages=1, max_pages=2)
    assert result.passed is False
    assert any("expected 1-2" in e and "found 3" in e for e in result.errors)


def test_max_pages_without_expected_pages_uses_one_as_lower_bound():
    pdf = render(TWO_PAGE_HTML)
    result = verify(pdf, max_pages=2)
    assert result.passed is True


def test_max_pages_equal_to_expected_pages_reports_exact_count_in_error():
    pdf = render(TWO_PAGE_HTML)
    result = verify(pdf, expected_pages=1, max_pages=1)
    assert result.passed is False
    assert any("expected 1 page(s), found 2" in e for e in result.errors)
