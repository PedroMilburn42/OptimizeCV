# Document rendering: WeasyPrint (HTML/CSS) over LaTeX

`PROJECT_BRIEF.md` §4b left the document-rendering technology open —
the reference implementation this project's functional scope was drawn
from uses LaTeX (moderncv + a custom `cover.cls`, compiled with
`lualatex`/`xelatex`, verified with external `pdfinfo`/`pdftotext` from
`poppler-utils`). RoleSherpa uses WeasyPrint (HTML/CSS → PDF) and
`pypdf` instead.

**Why:** a LaTeX toolchain (TeX Live/MiKTeX, hundreds of MB) is a heavy,
non-Python external dependency that sits awkwardly inside "a real,
testable Python library" — it can't be `uv add`ed, and its templates
aren't unit-testable except by compiling and inspecting the output.
WeasyPrint is an ordinary Python package; its templates are HTML/CSS,
which can be parsed and asserted on structurally, not just visually.
`pypdf` similarly replaces `poppler-utils`: pure Python, no external
binary on `PATH`, so the verification step (page count, ATS text-layer
extraction, keyword coverage) lives inside the same package instead of
shelling out — a direct improvement on the reference implementation's
own PDF-verification script, which depends on `pdfinfo`/`pdftotext`
being separately installed.

## Consequences

- CV/cover-letter templates registered via `rolesherpa-add-template/SKILL.md` are HTML/CSS with `[PLACEHOLDER]` tokens, not LaTeX `.tex` files — the same substitution convention the reference implementation uses, no new templating-engine dependency (Jinja2 etc.) needed.
- Page-break control — the single biggest source of iteration in the reference implementation's own apply workflow (orphaned entry titles, manual page-break hints) — becomes CSS `break-inside: avoid` / `break-after: avoid` instead of LaTeX macros. The stock templates (`templates/cv/stock/`, `templates/cover_letters/stock/`) use these rules on every entry/heading.
- WeasyPrint's CSS page-break model is less mature than LaTeX's for complex multi-page layouts. Accepted trade-off: the stock templates are deliberately simple single-column layouts, which is also the property the reference implementation's own stock template relies on for reliable ATS text-extraction order.
- A macOS/Homebrew dynamic-linking quirk: WeasyPrint's wheel imports cleanly but fails to `dlopen` `libgobject-2.0` unless `/opt/homebrew/lib` is on `DYLD_FALLBACK_LIBRARY_PATH`, even with Pango/cairo/glib already installed via Homebrew. Not a missing dependency — `src/rolesherpa/documents/render.py` sets the env var itself before the first `import weasyprint` in the process, so every entry point (tests, CLI, skills) picks it up transparently without the developer needing to discover or work around it.
