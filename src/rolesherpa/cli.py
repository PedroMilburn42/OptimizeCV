"""python -m rolesherpa.cli — the deterministic surface skills shell out
to instead of following prose instructions for connector search/detail
(design.md D3, PROJECT_BRIEF.md §4a point 2).
"""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from rolesherpa.connectors.registry import ConnectorRegistry
from rolesherpa.domain.chronology import (
    detect_gaps,
    detect_impossible_ranges,
    detect_overlaps,
    parse_profile_experience,
)
from rolesherpa.domain.dedup import filter_new
from rolesherpa.domain.models import JobPosting


def _print_error(message: str, code: str) -> None:
    print(json.dumps({"error": message, "code": code}), file=sys.stderr)


def _parse_filters(pairs: list[str]) -> dict:
    filters = {}
    for pair in pairs:
        key, _, value = pair.partition("=")
        filters[key] = value
    return filters


def _format_table(results) -> str:
    header = f"{'ID':<24} {'TITLE':<40} {'COMPANY':<25} {'LOCATION':<25} {'DATE':<12}"
    rows = [
        f"{r.id[:24]:<24} {r.title[:40]:<40} {r.company[:25]:<25} {(r.location or '')[:25]:<25} {(r.date or '')[:12]:<12}"
        for r in results
    ]
    return "\n".join([header, *rows])


def _format_plain(job) -> str:
    lines = [f"{job.title} — {job.company}", job.location or "", job.url, "", job.description or ""]
    return "\n".join(lines)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m rolesherpa.cli")
    top = parser.add_subparsers(dest="command", required=True)

    connectors = top.add_parser("connectors")
    action = connectors.add_subparsers(dest="action", required=True)

    search = action.add_parser("search")
    search.add_argument("--source", required=True)
    search.add_argument("--query", "-q", default="")
    search.add_argument("--location", "-l", default=None)
    search.add_argument("--jobage", type=int, default=None)
    search.add_argument("--page", type=int, default=1)
    search.add_argument("--limit", type=int, default=None)
    search.add_argument("--filter", action="append", default=[])
    search.add_argument("--format", choices=["json", "table", "plain"], default="json")

    detail = action.add_parser("detail")
    detail.add_argument("job_id")
    detail.add_argument("--source", required=True)
    detail.add_argument("--format", choices=["json", "table", "plain"], default="json")

    action.add_parser("list")

    render = top.add_parser("render")
    render_action = render.add_subparsers(dest="action", required=True)

    render_verify = render_action.add_parser("verify")
    render_verify.add_argument("path")
    render_verify.add_argument("--pages", type=int, default=None)
    render_verify.add_argument("--max-pages", type=int, default=None)
    render_verify.add_argument("--min-chars", type=int, default=1)
    render_verify.add_argument("--contains", action="append", default=[])

    render_pdf = render_action.add_parser("pdf")
    render_pdf.add_argument("html_path")
    render_pdf.add_argument("output_path")
    render_pdf.add_argument("--css", default=None)

    profile = top.add_parser("profile")
    profile_action = profile.add_subparsers(dest="action", required=True)

    audit_chronology = profile_action.add_parser("audit-chronology")
    audit_chronology.add_argument("path")
    audit_chronology.add_argument("--gap-threshold-days", type=int, default=30)

    dedup = top.add_parser("dedup")
    dedup_action = dedup.add_subparsers(dest="action", required=True)

    dedup_filter = dedup_action.add_parser("filter")
    dedup_filter.add_argument("candidates_path")
    dedup_filter.add_argument("--against", default=None)

    return parser


def _run_render_verify(args) -> int:
    try:
        from rolesherpa.documents.verify import verify

        pdf_bytes = Path(args.path).read_bytes()
        result = verify(
            pdf_bytes,
            expected_pages=args.pages,
            max_pages=args.max_pages,
            min_chars=args.min_chars,
            required_text=tuple(args.contains),
        )
    except Exception as exc:  # noqa: BLE001 - CLI boundary: any read/parse failure becomes a clean JSON error
        _print_error(str(exc), "VERIFICATION_ERROR")
        return 1

    if not result.passed:
        _print_error("; ".join(result.errors), "VERIFICATION_FAILED")
        return 1

    print(f"Verified {args.path}: {result.page_count} page(s), {result.text_length} character(s) extracted")
    if result.missing_keywords:
        print(f"Missing keywords (not blocking): {', '.join(result.missing_keywords)}")
    return 0


