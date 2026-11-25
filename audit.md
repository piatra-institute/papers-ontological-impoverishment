# Audit

Dated log of editorial passes and verification runs. Newest first.

## 2026-11-26: first complete version

Scope: new paper written from seed leads (two earlier manuscripts, an evidence memo, seven owner messages); nothing from the seeds is cited.
Built: brief, research, references (43 entries), sources, claims (95), recorded run `pew-gaps` re-analysing published Pew aggregates (no respondent-level data), figure, manuscript, metadata, README, CITATION.cff.
Verification:
  - `check_numerals.py`: every numeral in PAPER.md bound in claims.yaml (years and labels listed separately).
  - fetch_pew.py: 19 text-extractable transcribed values found on their stated PDF pages; chart-bar values transcribed visually.
  - refs --verify: no identity mismatch.
  - standards: no FAIL; abstract under 250 words.
  - build: no missing-character warnings; every page rendered at 80 dpi and inspected.
  - Source claims all `verified: false`; coverage pending; editorial and visual reviews pending for an independent reviewer.
