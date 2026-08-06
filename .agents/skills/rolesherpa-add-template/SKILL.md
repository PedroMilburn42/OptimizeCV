---
name: rolesherpa-add-template
version: 1.0.0
description: >
  Registers a custom HTML/CSS CV or cover letter template in place of the
  stock ones, verifies it renders correctly, and activates it for
  rolesherpa-apply/SKILL.md. Triggers on: custom CV template, custom cover letter
  template, add a template, change my CV design, /rolesherpa-add-template
allowed-tools: Read, Write, Edit, Bash(python -m rolesherpa.cli render *)
---

# Add Template — Register a Custom CV or Cover Letter Template

## Context and role

RoleSherpa ships one stock template per document type
(`templates/cv/stock/`, `templates/cover_letters/stock/`, both
HTML/CSS rendered via WeasyPrint — see `design.md` D6 for why HTML/CSS
instead of LaTeX). This skill lets the user swap in their own design
without touching `rolesherpa-apply/SKILL.md` itself. `$ARGUMENTS` may contain a
subcommand, a file path, or nothing.

## Task

### Step 0 — parse arguments

- `--list` → Glob `templates/**/TEMPLATE.md`, print name/type/page-limit/active-or-not for each, stop.
- `--use <name>` → **switch mode**: find the manifest whose parent folder matches `<name>` (ambiguous match → list and ask the user to rename one); `--use default` deactivates any custom template. Skip Steps 1-4, go straight to Step 5 with the resolved metadata.
- A file path or pasted HTML → carry it into Step 1 as the source.
- Otherwise → start registration at Step 1.

### Step 1 — type and source

Ask (skip anything `$ARGUMENTS` already answered): **CV** or **cover
letter**? Where's the source — a path, pasted HTML, or a directory with
HTML plus a CSS file? Read every provided file. If it references
assets (a font file, an image) not already in the source, confirm the
user has them.

### Step 2 — capture template metadata

Infer from the source first (`<style>` rules, `@page` size/margins, any
`@font-face`), present inferences for confirmation rather than asking
blind:

1. **Name** — kebab-case, must not collide with `templates/{cv,cover_letters}/<existing>`.
2. **Fonts** — bundled font files (copy into the template folder, record relative paths) vs. system fonts (record the name, note the user's machine needs it installed).
3. **Style rules** the drafter must preserve: color scheme, section order, heading style, spacing, bullet formatting.
4. **Page limit** — default 2 pages for a CV, 1 for a cover letter.
5. **Known pitfalls** (optional) — CSS rules that break with certain content, characters needing escaping.

### Step 3 — store the template

Create `templates/{cv,cover_letters}/<name>/`:

- **`template.html`** (+ any `.css`) — personal data replaced with `[PLACEHOLDER]` tokens (`[YOUR_NAME]`, `[YOUR_EMAIL]`, ...) matching the stock templates' convention, so it stays shareable and profile-agnostic. Preserve the structure and styling exactly as provided.
- **Font files**, if bundled, under `fonts/` with paths adjusted to be relative to the template folder.
- **`TEMPLATE.md`** manifest, in the format `templates/cv/stock/TEMPLATE.md` already uses (Type, Renderer, Page limit, Fonts, Class/packages, render+verify command, Style rules, Known pitfalls).

### Step 4 — mandatory test-render (never skip)

A template that has never rendered will fail mid-`apply`, the worst
place to discover it.

1. Copy `template.html` (and, if the template ships a separate `.css` file, copy that too) to scratch files in the same folder, fill every `[PLACEHOLDER]` with realistic dummy content (name, contact line, one education entry, one job entry with 3 bullets — enough to exercise the layout).
2. Render and verify — pass `--css` whenever the template has a separate CSS file, so the verification actually exercises the real styling, not just the bare HTML:
   ```
   python -m rolesherpa.cli render pdf templates/<type>/<name>/_scratch.html templates/<type>/<name>/_scratch.pdf [--css templates/<type>/<name>/_scratch.css]
   python -m rolesherpa.cli render verify templates/<type>/<name>/_scratch.pdf --pages <declared limit>
   ```
3. Compile failure or wrong page count → diagnose (missing font, layout overflow), fix, re-render. If the fix needs something only the user has (a missing font file), ask and wait.
4. On success, note anything worth recording in the manifest's Known Pitfalls.
5. Delete the scratch files (`_scratch.html`, `_scratch.css` if created, `_scratch.pdf`).

Do not proceed to Step 5 until this passes.

### Step 5 — activate

Insert (or replace) a managed block right after the H1/title in
`.agents/skills/career-profile/05-cv-templates.md` (CV) or
`06-cover-letter-templates.md` (cover letter):

```markdown
<!-- BEGIN ACTIVE-TEMPLATE (managed by add-template — do not edit by hand) -->
> **Active template override: `<name>`**
>
> A custom template is active. Where this block conflicts with the stock guidance below, this block wins.
>
> - **Template skeleton:** `templates/<type>/<name>/template.html`
> - **Manifest:** `templates/<type>/<name>/TEMPLATE.md`
> - **Fonts:** <font summary>
> - **Page limit:** exactly <N> page(s)
> - **Output file:** `data/applications/<company>-<role>-<YYMMDD>/CV-<company>-<role>-<YYMMDD>.html` / `.../CL-<company>-<role>-<YYMMDD>.html`; copy any font files the template needs alongside the output, or reference them by relative path
<!-- END ACTIVE-TEMPLATE -->
```

Exactly one managed block per file — replace the whole block on switch,
never stack. `--use default` removes the block entirely; the stock
guidance underneath is untouched and takes over again.

### Step 6 — confirm

Files created, test-render result (page count, engine confirmed
working), and that `rolesherpa-apply/SKILL.md` will now draft from this template.

## Quality criteria

- Never registers a template without a passing test-render at the declared page limit.
- Templates stay profile-agnostic (`[PLACEHOLDER]` tokens) — shareable without leaking personal data.
- Exactly one managed block per guidance file; `--use default` is a clean revert.
- Activation never rewrites the guidance file outside the managed block markers.

## Output format

See Step 6.

## Final check

Before confirming, re-read the guidance file's managed block and
confirm it names the template that was actually just verified — not a
stale name from an earlier attempt in this same session.
