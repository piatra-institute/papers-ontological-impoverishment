# Audit

Dated log of editorial passes and verification runs. Newest first.

## 2026-11-26: revision round 3 (owner decision on F4)

Changes: removed every comparison between party and religious-commitment differences from the abstract, survey section, verdict, limits, figure and caption. Religiosity appears in one descriptive sentence saying it is correlated with party and cannot be separated in published tables. The 2016 report is used only to note that it has no party breakdown. Dropped scheufele2009 and the religiosity claims. The figure was redrawn with party only and `pew-gaps` re-recorded (the P2 religiosity scoring was removed from the analysis).
Verification: numeral audit 34 bound, 0 unbound; build 21 pages, 0 missing glyphs, all pages inspected; standards PASS (abstract 241 words); refs --verify no mismatch; check 95 PASS, 22 NOT_APPLICABLE, 43 NEEDS_REVIEW (40 unverified source claims, coverage, editorial, visual), 0 FAIL.

## 2026-11-26: revision round 2 (closure check: 11 of 12 closed)

Changes:
  - Survey sentences restated as descriptive bivariate comparisons in the abstract, survey section, figure caption and verdict. Removed "similar to one step" and "a range that contains every party gap". The confounding of party and religiosity is stated in the same sentences (F4).
  - Removed the uncheckable source claims buchanan, sen-capability, nussbaum-body, aho and hester. The works stay cited for their well-known thesis only, listed as cited-unread in sources.md; Hester's prose narrowed.
  - Proposition 2 proof updated for the stay/move split. The political test is scoped at its first statement in the introduction. The levin-layers rationale now counts six studies.
  - Display equations kept with their lead-in lines; the widowed "Definition." line is fixed.
Verification: numeral audit 44 bound, 0 unbound; build 22 pages, 0 missing glyphs, all pages rendered and inspected; standards PASS (abstract 250 words); refs --verify no mismatch; check 106 PASS, 22 NOT_APPLICABLE, 45 NEEDS_REVIEW (42 unverified source claims, coverage, editorial, visual), 0 FAIL.

## 2026-11-26: revision round 1 (independent referee, 9 majors, 3 minors)

Scope: responses to every finding.
Changes:
  - Reachable set split into stay and move components so an unlivable or coerced start no longer empties it; propositions rechecked (F1).
  - Admissible alternatives now carry a justification filter; frontier limit and impoverishment of inquiry use an explicit horizon (F2).
  - Proposition 1 restated with its exogenous-institution condition, monotonicity within a regime, and a strict income-reversal example; abstract qualified (F3).
  - "About twice as much" and the ratio dropped; party gaps now compared with adjacent religiosity steps and with group coverage, and the bivariate limitation is explicit (F4).
  - Verdict restated at the scale of the survey construct; regulation gaps for non-bodily technologies added; ATP W99 microdata need a Pew account, so the joint model was not attempted (F5).
  - Capability-theory characterisation corrected, with Mitra, Nussbaum 2006 and Venkatapuram; contribution narrowed to routes, intermediate states and research-dependent route sets (F6).
  - Added Buchanan et al. 2000, Daniels 2007, Mitra 2006, Nussbaum 2006, Venkatapuram 2011, Pattanaik and Xu 1990, Scheufele et al. 2009, Aho 2009 (F7) and Blackiston and Levin 2013 (F8), each registry-checked.
  - Locators removed for uninspected texts; FCM pages cited via Engelland; Earle attribution fixed (F9); Bradshaw initials, gumuskaya2025 article number (F10); half-sample margins for regulation (F11); meta-commentary removed (F12).
Verification:
  - Re-recorded `pew-gaps` (tests 7/7 pass; fetch check 30/30 transcribed text values found).
  - check_numerals.py: 44 numerals bound, 0 unbound.
  - build: 21 pages, no missing-character warnings; all pages rendered and inspected; equations split to fit the text width.
  - standards PASS (abstract 248 words); refs --verify no mismatch (nussbaum2006 DOI moved to a note because its registry record lacks an author); check: 106 PASS, 22 NOT_APPLICABLE, 50 NEEDS_REVIEW (47 unverified source claims, coverage, editorial, visual), 0 FAIL.

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
