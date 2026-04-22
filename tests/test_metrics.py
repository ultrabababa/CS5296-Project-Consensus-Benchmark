import unittest

from analysis.metrics import sensitivity_score, summarize_latencies


class MetricsTests(unittest.TestCase):
    def test_summarize_latencies_calculates_expected_fields(self):
        latencies = [10.0, 20.0, 30.0, 40.0, 50.0]
        summary = summarize_latencies(latencies, duration_sec=10.0, total_ops=5, failed_ops=1)

        self.assertEqual(summary["total_ops"], 5)
        self.assertEqual(summary["success_ops"], 4)
        self.assertEqual(summary["failed_ops"], 1)
        self.assertAlmostEqual(summary["throughput_ops_per_sec"], 0.4)
        self.assertAlmostEqual(summary["p50_ms"], 30.0)
        self.assertAlmostEqual(summary["p95_ms"], 48.0)
        self.assertAlmostEqual(summary["p99_ms"], 49.6)

    def test_sensitivity_score_is_zero_for_identical_distributions(self):
        baseline = [10.0, 20.0, 30.0, 40.0]
        fault = [10.0, 20.0, 30.0, 40.0]
        self.assertAlmostEqual(sensitivity_score(baseline, fault), 0.0)

    def test_sensitivity_score_increases_for_slower_fault_distribution(self):
        baseline = [10.0, 12.0, 14.0, 16.0, 18.0]
        fault = [30.0, 32.0, 34.0, 36.0, 38.0]
        score = sensitivity_score(baseline, fault)
        self.assertGreater(score, 0.0)


if __name__ == "__main__":
    unittest.main()
