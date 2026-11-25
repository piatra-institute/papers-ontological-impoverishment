"""Recorded analysis: gaps in published Pew tables and the summary figure."""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import analysis  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"

SHORT = {
    "c": "Prevent serious disease",
    "b": "Process information faster",
    "f": "Hear far beyond typical",
    "d": "Greatly increased strength",
    "e": "See patterns far beyond typical",
    "a": "Slow aging, live decades longer",
}


def figure(exc: dict, path: Path) -> None:
    plt.rcParams.update({"font.size": 13, "font.family": "DejaVu Sans"})
    fig, ax = plt.subplots(figsize=(9.0, 5.6))
    codes = list(analysis.ITEM_ORDER)
    for i, code in enumerate(codes):
        y = len(codes) - 1 - i
        p = exc["items"][code]["party"]
        r = exc["items"][code]["religiosity"]
        ax.plot([p["b"], p["a"]], [y + 0.15, y + 0.15], color="#8a8a8a", lw=2, zorder=1)
        ax.scatter([p["b"]], [y + 0.15], color="#c0392b", s=70, zorder=2, label="Rep/lean Rep" if i == 0 else None)
        ax.scatter([p["a"]], [y + 0.15], color="#2c5aa0", s=70, zorder=2, label="Dem/lean Dem" if i == 0 else None)
        ax.plot([r["b"], r["a"]], [y - 0.15, y - 0.15], color="#8a8a8a", lw=2, ls=":", zorder=1)
        ax.scatter([r["b"]], [y - 0.15], color="#6b4f2a", marker="s", s=60, zorder=2, label="High religious commitment" if i == 0 else None)
        ax.scatter([r["a"]], [y - 0.15], color="#d9a441", marker="s", s=60, zorder=2, label="Low religious commitment" if i == 0 else None)
    ax.set_yticks(range(len(codes)))
    ax.set_yticklabels([SHORT[c] for c in reversed(codes)])
    ax.set_xlabel("% very or somewhat excited (Pew, Nov. 2021)")
    ax.set_xlim(25, 80)
    ax.grid(axis="x", color="#dddddd")
    ax.legend(loc="lower right", fontsize=11, frameon=True)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def main() -> int:
    OUT.mkdir(exist_ok=True)
    exc = analysis.excitement_gaps()
    reg = analysis.regulation_gaps()
    med = analysis.meddling_2016()
    results = {
        "inputs": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((HERE / "data").glob("*.csv"))},
        "excitement_2022": exc,
        "regulation_2022": reg,
        "meddling_2016": med,
        "provocation_test": analysis.provocation_test(exc, reg),
        "environment": {"python": sys.version.split()[0], "platform": platform.platform(), "matplotlib": matplotlib.__version__},
    }
    (OUT / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    figure(exc, OUT / "fig_gaps.png")
    s = exc["summary"]
    print(f"party gap {s['party_gap_min']}-{s['party_gap_max']} (Dem higher on {s['n_dem_higher']}/{s['n_items']}); "
          f"religiosity gap {s['religiosity_gap_min']}-{s['religiosity_gap_max']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
