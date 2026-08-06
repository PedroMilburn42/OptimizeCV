# documents/

Personal source materials for onboarding via `rolesherpa-setup/SKILL.md` Path A.
Everything here except this file and the `.gitkeep` placeholders is
gitignored — these are Carlos's real CV, LinkedIn export, diplomas, and
reference letters, not portfolio content.

## Layout

- **`cv/`** — CV/resume files (PDF, DOCX, or plain text).
- **`linkedin/`** — LinkedIn data export. If more than one export is
  present, `setup` uses the most recently modified file.
- **`diplomas/`** — degree certificates / transcripts.
- **`references/`** — reference letters.

The per-application archive (submitted CV/cover letter copies, fetched
job postings, outcomes, interview prep) is generated state, not
user-supplied source material — it lives under `data/applications/`,
documented in `data/README.md`.

Drop what you have into the matching subfolder, then run the setup
skill — it reads everything here, cross-references it for consistency,
and proposes changes to `data/profile/` before writing anything.
Re-running setup as you add more documents is safe and idempotent; it
never proposes the same addition twice.
