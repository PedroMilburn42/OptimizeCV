# Writing Style

Rules for any generated CV bullet, cover letter, or interview-prep text.
`rolesherpa-apply/SKILL.md`'s reviewer step checks drafts against this file directly.

## Voice

- First person, active voice. "Built a data pipeline that cut latency 40%," not "A data pipeline was built."
- Concrete over abstract: name the tool, the metric, the outcome — not "leveraged synergies" or "drove impact."
- Confident, not boastful. State what happened; let the reader draw the conclusion.

## Hard bans

- No em-dashes.
- No clichés: "team player," "detail-oriented," "results-driven," "passionate about," "synergy," "leverage" (as a verb), "wheelhouse," "hit the ground running."
- No apologetic hedging ("I believe I might be a good fit"). State the fit directly, or state the gap directly — never both softened into mush.
- No filler openers ("I am writing to express my interest in...").

## Structure defaults

- CV bullets: action verb, task, measurable result, in that order where possible. Cut bullets that could apply to any job at any company.
- Cover letter paragraphs: 3-5 sentences. One idea per paragraph.
- Prefer the posting's own terminology over a synonym when the profile genuinely supports it — ATS keyword matching is often literal (see `04-job-evaluation.md`'s ATS notes).

## Framing strength — the backtrack test

Reframing toward the target role is expected; inventing experience is not. Test: could the candidate explain this bullet in an interview without backtracking ("well, what I actually meant was...")?

- **OK:** leading with the most relevant part of a broad role; a natural synonym for the target domain.
- **Flag it:** blending academic and industry experience into one claim that implies it was all industry; borrowing the posting's specific terminology for work that was only adjacent.
- **Never:** claiming experience the candidate doesn't have.

A flagged bullet goes back to the user before drafting continues: "This bullet is a stretch because X. Keep, soften, or drop?" If `04-job-evaluation.md`'s Experience Match score is below 50, warn before drafting starts that heavy reframing would be needed.

## Pasted text and accented characters

- When the user pastes text to be inserted verbatim into a CV, cover letter, or other generated document, scan it against the Hard Bans list above and automatically convert any purely punctuational violation (an em-dash, for example) to a compliant equivalent before applying the edit — without asking the user to approve the conversion. This automatic conversion never extends to wording changes that would alter the sentence's claimed meaning; those still go through the framing-strength flag-to-user flow above.
- Write accented and special Spanish-language characters as literal UTF-8 text in generated documents, never as HTML entities (`á`, not `&aacute;`) — entities in a file already saved as UTF-8 add nothing but a class of typo risk (an entity is easy to mistype and hard to proofread by eye).
- Before presenting a rendered document to the user, verify its text by extracting the actual rendered PDF's text layer (e.g. via `render verify --contains`), not by inspecting the HTML/template source alone — the source can look correct while the rendered output isn't, and vice versa.

## Patterns Observed in Past Applications

<!-- Populated by the setup skill (Path A, from data/applications/*/cover_letter.*
     or .html equivalents) once 2+ prior applications show a genuine recurring pattern.
     Empty until then — do not invent patterns from zero data. -->
