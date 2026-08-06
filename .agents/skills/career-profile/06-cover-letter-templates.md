# Cover Letter Template Guidance

<!-- BEGIN ACTIVE-TEMPLATE (managed by add-template — do not edit by hand) -->
> **Active template override: `modern-safe`**
>
> A custom template is active. Where this block conflicts with the stock guidance below, this block wins.
>
> - **Template skeleton:** `templates/cover_letters/modern-safe/template.html`
> - **Manifest:** `templates/cover_letters/modern-safe/TEMPLATE.md`
> - **Fonts:** Helvetica Neue / Arial system font stack — no bundled font files
> - **Page limit:** exactly 1 page(s), no tolerance (`--pages 1`)
> - **Output file:** `data/applications/<company>-<role>-<YYMMDD>/CL-<company>-<role>-<YYMMDD>.html`; no font files to copy alongside the output
<!-- END ACTIVE-TEMPLATE -->

## Structure

Base every generated cover letter on
`templates/cover_letters/stock/template.html` (`TEMPLATE.md` in the
same folder documents its style rules). Sections: sender block, date,
recipient, opening paragraph, one or two body paragraphs, an optional
highlight bullet list, closing paragraph, signature.

- Match the language of the job posting (an English posting gets an English letter; a Spanish posting gets a Spanish letter).
- Address a named contact if the posting gives one, otherwise "Dear Hiring Manager" (or the equivalent in the posting's language).
- Output file: `data/applications/<company>-<role>-<YYMMDD>/CL-<company>-<role>-<YYMMDD>.html` (and `.pdf` once rendered) — see `05-cv-templates.md`'s Structure section for the matching CV convention.
- Exactly 1 page. Render with `python -m rolesherpa.cli render verify <path> --pages 1` before presenting.
- Any mention of agentic coding or AI tooling used to build the application must name whichever host actually assisted (see `career-profile`'s host-attribution note in `setup`) — never a hardcoded tool name, and never omit it if it's genuinely mentioned.

## Tailoring rules

- Open with the single strongest match to the posting, not a generic "I am writing to express interest" line.
- Connect specific experience to specific posting requirements — no restating the CV in prose.
- Acknowledge genuine gaps honestly; bridge with adjacent experience rather than glossing over them.
- Follow `03-writing-style.md` exactly, especially the hard bans.

## Trimming (when content overflows 1 page)

First cut: sentences that restate what a bullet already said. Second
cut: a bullet that doesn't hit posting keywords. Never shrink margins
or line spacing to force a fit — cut content instead.

**Last resort — pause and ask, don't cut silently:** if the letter
still doesn't fit after both cuts above, the only thing left to cut is
a bullet that *does* hit posting keywords — the strongest content in
the letter. Don't apply that cut unilaterally. Stop and ask the user,
the same gate `05-cv-templates.md`'s structural cuts use for the CV:
name the specific bullet that would have to go and why, and wait for
their decision (cut it / cut something else instead / tighten other
paragraphs further to make room) before finalizing. A cover letter has
no page-3 escape valve like the CV does — see `05-cv-templates.md` and
this file's Structure section for why 1 page stays a hard limit here —
so this pause is the only safeguard against silently losing the
letter's best point.
