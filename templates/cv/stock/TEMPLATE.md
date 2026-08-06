# Template: stock (CV)

- **Type:** CV
- **Renderer:** WeasyPrint (HTML/CSS → PDF) — see `design.md` D6 for why WeasyPrint over LaTeX
- **Page limit:** 2 page(s)
- **Fonts:** Helvetica Neue / Arial system font stack — no bundled font files, no `Path` overrides needed
- **Class/packages:** standard HTML/CSS, no dependencies beyond WeasyPrint

## Render + verify command

    python -m rolesherpa.cli render verify <output.pdf> --pages 2

## Style rules

- Single-column layout only — safe for ATS text-extraction reading order (matches the reference implementation's own stock-template safety property).
- Section headings (`h2`) use `break-after: avoid` so a heading never sits alone at the bottom of a page.
- Each experience/education entry (`.entry`) uses `break-inside: avoid` so a role's title never splits from its bullets across a page break — the CSS equivalent of the reference implementation's LaTeX page-break fix for orphaned entry titles.
- Contact details (email, phone) are printed as literal text, never icon-only — required for the ATS text-layer check in `document-pipeline` verification.

## Known pitfalls

- `.entry-header`'s two `<span>` children (title/company vs. dates) must have a literal space between their closing/opening tags in the HTML source, even though `display: flex; justify-content: space-between` visually separates them — without it, PDF text-layer extraction concatenates them with no separator (e.g. `"Example CorpJan 2024"`), which risks ATS date-range parsing. Fixed 2026-08-02; keep the space if this file is ever regenerated from scratch.
