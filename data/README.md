# data/

Personal runtime state for the job search. Everything under this directory
except this file, `applications/.gitkeep`, and `profile/.gitkeep` is
gitignored — none of it ships in the repo, and none of it should (job
postings, application history, contact details, and the candidate's
profile data are Carlos's personal data, not portfolio content).

## Layout

- **`seen_jobs.json`** — created by `rolesherpa-scrape/SKILL.md` via
  `JsonStore(path, default={"seen": {}})`. Deduplication state across
  scrape runs; `rolesherpa-rank/SKILL.md` extends entries additively
  (`rank_score`, `rank_verdict`, `rank_date`).
- **`job_search_tracker.csv`** — created by `rolesherpa-outcome/SKILL.md` via
  `CsvStore`. One row per application; header is fixed
  (`date,company,sector,role,role_type,channel,status,contact_person,
  fit_rating,notes,cv_file,cover_letter_file,source`). Rows are appended,
  never reordered or rewritten in place except by an explicit `save()`
  (full replace).
- **`applications/<company>-<role>-<YYMMDD>/`** — the single folder for
  one application's entire lifecycle: draft, submitted, and archived
  material all live here, no separate staging directory. `company` and
  `role` are lowercase with underscores for internal word separation; a
  single dash separates the company, role, and date blocks (e.g.
  `acme_corp-software_engineer-260101`); the date is the folder's
  creation date (when `rolesherpa-apply/SKILL.md` first drafted the
  CV/cover letter), not the submission or outcome date. Created by
  `rolesherpa-apply/SKILL.md`, then written into by
  `rolesherpa-outcome/SKILL.md` and `rolesherpa-interview/SKILL.md`.
  Fixed file names inside: `CV-<company>-<role>-<YYMMDD>.html`,
  `CV-<company>-<role>-<YYMMDD>.pdf`, `CL-<company>-<role>-<YYMMDD>.html`,
  `CL-<company>-<role>-<YYMMDD>.pdf`, `job_posting.md`, `outcome.md`,
  `interview_prep_<stage>.md`.
- **`profile/`** — the candidate's own data: `candidate-profile.md`,
  `behavioral-profile.md`, `search-queries.md`. Bootstrapped from
  `templates/profile/*.md` by `rolesherpa-setup/SKILL.md` on a fresh
  checkout (never overwriting an existing populated file), and restored
  to blank by `rolesherpa-reset/SKILL.md` the same way. Moved out of
  the tracked `.agents/skills/`/`.claude/skills/` tree specifically
  because that coupling once caused real contact info to be committed
  to git as a side effect of an unrelated skill-tree change — see the
  `decouple-profile-data-from-skills` change.

## Why JSON/CSV, not a database

Per `PROJECT_BRIEF.md` §4b: plain JSON/CSV files, no SQLite. `JsonStore`
and `CsvStore` (`src/rolesherpa/storage/`) are the only two `StoragePort`
adapters this project needs.
