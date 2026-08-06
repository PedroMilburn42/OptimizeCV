import json

from rolesherpa import cli
from rolesherpa.documents.render import render

ONE_PAGE_HTML = "<h1>Data Engineer CV</h1><p>Experienced with Python and SQL.</p>"
TWO_PAGE_HTML = '<div style="break-after: page;">Page one.</div><div>Page two.</div>'


def _write_pdf(tmp_path, html, name="doc.pdf"):
    path = tmp_path / name
    path.write_bytes(render(html))
    return path


def test_verify_compliant_pdf_exits_zero_and_prints_confirmation(tmp_path, capsys):
    path = _write_pdf(tmp_path, ONE_PAGE_HTML)

    exit_code = cli.main(["render", "verify", str(path), "--pages", "1"])

    assert exit_code == 0
    out = capsys.readouterr().out
    assert "1 page" in out


def test_verify_reports_missing_keyword_without_failing(tmp_path, capsys):
    path = _write_pdf(tmp_path, ONE_PAGE_HTML)

    exit_code = cli.main(["render", "verify", str(path), "--contains", "Kubernetes"])

    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Kubernetes" in out


def test_verify_wrong_page_count_exits_one_with_json_error(tmp_path, capsys):
    path = _write_pdf(tmp_path, TWO_PAGE_HTML)

    exit_code = cli.main(["render", "verify", str(path), "--pages", "1"])

    assert exit_code == 1
    out, err = capsys.readouterr()
    assert out == ""
    payload = json.loads(err)
    assert payload["code"] == "VERIFICATION_FAILED"
    assert "expected 1" in payload["error"]


def test_verify_within_max_pages_tolerance_exits_zero(tmp_path, capsys):
    path = _write_pdf(tmp_path, TWO_PAGE_HTML)

    exit_code = cli.main(["render", "verify", str(path), "--pages", "1", "--max-pages", "2"])

    assert exit_code == 0
    out = capsys.readouterr().out
    assert "2 page" in out


def test_verify_above_max_pages_exits_one_with_json_error(tmp_path, capsys):
    THREE_PAGE_HTML = (
        '<div style="break-after: page;">Page one.</div>'
        '<div style="break-after: page;">Page two.</div>'
        "<div>Page three.</div>"
    )
    path = _write_pdf(tmp_path, THREE_PAGE_HTML, name="three.pdf")

    exit_code = cli.main(["render", "verify", str(path), "--pages", "1", "--max-pages", "2"])

    assert exit_code == 1
    out, err = capsys.readouterr()
    assert out == ""
    payload = json.loads(err)
    assert payload["code"] == "VERIFICATION_FAILED"
    assert "expected 1-2" in payload["error"]


def test_verify_missing_file_exits_one_with_json_error(tmp_path, capsys):
    missing = tmp_path / "does-not-exist.pdf"

    exit_code = cli.main(["render", "verify", str(missing)])

    assert exit_code == 1
    out, err = capsys.readouterr()
    assert out == ""
    payload = json.loads(err)
    assert payload["code"] == "VERIFICATION_ERROR"


def test_verify_matched_keyword_is_not_reported_as_missing(tmp_path, capsys):
    path = _write_pdf(tmp_path, ONE_PAGE_HTML)

    exit_code = cli.main(["render", "verify", str(path), "--contains", "Python"])

    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Missing" not in out


def test_render_pdf_writes_a_pdf_file_from_html(tmp_path, capsys):
    html_path = tmp_path / "cv.html"
    html_path.write_text(ONE_PAGE_HTML)
    output_path = tmp_path / "cv.pdf"

    exit_code = cli.main(["render", "pdf", str(html_path), str(output_path)])

    assert exit_code == 0
    assert output_path.read_bytes().startswith(b"%PDF")
    out = capsys.readouterr().out
    assert str(output_path) in out


def test_render_pdf_applies_css_file_when_given(tmp_path):
    html_path = tmp_path / "cv.html"
    html_path.write_text("<h1>Styled</h1>")
    css_path = tmp_path / "style.css"
    css_path.write_text("h1 { color: red; }")
    output_path = tmp_path / "cv.pdf"

    exit_code = cli.main(["render", "pdf", str(html_path), str(output_path), "--css", str(css_path)])

    assert exit_code == 0
    assert output_path.exists()


def test_render_pdf_missing_html_file_errors_to_stderr_with_exit_1(tmp_path, capsys):
    missing = tmp_path / "does-not-exist.html"
    output_path = tmp_path / "cv.pdf"

    exit_code = cli.main(["render", "pdf", str(missing), str(output_path)])

    assert exit_code == 1
    out, err = capsys.readouterr()
    assert out == ""
    payload = json.loads(err)
    assert payload["code"] == "RENDER_ERROR"