def _load_postings(path: str) -> list[JobPosting]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [JobPosting(**item) for item in data]


def _run_dedup_filter(args) -> int:
    try:
        candidates = _load_postings(args.candidates_path)
        existing = _load_postings(args.against) if args.against else []
    except Exception as exc:  # noqa: BLE001 - CLI boundary: any read/parse failure becomes a clean JSON error
        _print_error(str(exc), "DEDUP_ERROR")
        return 1

    new, duplicates = filter_new(candidates, existing)
    payload = {
        "new": [asdict(p) for p in new],
        "duplicates": [{"candidate": asdict(c), "matched": asdict(m)} for c, m in duplicates],
    }
    print(json.dumps(payload))
    return 0


def _run_render_pdf(args) -> int:
    try:
        from rolesherpa.documents.render import render

        html = Path(args.html_path).read_text(encoding="utf-8")
        css = Path(args.css).read_text(encoding="utf-8") if args.css else None
        pdf_bytes = render(html, css=css)
        Path(args.output_path).write_bytes(pdf_bytes)
    except Exception as exc:  # noqa: BLE001 - CLI boundary: any render failure becomes a clean JSON error
        _print_error(str(exc), "RENDER_ERROR")
        return 1

    print(f"Rendered {args.output_path}")
    return 0


def _entry_label(entry) -> str:
    return f"{entry.title} — {entry.company}"


def _run_profile_audit_chronology(args) -> int:
    try:
        text = Path(args.path).read_text(encoding="utf-8")
        entries = parse_profile_experience(text)
    except Exception as exc:  # noqa: BLE001 - CLI boundary: any read/parse failure becomes a clean JSON error
        _print_error(str(exc), "AUDIT_ERROR")
        return 1

    gaps = detect_gaps(entries, threshold_days=args.gap_threshold_days)
    overlaps = detect_overlaps(entries)
    impossible = detect_impossible_ranges(entries)

    payload = {
        "entries_parsed": len(entries),
        "gaps": [
            {"after": _entry_label(g.after), "before": _entry_label(g.before), "days": g.days}
            for g in gaps
        ],
        "overlaps": [
            {"a": _entry_label(o.a), "b": _entry_label(o.b), "days": o.days}
            for o in overlaps
        ],
        "impossible_ranges": impossible,
    }
    print(json.dumps(payload))
    return 0


def main(argv: list[str] | None = None, registry: ConnectorRegistry | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.command == "render" and args.action == "pdf":
        return _run_render_pdf(args)
    if args.command == "render":
        return _run_render_verify(args)

    if args.command == "profile":
        return _run_profile_audit_chronology(args)

    if args.command == "dedup":
        return _run_dedup_filter(args)

    registry = registry or ConnectorRegistry()

    if args.action == "list":
        payload = {
            "active": sorted(registry.active_connectors()),
            "blocked": [{"name": b.name, "reason": b.blocked_reason} for b in registry.blocked_sources()],
        }
        print(json.dumps(payload))
        return 0

    connector = registry.active_connectors().get(args.source)
    if connector is None:
        _print_error(f"unknown or disabled source: {args.source}", "UNKNOWN_SOURCE")
        return 1

    try:
        if args.action == "search":
            kwargs = _parse_filters(args.filter)
            if args.location is not None:
                kwargs["location"] = args.location
            if args.jobage is not None:
                kwargs["jobage"] = args.jobage
            if args.limit is not None:
                kwargs["limit"] = args.limit
            result = connector.search(args.query, page=args.page, **kwargs)

            if args.format == "json":
                payload = {
                    "meta": {"count": result.meta.count, "page": result.meta.page},
                    "results": [asdict(r) for r in result.results],
                }
                print(json.dumps(payload))
            elif args.format == "table":
                print(_format_table(result.results))
            else:
                print("\n\n".join(_format_plain(r) for r in result.results))
            return 0

        job = connector.detail(args.job_id)
        if args.format == "json":
            print(json.dumps(asdict(job)))
        else:
            print(_format_plain(job))
        return 0

    except LookupError as exc:
        _print_error(str(exc), "NOT_FOUND")
        return 1
    except ValueError as exc:
        _print_error(str(exc), "INVALID_ARGUMENT")
        return 1
    except Exception as exc:  # noqa: BLE001 - CLI boundary: any connector failure becomes a clean JSON error
        _print_error(str(exc), "CONNECTOR_ERROR")
        return 1


if __name__ == "__main__":
    sys.exit(main())
