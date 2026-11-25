"""Gap analysis of published Pew aggregate tables (no respondent-level data)."""
from __future__ import annotations

import csv
import math
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"

PARTY = ("Dem/lean Dem", "Rep/lean Rep")
RELIGIOSITY = ("Low religious commitment", "High religious commitment")
ITEM_ORDER = ("c", "b", "f", "d", "e", "a")  # column order of the published chart


def read(name: str) -> list[dict]:
    with open(DATA / name, newline="") as fh:
        return list(csv.DictReader(fh))


def margins(survey: str) -> dict[str, float]:
    return {r["group"]: float(r["moe_pct_points"]) for r in read("pew_margins_of_error.csv") if r["survey"] == survey}


def gap(a: float, b: float, moe_a: float, moe_b: float) -> dict:
    """Difference a - b with an approximate 95% margin for disjoint groups.

    Published margins already include design effects. Published percentages are
    rounded to integers, so the true difference can be smaller by up to one
    point; `rounding_floor` is that conservative lower bound.
    """
    diff = a - b
    moe = math.sqrt(moe_a ** 2 + moe_b ** 2)
    floor = abs(diff) - 1.0
    return {
        "a": a,
        "b": b,
        "difference": diff,
        "moe95": moe,
        "rounding_floor": floor,
        "exceeds_moe": abs(diff) > moe,
        "rounding_floor_exceeds_moe": floor > moe,
    }


def excitement_gaps() -> dict:
    rows = read("pew2022_excitement_by_group.csv")
    m = margins("2022")
    table: dict[str, dict] = {}
    for r in rows:
        table.setdefault(r["item_code"], {"item": r["item"]})[r["group"]] = float(r["pct_excited"])
    items = {}
    for code in ITEM_ORDER:
        t = table[code]
        items[code] = {
            "item": t["item"],
            "us_adults": t["U.S. adults"],
            "party": gap(t[PARTY[0]], t[PARTY[1]], m[PARTY[0]], m[PARTY[1]]),
            "religiosity": gap(t[RELIGIOSITY[0]], t[RELIGIOSITY[1]], m[RELIGIOSITY[0]], m[RELIGIOSITY[1]]),
        }
        items[code]["religiosity_minus_party"] = items[code]["religiosity"]["difference"] - items[code]["party"]["difference"]
    party = [items[c]["party"]["difference"] for c in ITEM_ORDER]
    relig = [items[c]["religiosity"]["difference"] for c in ITEM_ORDER]
    summary = {
        "n_items": len(ITEM_ORDER),
        "n_dem_higher": sum(d > 0 for d in party),
        "n_rep_higher": sum(d < 0 for d in party),
        "party_gap_min": min(party),
        "party_gap_max": max(party),
        "party_gap_mean": sum(party) / len(party),
        "religiosity_gap_min": min(relig),
        "religiosity_gap_max": max(relig),
        "religiosity_gap_mean": sum(relig) / len(relig),
        "ratio_mean_religiosity_to_party": (sum(relig) / len(relig)) / (sum(party) / len(party)),
        "n_party_gap_exceeds_moe": sum(items[c]["party"]["exceeds_moe"] for c in ITEM_ORDER),
        "n_party_floor_exceeds_moe": sum(items[c]["party"]["rounding_floor_exceeds_moe"] for c in ITEM_ORDER),
        "n_religiosity_gap_exceeds_moe": sum(items[c]["religiosity"]["exceeds_moe"] for c in ITEM_ORDER),
        "n_religiosity_exceeds_party": sum(items[c]["religiosity_minus_party"] > 0 for c in ITEM_ORDER),
        "party_moe95": items[ITEM_ORDER[0]]["party"]["moe95"],
        "religiosity_moe95": items[ITEM_ORDER[0]]["religiosity"]["moe95"],
    }
    return {"items": items, "summary": summary}


def regulation_gaps() -> dict:
    rows = read("pew2022_regulation_by_party.csv")
    m = margins("2022")
    out = {}
    for tech in dict.fromkeys(r["technology"] for r in rows):
        t = {r["group"]: r for r in rows if r["technology"] == tech}
        dem, rep = t[PARTY[0]], t[PARTY[1]]
        out[tech] = {
            "us_not_far_enough": float(t["U.S. adults"]["pct_not_far_enough"]),
            "us_too_far": float(t["U.S. adults"]["pct_too_far"]),
            "dem_not_far_enough": float(dem["pct_not_far_enough"]),
            "rep_not_far_enough": float(rep["pct_not_far_enough"]),
            "dem_too_far": float(dem["pct_too_far"]),
            "rep_too_far": float(rep["pct_too_far"]),
            "not_far_enough_gap": gap(float(dem["pct_not_far_enough"]), float(rep["pct_not_far_enough"]), m[PARTY[0]], m[PARTY[1]]),
        }
    gaps = [v["not_far_enough_gap"]["difference"] for v in out.values()]
    return {"items": out, "summary": {
        "n_items": len(gaps),
        "n_dem_more_under_regulation_concern": sum(g > 0 for g in gaps),
        "gap_min": min(gaps),
        "gap_max": max(gaps),
    }}


def meddling_2016() -> dict:
    rows = read("pew2016_meddling_by_religiosity.csv")
    m = margins("2016")
    out = {}
    for tech in dict.fromkeys(r["technology"] for r in rows):
        t = {r["group"]: float(r["pct_meddling"]) for r in rows if r["technology"] == tech}
        out[tech] = {
            "high": t["High religious commitment"],
            "low": t["Low religious commitment"],
            "gap_high_minus_low": gap(t["High religious commitment"], t["Low religious commitment"],
                                      m["High religious commitment"], m["Low religious commitment"]),
        }
    gaps = [v["gap_high_minus_low"]["difference"] for v in out.values()]
    return {"items": out, "summary": {"gap_min": min(gaps), "gap_max": max(gaps), "n_items": len(gaps),
                                      "n_exceeds_moe": sum(v["gap_high_minus_low"]["exceeds_moe"] for v in out.values())}}


def provocation_test(exc: dict, reg: dict) -> dict:
    """Score the hypothesis that the political left is the locus of resistance.

    Prediction P1: Democrats and leaners report less excitement than Republicans
    and leaners about enhancement possibilities. Prediction P2: party is the main
    divider, so the party gap exceeds the religiosity gap. Prediction P3:
    Democrats more often fear under-regulation (a preference about governance).
    """
    s = exc["summary"]
    return {
        "P1_left_less_excited_items_consistent": s["n_rep_higher"],
        "P1_left_less_excited_items_contrary": s["n_dem_higher"],
        "P2_party_larger_than_religiosity_items": s["n_items"] - s["n_religiosity_exceeds_party"],
        "P3_dem_more_under_regulation_concern_items": reg["summary"]["n_dem_more_under_regulation_concern"],
        "P1_supported": s["n_rep_higher"] > s["n_dem_higher"],
        "P2_supported": s["n_religiosity_exceeds_party"] < s["n_items"] / 2,
        "P3_supported": reg["summary"]["n_dem_more_under_regulation_concern"] == reg["summary"]["n_items"],
    }
