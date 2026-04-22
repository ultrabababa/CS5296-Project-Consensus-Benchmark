import math
import unittest

from analysis.stabl_metric import area_under_ecdf, stabl_sensitivity_score


class StablMetricTests(unittest.TestCase):
    def test_stabl_sensitivity_zero_for_identical_distributions(self):
        sample = [10.0, 20.0, 30.0, 40.0]
        self.assertAlmostEqual(stabl_sensitivity_score(sample, sample), 0.0)

    def test_stabl_sensitivity_matches_absolute_area_difference(self):
        baseline = [1.0, 2.0, 3.0]
        altered = [2.0, 3.0, 4.0]
        lower = min(min(baseline), min(altered), 0.0)
        upper = max(max(baseline), max(altered))
        expected = abs(
            area_under_ecdf(baseline, lower_bound=lower, upper_bound=upper)
            - area_under_ecdf(altered, lower_bound=lower, upper_bound=upper)
        )
        self.assertAlmostEqual(stabl_sensitivity_score(baseline, altered), expected)

    def test_stabl_sensitivity_infinite_when_altered_has_no_successful_latency(self):
        baseline = [10.0, 12.0, 14.0]
        altered: list[float] = []
        self.assertTrue(math.isinf(stabl_sensitivity_score(baseline, altered)))


if __name__ == "__main__":
    unittest.main()
