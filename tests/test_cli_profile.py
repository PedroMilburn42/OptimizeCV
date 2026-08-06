import json

from rolesherpa import cli

FIXTURE = """
## Professional Experience

**Role A** | Company A | Jan 2020 – Jun 2020
- did things.

**Role B** | Company B | Jan 2021 – Jun 2021
- did other things.
"""

CONTIGUOUS_FIXTURE = """
## Professional Experience

**Role A** | Company A | Jan 2020 – Jun 2020
- did things.

**Role B** | Company B | Jun 2020 – Dec 2020
- did other things.
"""


def _write(tmp_path, text):
    path = tmp_path / "01-candidate-profile.md"
    path.write_text(text)
    return path


def test_audit_chronology_reports_a_gap(tmp_path, capsys):
    path = _write(tmp_path, FIXTURE)

    exit_code = cli.main(["profile", "audit-chronology", str(path)])

    assert exit_code == 0
    out = json.loads(capsys.readouterr().out)
    assert out["entries_parsed"] == 2
    assert len(out["gaps"]) == 1
    assert out["gaps"][0]["after"] == "Role A — Company A"
    assert out["gaps"][0]["before"] == "Role B — Company B"
    assert out["gaps"][0]["days"] > 100
    assert out["overlaps"] == []
    assert out["impossible_ranges"] == []


def test_audit_chronology_no_gap_for_contiguous_roles(tmp_path, capsys):
    path = _write(tmp_path, CONTIGUOUS_FIXTURE)

    exit_code = cli.main(["profile", "audit-chronology", str(path)])

    assert exit_code == 0
    out = json.loads(capsys.readouterr().out)
    assert out["gaps"] == []


def test_audit_chronology_respects_custom_threshold(tmp_path, capsys):
    path = _write(tmp_path, FIXTURE)

    exit_code = cli.main(["profile", "audit-chronology", str(path), "--gap-threshold-days", "300"])

    assert exit_code == 0
    out = json.loads(capsys.readouterr().out)
    assert out["gaps"] == []


def test_audit_chronology_missing_file_exits_one_with_json_error(tmp_path, capsys):
    missing = tmp_path / "does-not-exist.md"

    exit_code = cli.main(["profile", "audit-chronology", str(missing)])

    assert exit_code == 1
    out, err = capsys.readouterr()
    assert out == ""
    payload = json.loads(err)
    assert payload["code"] == "AUDIT_ERROR"
