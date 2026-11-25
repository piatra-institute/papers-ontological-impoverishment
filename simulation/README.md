# Analysis of published Pew aggregate tables

This folder re-analyses aggregate percentages that Pew Research Center published in two reports on human enhancement. No respondent-level data are used or redistributed.

- `fetch_pew.py` downloads the two report PDFs into `data/raw/` (ignored by Git), writes their hashes to `data/raw_manifest.json`, and checks every transcribed value that is extractable as text against the stated PDF page (`data/transcription_check.json`). Values printed inside chart bars are images; they were transcribed visually and cross-checked against the report topline where one exists.
- `data/*.csv` are the frozen transcriptions, each row with its printed report page and PDF page.
- `analysis.py` computes unadjusted Democrat-Republican differences with approximate 95% margins for differences between disjoint groups, using the margins that Pew publishes for each group, and a one-point rounding floor. Religious-commitment rows are transcribed as published and summarised, but the paper does not compare them with party, because published tables cannot separate the two.
- `run_all.py` writes `output/results.json` and `output/fig_gaps.png`.
- `test_analysis.py` checks the gap arithmetic and the integrity of the tables.

```bash
uv lock
uv run python fetch_pew.py          # optional; needs network and pdftotext
uv run python -m unittest -v test_analysis
uv run python run_all.py
```

The recorded run is made from the paper root's workspace with `./papers run ontological-impoverishment --id pew-gaps --cwd simulation --artifact simulation/output/results.json --input simulation/data/<file>.csv ... -- uv run python run_all.py`.
