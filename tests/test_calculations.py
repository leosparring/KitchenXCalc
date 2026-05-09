import math
import sys
import unittest
from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[1] / "kitchen_appliances_app"
sys.path.insert(0, str(APP_DIR))

from calculations import (  # noqa: E402
    calculate_slot,
    compute_sections,
    compute_sections_drip,
    compute_sections_perimeter,
    compute_sections_plenum,
    compute_sections_range_top_shelf,
    drip_needs_split,
    optimal_circle_grid,
    summarize_slot,
)
from data import APPLIANCES  # noqa: E402


class CalculationTests(unittest.TestCase):
    def test_rectangular_section_split_respects_area_and_side_limits(self):
        rows, cols, cell_w, cell_d, total = compute_sections(800, 500, 0.137, 380)

        self.assertEqual((rows, cols, total), (2, 3, 6))
        self.assertLessEqual((cell_w / 1000) * (cell_d / 1000), 0.137)
        self.assertLessEqual(max(cell_w, cell_d), 380)

    def test_circular_area_split_uses_minimum_covering_grid(self):
        area_m2 = math.pi * (700 / 2000) ** 2
        required = math.ceil(area_m2 / APPLIANCES["Wok"]["max_area"])

        self.assertEqual(required, 2)
        self.assertEqual(optimal_circle_grid(required), (1, 2))

    def test_perimeter_based_duct_split(self):
        rows, cols, cell_w, cell_d, total = compute_sections_perimeter(700, 700, 1270)

        self.assertEqual((rows, cols, total), (2, 3, 6))
        self.assertLess(2 * (cell_w + cell_d), 1270)

    def test_plenum_v_style_keeps_minimum_two_width_sections(self):
        rows, cols, cell_w, cell_d, total = compute_sections_plenum(1200, 3000, 600, 3000, 2)

        self.assertEqual((rows, cols, total), (1, 2, 2))
        self.assertEqual((cell_w, cell_d), (600, 3000))

    def test_fryer_with_drip_board_split(self):
        self.assertTrue(drip_needs_split(600, 600, 160, 0.137, 380, 0.194, 540))

        rows, cols, cell_w, cell_d, total, bottom_depth = compute_sections_drip(
            600, 600, 160, 0.137, 380, 0.194, 540
        )
        self.assertEqual((rows, cols, total), (2, 2, 4))
        self.assertEqual((cell_w, cell_d, bottom_depth), (300, 300, 300))

    def test_range_top_shelf_feasible_and_infeasible_cases(self):
        feasible = compute_sections_range_top_shelf(640, 640, 270, 800, 100)
        infeasible = compute_sections_range_top_shelf(2000, 2000, 270, 100, 1000)

        self.assertIsNotNone(feasible)
        self.assertEqual(feasible[4], 1)
        self.assertIsNone(infeasible)

    def test_summary_uses_shared_slot_calculation(self):
        vals = {"width": 900, "depth": 900, "qty": 2}

        calc = calculate_slot("Griddle", vals.copy(), APPLIANCES)
        summary = summarize_slot("Griddle", vals.copy(), APPLIANCES)

        self.assertEqual(calc["n_sections"], 4)
        self.assertEqual(summary["nozzle_str"], "4x 1–60")
        self.assertEqual(summary["total_flow"], 8)
        self.assertEqual(summary["nozzle_count"], 8)


if __name__ == "__main__":
    unittest.main()
