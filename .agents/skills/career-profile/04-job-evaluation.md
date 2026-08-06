# Job Evaluation Framework

Scoring framework used by `rolesherpa-apply/SKILL.md` (full evaluation, with company
research) and `rolesherpa-rank/SKILL.md` (triage-only, posting text against this
file — no company research, no salary lookup).

## Ambiguous quantifiable facts

Any quantifiable fact that depends on how it's counted — years of experience, team size, budget figures, and similar — and isn't already stated verbatim in `data/profile/candidate-profile.md`, gets confirmed explicitly with the user before it appears in a score, a CV, or a cover letter. Never compute it (e.g. from a career-start date and today's date), assume it, or silently carry it over from a prior document (an old CV, a cached score). A comparative audit of a sister project's session (2026-08-03) found exactly this failure mode: a team-size figure inherited unquestioned from an old CV turned out to be wrong once the user was actually asked.

## Scoring Dimensions

### 1. Technical Skills Match (0-100)

| Score | Meaning |
|-------|---------|
| 80-100 | Core requirements are primary skills |
| 60-79 | Most requirements match, 1-2 learnable gaps |
| 40-59 | Partial match, significant upskilling needed |
| 0-39 | Fundamental mismatch |

Cross-reference `data/profile/job-evaluation-calibration.md` for the candidate's strong/moderate/weak technical-skill match areas — this file never inlines that calibration directly.

### 2. Experience Match (0-100)

| Score | Meaning |
|-------|---------|
| 80-100 | Direct experience in the same domain and role type |
| 60-79 | Related experience, transferable skills clear |
| 40-59 | Adjacent experience, would need to make the case |
| 0-39 | Unrelated experience |

### 3. Behavioral/Culture Fit (0-100)

| Score | Meaning |
|-------|---------|
| 80-100 | Culture strongly matches behavioral preferences (see `data/profile/behavioral-profile.md`) |
| 60-79 | Mixed signals but mostly compatible |
| 40-59 | Some friction areas |
| 0-39 | Significant culture mismatch |

**Red flags to research:** disorganization, maintenance-heavy work over greenfield development, poor leadership chemistry — check reviews, media coverage, and network contacts for insider signal.

### 4. Location & Logistics (Pass/Fail + Notes)

- Within commute range, or remote with occasional office: **PASS**
- Requires relocation: **FAIL** (deal-breaker)
- Frequent international travel: **FLAG** (surface to the user, don't auto-exclude)

### 5. Career Alignment & Motivation (0-100)

| Score | Meaning |
|-------|---------|
| 80-100 | Strongly aligned with career direction, clear growth path |
| 60-79 | Good role but only partially aligned with long-term goals |
| 40-59 | Decent job but doesn't build toward career goals |
| 0-39 | Dead end or backwards step |

Cross-reference `data/profile/job-evaluation-calibration.md` for career goals (including target-title fallback order), the motivation filter, and life-situation constraints (salary baseline, flexibility, employment-discretion requirements) — this file never inlines that calibration directly.

### 6. Salary Benchmark (optional, not currently configured)

If a company salary dataset is ever added to this repo, look it up here
and report it as an index against a stated baseline. No such dataset
exists in this repo today — skip this section rather than fabricating
a number.

## Weighting

- Technical Skills: 30%
- Experience Match: 25%
- Behavioral Fit: 15%
- Career Alignment: 30%
- (Location is pass/fail, not weighted)

## Thresholds

- **Strong Fit** (75+): apply, tailor everything
- **Good Fit** (60-74): apply, address gaps in the cover letter
- **Moderate Fit** (45-59): discuss with the user before proceeding
- **Weak Fit** (30-44): skip unless there's a strategic reason
- **Poor Fit** (<30): skip

## Output Format (full evaluation — `rolesherpa-apply/SKILL.md`)

```
## Job Fit Evaluation: [Role] at [Company]

| Dimension | Score | Notes |
|-----------|-------|-------|
| Technical Skills | XX/100 | ... |
| Experience Match | XX/100 | ... |
| Behavioral Fit | XX/100 | ... |
| Location | PASS/FAIL | ... |
| Career Alignment | XX/100 | ... |

**Overall Score: XX/100**

### Verdict: [Strong Fit / Good Fit / Moderate Fit / Weak Fit / Poor Fit]

### Key Strengths
### Gaps to Address
### Recommendation

### Company Research Checklist
- [ ] Company website (mission, values, recent news)
- [ ] Review sites
- [ ] LinkedIn (team size, recent hires, connections)
- [ ] Media coverage (growth, restructuring, workplace issues)
```

## Pre-Application: Call the Employer

Suggest calling the posting's contact person **only when there are
substantive questions** — never just to "be remembered." Good reasons:
ambiguous requirements, unclear which competencies are essential, vague
day-to-day description. The call's purpose is gathering information, not
delivering a pitch; reference what was learned naturally in the cover
letter if a call happens.

## Calibration from Past Applications

<!-- Populated by the setup skill (Path A) from data/applications/*/outcome.md
     once resolved applications exist: role types/sectors that reached
     interview or offer are a confirmed strong-fit signal; repeated
     no-response or rejection patterns get noted here too. -->
