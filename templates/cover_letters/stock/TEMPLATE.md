# Template: stock (Cover letter)

- **Type:** Cover letter
- **Renderer:** WeasyPrint (HTML/CSS → PDF) — see `design.md` D6 for why WeasyPrint over LaTeX
- **Page limit:** 1 page(s)
- **Fonts:** Helvetica Neue / Arial system font stack — no bundled font files
- **Class/packages:** standard HTML/CSS, no dependencies beyond WeasyPrint

## Render + verify command

    python -m rolesherpa.cli render verify <output.pdf> --pages 1

## Style rules

- Single paragraph flow, no columns.
- The highlight bullet list uses `break-inside: avoid` so it never splits across a page.
- Keep to 3–4 short paragraphs plus the bullet list — trim content rather than shrinking margins or line spacing if it overflows to a second page (same relevance-weighted cutting discipline the reference implementation's own apply workflow uses, applied here instead of LaTeX geometry tweaks).

## Known pitfalls

- None recorded yet.
