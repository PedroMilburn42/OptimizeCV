# Template: modern-safe (Cover letter)

- **Type:** Cover letter
- **Renderer:** WeasyPrint (HTML/CSS → PDF) — see `design.md` D6
- **Page limit:** exactly 1 page(s) — no tolerance, unlike the CV's modern-safe template. A cover letter that needs more than 1 page is a sign the text needs editing, not more room; see `06-cover-letter-templates.md`'s Structure section for why this differs from the CV's 2-page-target/3-tolerated rule.
- **Fonts:** Helvetica Neue / Arial system font stack — no bundled font files
- **Class/packages:** standard HTML/CSS, no dependencies beyond WeasyPrint

## Origin

Built 2026-08-02 for visual consistency with `templates/cv/modern-safe/`
when both documents are submitted together — same color accent
(`#1f3a5f`) and bold treatment on the candidate's name in the sender
block. Deliberately does **not** port every CV modern-safe feature:
no tagline (a cover letter isn't headed with a positioning line), no
Core Competencies grouping (narrative prose, not a skills list), no
page tolerance (see Page limit above).

## Render + verify command

    python -m rolesherpa.cli render verify <output.pdf> --pages 1

## Character budget

Measured against a real render at this template's default font/margins: the full page-1 text (sender block + date + recipient + greeting + body paragraphs + bullet list + signature) fits at ~2250 characters, and reliably overflows to a second page at ~2400+ characters. Use this as a starting budget when trimming for the 1-page limit instead of iterating render→verify→trim from scratch — a cut needs to remove roughly a full line's worth of text (not a few words) to actually free a line, since WeasyPrint's line-wrapping means small trims often land mid-line with no visible effect on page count.

## Style rules

- Single paragraph flow, no columns.
- The highlight bullet list uses `break-inside: avoid` so it never splits across a page.
- Keep to 3–4 short paragraphs plus the bullet list — trim content rather than shrinking margins or line spacing if it overflows to a second page.
- The sender block's name (`.sender-name`) has a literal `&nbsp;` before its closing tag — without it, PDF text-layer extraction concatenates the name directly into the contact line below (e.g. `"Jane DoeMontevideo, Uruguay"`), the same class of bug found and fixed in `templates/cv/modern-safe/`'s header. Applied here from the start rather than found after the fact.

## Known pitfalls

- None recorded yet beyond the sender-name spacing rule above (already applied, not a fix-after-the-fact).
