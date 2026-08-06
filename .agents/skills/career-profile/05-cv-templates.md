# CV Template Guidance

<!-- BEGIN ACTIVE-TEMPLATE (managed by add-template — do not edit by hand) -->
> **Active template override: `modern-safe`**
>
> A custom template is active. Where this block conflicts with the stock guidance below, this block wins.
>
> - **Template skeleton:** `templates/cv/modern-safe/template.html`
> - **Manifest:** `templates/cv/modern-safe/TEMPLATE.md`
> - **Fonts:** Helvetica Neue / Arial system font stack — no bundled font files
> - **Page limit:** 2 page(s) target, 3 tolerated (see this file's Structure section — `--pages 2 --max-pages 3`)
> - **Output file:** `data/applications/<company>-<role>-<YYMMDD>/CV-<company>-<role>-<YYMMDD>.html`; no font files to copy alongside the output
<!-- END ACTIVE-TEMPLATE -->

## Structure

Base every generated CV on `templates/cv/stock/template.html`
(`TEMPLATE.md` in the same folder documents its style rules and
`break-inside: avoid` conventions). Sections, in order: Profile
statement, Experience, Education, Technical Skills.

- Always in English.
- Output file: `data/applications/<company>-<role>-<YYMMDD>/CV-<company>-<role>-<YYMMDD>.html` (and `.pdf` once rendered) — see `06-cover-letter-templates.md`'s Structure section for the matching cover-letter convention.
- Single-column layout — required for reliable ATS text-extraction order (`document-pipeline` verification checks this).
- **2 pages is the target; 3 is tolerated as an escape valve, never a default.** Render with `python -m rolesherpa.cli render verify <path> --pages 2 --max-pages 3` before presenting — never eyeball the HTML source and assume it's fine, page-break behavior depends on actual content length. A CV should land on 2 pages whenever the protected content (below) fits; only expand to 3 when it doesn't. See `rolesherpa-apply/SKILL.md` Step 5 for the exact escalation sequence (try 2 → protection rule would be violated → try 3 → still violated → pause and ask the user).
- Contact details (email, phone) must appear as literal text, never icon-only — an icon-only contact detail is invisible to ATS parsing.

## Tailoring rules

- Reframe the profile statement and experience bullets to the specific posting's language, without inventing anything not in `data/profile/candidate-profile.md`.
- Reorder or re-emphasize bullets by relevance to the posting; don't reorder whole sections.
- Nice-to-have requirements the candidate genuinely meets: surface them even if not asked.

## Relevance-weighted cutting (when content overflows 2 pages)

Score each candidate bullet by: (a) relevance to this posting's keywords and responsibilities, (b) uniqueness — is it duplicated elsewhere, (c) narrative load — does the cover letter depend on it. Cut the lowest-total-score bullet first, regardless of which section it's in. An older-role bullet that hits posting keywords outranks a recent-role bullet that doesn't — don't apply a static "cut the oldest role first" rule.

**Protected content — never cut silently, at any page count:**

- **Employment continuity.** Never drop an entire role from `data/profile/candidate-profile.md`'s Professional Experience if doing so leaves a visible gap between the roles on either side of it (compare end date of the role below it to the start date of the role above it — any gap over ~1 month reads as unexplained to a recruiter). If a role must be trimmed for space, trim its bullets, never remove the role header/dates entirely.
- **Top-tier quantified achievements.** A bullet carrying a concrete, verifiable metric (budget size, team size, % improvement, uptime figure, project value in currency) ranks above an unquantified bullet in the same role, regardless of the relevance score in the paragraph above — quantified impact is itself a relevance signal `05`'s scoring undervalues on its own.
- If applying the normal relevance-weighted cut would violate either rule at 2 pages, that is precisely the signal to invoke the page-3 escape valve from the Structure section above — not to cut the protected content. If it would still be violated at 3 pages, `rolesherpa-apply/SKILL.md` Step 5 requires pausing and asking the user before finalizing; this rule is never silently overridden.

## Profile statement templates

Reusable opening-statement arcs live in `data/profile/cv-profile-arcs.md`
(gitignored, personal data) — pick per posting, don't default to the same one
every time. Reorder or lightly reframe wording to the posting's language, but
don't blend multiple arcs into a third, uncommitted-to one.

<!-- Populated by the setup skill (Path A) from data/profile/candidate-profile.md,
     since data/applications/ has no real prior CVs to mine yet per
     rolesherpa-setup/SKILL.md Step 2.5's normal source. This section stays
     empty in the tracked skill file; the arcs themselves are personal data and
     live outside the skill tree. Once 2+ real applications exist,
     rolesherpa-setup --section cv-templates may add further arcs mined from
     what actually got used — it should not silently replace existing ones
     without flagging the conflict, per that skill's Path A conflict-resolution
     rule. -->
