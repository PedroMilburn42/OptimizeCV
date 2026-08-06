# Template: modern-safe (CV)

- **Type:** CV
- **Renderer:** WeasyPrint (HTML/CSS → PDF) — see `design.md` D6
- **Page limit:** 2 page(s) target, 3 tolerated per `05-cv-templates.md`'s escape-valve rule
- **Fonts:** Helvetica Neue / Arial system font stack — no bundled font files, no `Path` overrides needed
- **Class/packages:** standard HTML/CSS, no dependencies beyond WeasyPrint

## Origin

Built 2026-08-02 to reproduce the visual impact of an earlier CV
(LaTeX `libre-franklin-modern` template) —
tagline under the name, a stronger typographic hierarchy, and
categorized skills grouping — **without** that document's two ATS
risk factors: icon-only contact details (extracted as `"Map-marker"`,
`"Phone"`, `"Envelope"` literal text in that PDF's text layer) and a
true multi-column competency table. Same effect, none of the risk.

## Render + verify command

    python -m rolesherpa.cli render verify <output.pdf> --pages 2 --max-pages 3

## Character budget

Rougher estimate than the cover letter's (never tightly calibrated to the 2-page edge in practice — a 3-page render was accepted within tolerance rather than trimmed to exactly 2): roughly ~2400-2600 characters of extracted text per page at this template's default font/margins. Same caveat as the cover letter template — trims need to remove close to a full line to change the page count, not a few words.

## Style rules

- Single-column layout only — safe for ATS text-extraction reading order.
- A color accent (`#1f3a5f`, dark blue) is used on the name, section headings, and the header rule — chosen because it stays legible in grayscale printing and photocopying, unlike lighter accent colors.
- `[YOUR_TAGLINE]` sits directly under the name — a one-line positioning statement (e.g. "Program & Release Manager · AI & Data Science"), not a second profile paragraph.
- "Core Competencies" entries are plain `<p>` rows with a bold label, never a real CSS grid/table/multi-column layout — this reproduces the visual grouping effect of a competency table without the ATS reading-order risk a true table carries.
- Contact details (email, phone) are printed as literal text, never icon-only — required for the ATS text-layer check in `document-pipeline` verification. No icon glyphs anywhere in this template.
- Section headings (`h2`) use `break-after: avoid` so a heading never sits alone at the bottom of a page.
- Each experience/education entry (`.entry`) uses `break-inside: avoid` so a role's title never splits from its bullets across a page break.
- `.entry-header`'s two `<span>` children (title/company vs. dates) have a literal space between their closing/opening tags in the HTML source — `display: flex; justify-content: space-between` visually separates them regardless, but the space prevents PDF text-layer concatenation (e.g. `"Example CorpJan 2024"`) that risks ATS date-range parsing. See `templates/cv/stock/TEMPLATE.md`'s Known Pitfalls for the same issue found and fixed in the stock template.

## Known pitfalls

- None recorded yet beyond the entry-header spacing rule above (already applied in this template from the start, not a fix-after-the-fact).
