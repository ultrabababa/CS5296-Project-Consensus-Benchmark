import unittest

from analysis.figures import (
    compute_ecdf_x_limit,
    compute_radar_rmax,
    radar_scenarios,
)


class FiguresConfigTests(unittest.TestCase):
    def test_radar_scenarios_excludes_byzantine_like(self):
        scenarios = radar_scenarios()
        self.assertNotIn("byzantine_like", scenarios)
        self.assertEqual(
            scenarios,
            [
                "leader_kill",
                "delay_120ms",
                "loss_8pct",
                "partition",
                "majority_crash",
                "majority_partition",
            ],
        )

    def test_compute_ecdf_x_limit_ignores_large_outlier(self):
        baseline = [10.0, 11.0, 12.0, 13.0, 1000.0]
        altered = [9.0, 10.0, 11.0, 12.0]
        x_limit = compute_ecdf_x_limit(baseline, altered)
        self.assertLess(x_limit, 300.0)
        self.assertGreater(x_limit, 10.0)

    def test_compute_radar_rmax_uses_compact_upper_bound(self):
        scores = {
            "etcd": {
                "leader_kill": 1.1,
                "delay_120ms": 1.4,
                "loss_8pct": 0.2,
                "partition": 0.6,
                "majority_crash": 1.7,
                "majority_partition": 0.7,
            }
        }
        rmax = compute_radar_rmax(scores, radar_scenarios())
        self.assertGreaterEqual(rmax, 1.7)
        self.assertLess(rmax, 2.5)


if __name__ == "__main__":
    unittest.main()
