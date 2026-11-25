"""Fetch the two Pew Research Center report PDFs and check the transcribed tables.

This script is separate from the recorded analysis. It downloads the published
reports into data/raw/ (not committed), records their hashes in
data/raw_manifest.json, and checks every transcribed value that is extractable
as text from the stated PDF page. Values printed inside chart bars are images;
those are reported as visual transcriptions in data/transcription_check.json.

Usage: uv run python fetch_pew.py
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "data" / "raw"
REPORTS = {
    "2016": "https://www.pewresearch.org/wp-content/uploads/sites/9/2016/07/PS_2016.07.26_Human-Enhancement-Survey_FINAL.pdf",
    "2022": "https://www.pewresearch.org/wp-content/uploads/sites/20/2022/03/PS_2022.03.17_AI-HE_REPORT.pdf",
}
UA = {"User-Agent": "Mozilla/5.0 (generic research client)"}


def fetch() -> dict:
    RAW.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for year, url in REPORTS.items():
        target = RAW / f"pew{year}.pdf"
        if not target.exists():
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                target.write_bytes(r.read())
        data = target.read_bytes()
        manifest[year] = {
            "url": url,
            "file": f"data/raw/pew{year}.pdf",
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
    manifest["fetched_utc"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return manifest


def page_text(pdf: Path, page: int) -> str:
    out = subprocess.run(["pdftotext", "-layout", "-f", str(page), "-l", str(page), str(pdf), "-"],
                         capture_output=True, text=True, check=True).stdout
    return re.sub(r"\s+", " ", out)


def check_rows() -> dict:
    results = {"text_checked": [], "visual_only": []}
    if shutil.which("pdftotext") is None:
        results["note"] = "pdftotext unavailable; no automatic check"
        return results
    reg = list(csv.DictReader(open(HERE / "data" / "pew2022_regulation_by_party.csv")))
    for row in reg:
        text = page_text(RAW / "pew2022.pdf", int(row["pdf_page"]))
        label = row["group"]
        pattern = re.escape(label) + r"\s+" + row["pct_not_far_enough"] + r"\s+" + row["pct_too_far"] + r"\b"
        # The layout sometimes prints the two values before the row label.
        alt = row["pct_not_far_enough"] + r"\s+" + row["pct_too_far"] + r"\s+" + re.escape(label)
        found = bool(re.search(pattern, text) or re.search(alt, text))
        results["text_checked"].append({"table": "regulation", "row": row, "found": found})
    moe = list(csv.DictReader(open(HERE / "data" / "pew_margins_of_error.csv")))
    for row in moe:
        text = page_text(RAW / f"pew{row['survey']}.pdf", int(row["pdf_page"]))
        n = f"{int(row['unweighted_n']):,}"
        found = n in text and row["moe_pct_points"] in text
        results["text_checked"].append({"table": "margins", "row": row, "found": found})
    for name in ("pew2022_excitement_by_group.csv", "pew2016_meddling_by_religiosity.csv"):
        results["visual_only"].append({
            "table": name,
            "note": "values are printed inside chart bars (images); transcribed visually from a 160-300 dpi render and cross-checked against the topline where available",
        })
    return results


if __name__ == "__main__":
    manifest = fetch()
    (HERE / "data" / "raw_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    check = check_rows()
    (HERE / "data" / "transcription_check.json").write_text(json.dumps(check, indent=2) + "\n")
    bad = [c for c in check["text_checked"] if not c["found"]]
    print(f"text-checked rows: {len(check['text_checked'])}; not found: {len(bad)}")
    for c in bad:
        print("  NOT FOUND:", c["table"], c["row"])
