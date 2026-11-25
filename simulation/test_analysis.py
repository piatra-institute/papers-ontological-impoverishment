import csv
import math
import unittest
from pathlib import Path

import analysis

DATA = Path(__file__).resolve().parent / "data"


class GapTests(unittest.TestCase):
    def test_gap_margin_and_rounding_floor(self):
        g = analysis.gap(52, 43, 2.2, 2.3)
        self.assertEqual(g["difference"], 9)
        self.assertAlmostEqual(g["moe95"], math.sqrt(2.2 ** 2 + 2.3 ** 2))
        self.assertEqual(g["rounding_floor"], 8)
        self.assertTrue(g["exceeds_moe"])

    def test_tables_are_complete(self):
        rows = list(csv.DictReader(open(DATA / "pew2022_excitement_by_group.csv")))
        self.assertEqual(len(rows), 36)
        for r in rows:
            self.assertTrue(0 <= int(r["pct_excited"]) <= 100)
        groups = {r["group"] for r in rows}
        self.assertIn("Dem/lean Dem", groups)
        self.assertIn("Low religious commitment", groups)

    def test_regulation_uses_half_sample_margins(self):
        reg = analysis.regulation_gaps()
        self.assertAlmostEqual(reg["summary"]["moe95"], math.sqrt(3.2 ** 2 + 3.3 ** 2))
        self.assertEqual(reg["summary"]["enhancement"]["n_items"], 3)
        self.assertEqual(reg["summary"]["non-bodily"]["n_items"], 3)

    def test_adjacent_steps_sum_to_tail_gap(self):
        exc = analysis.excitement_gaps()
        for item in exc["items"].values():
            self.assertEqual(item["step_high_to_medium"] + item["step_medium_to_low"], item["religiosity"]["difference"])

    def test_regulation_rows_sum_near_100(self):
        for r in csv.DictReader(open(DATA / "pew2022_regulation_by_party.csv")):
            total = int(r["pct_not_far_enough"]) + int(r["pct_too_far"])
            self.assertTrue(95 <= total <= 100, r)

    def test_us_adults_lie_between_party_groups(self):
        exc = analysis.excitement_gaps()
        for item in exc["items"].values():
            lo, hi = sorted((item["party"]["a"], item["party"]["b"]))
            self.assertTrue(lo <= item["us_adults"] <= hi)

    def test_provocation_scoring(self):
        exc = analysis.excitement_gaps()
        reg = analysis.regulation_gaps()
        t = analysis.provocation_test(exc, reg)
        self.assertEqual(t["P1_left_less_excited_items_consistent"] + t["P1_left_less_excited_items_contrary"]
                         + sum(1 for i in exc["items"].values() if i["party"]["difference"] == 0), 6)


if __name__ == "__main__":
    unittest.main()
