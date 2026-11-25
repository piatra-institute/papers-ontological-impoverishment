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


def coverage() -> dict:
    """Population coverage of the compared groups (Pew 2022 margins table, p. 124)."""
    rows = {r["group"]: r for r in read("pew_margins_of_error.csv") if r["survey"] == "2022"}
    total = float(rows["Total sample"]["unweighted_n"])
    return {
        "party_weighted_pct_dem": float(rows[PARTY[0]]["weighted_pct"]),
        "party_weighted_pct_rep": float(rows[PARTY[1]]["weighted_pct"]),
        "party_weighted_pct_both": float(rows[PARTY[0]]["weighted_pct"]) + float(rows[PARTY[1]]["weighted_pct"]),
        "religiosity_unweighted_share_high": 100 * float(rows["High religious commitment"]["unweighted_n"]) / total,
        "religiosity_unweighted_share_medium": 100 * float(rows["Medium religious commitment"]["unweighted_n"]) / total,
        "religiosity_unweighted_share_low": 100 * float(rows["Low religious commitment"]["unweighted_n"]) / total,
        "religiosity_unweighted_share_tails": 100 * (float(rows["High religious commitment"]["unweighted_n"]) + float(rows["Low religious commitment"]["unweighted_n"])) / total,
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
        items[code]["step_high_to_medium"] = t["Medium religious commitment"] - t["High religious commitment"]
        items[code]["step_medium_to_low"] = t["Low religious commitment"] - t["Medium religious commitment"]
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
        "religiosity_step_min": min(min(items[c]["step_high_to_medium"], items[c]["step_medium_to_low"]) for c in ITEM_ORDER),
        "religiosity_step_max": max(max(items[c]["step_high_to_medium"], items[c]["step_medium_to_low"]) for c in ITEM_ORDER),
        "coverage": coverage(),
        "religiosity_moe95": items[ITEM_ORDER[0]]["religiosity"]["moe95"],
    }
    return {"items": items, "summary": summary}


def regulation_gaps() -> dict:
    """Party gaps in fearing under-regulation. All six items were asked of a half sample
    (Form 2 for the enhancement modules, Form 1 for the non-bodily AI modules), so the
    half-sample party margins from p. 124 apply."""
    rows = read("pew2022_regulation_by_party.csv")
    m = margins("2022")
    moe_dem, moe_rep = m[PARTY[0] + " (half sample)"], m[PARTY[1] + " (half sample)"]
    out = {}
    for tech in dict.fromkeys(r["technology"] for r in rows):
        t = {r["group"]: r for r in rows if r["technology"] == tech}
        dem, rep = t[PARTY[0]], t[PARTY[1]]
        out[tech] = {
            "domain": dem["domain"],
            "us_not_far_enough": float(t["U.S. adults"]["pct_not_far_enough"]),
            "us_too_far": float(t["U.S. adults"]["pct_too_far"]),
            "dem_not_far_enough": float(dem["pct_not_far_enough"]),
            "rep_not_far_enough": float(rep["pct_not_far_enough"]),
            "dem_too_far": float(dem["pct_too_far"]),
            "rep_too_far": float(rep["pct_too_far"]),
            "not_far_enough_gap": gap(float(dem["pct_not_far_enough"]), float(rep["pct_not_far_enough"]), moe_dem, moe_rep),
        }
    summary = {}
    for domain in ("enhancement", "non-bodily"):
        gaps = [v["not_far_enough_gap"]["difference"] for v in out.values() if v["domain"] == domain]
        summary[domain] = {
            "n_items": len(gaps),
            "n_dem_more_under_regulation_concern": sum(g > 0 for g in gaps),
            "gap_min": min(gaps),
            "gap_max": max(gaps),
        }
    summary["moe95"] = math.sqrt(moe_dem ** 2 + moe_rep ** 2)
    return {"items": out, "summary": summary}


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

    Scope: unadjusted U.S. Dem/lean Dem vs Rep/lean Rep differences. Prediction
    P1: Democrats and leaners report less excitement than Republicans and leaners
    about six specific techniques. Prediction P3:
    Democrats more often fear under-regulation (a preference about governance).
    """
    s = exc["summary"]
    return {
        "P1_left_less_excited_items_consistent": s["n_rep_higher"],
        "P1_left_less_excited_items_contrary": s["n_dem_higher"],
        "P3_dem_more_under_regulation_concern_items": reg["summary"]["enhancement"]["n_dem_more_under_regulation_concern"],
        "P1_supported": s["n_rep_higher"] > s["n_dem_higher"],
        "P3_supported": reg["summary"]["enhancement"]["n_dem_more_under_regulation_concern"] == reg["summary"]["enhancement"]["n_items"],
    }
