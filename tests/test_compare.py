import json
import tempfile
import unittest
from pathlib import Path

from analysis.compare_runs import aggregate_scenario


class CompareRunsTests(unittest.TestCase):
    def test_aggregate_scenario_combines_runs_and_calculates_means(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            run1 = {
                "summary": {
                    "throughput_ops_per_sec": 100.0,
                    "p99_ms": 30.0,
                    "failure_rate": 0.01,
                },
                "latencies_ms": [10.0, 20.0, 30.0],
            }
            run2 = {
                "summary": {
                    "throughput_ops_per_sec": 80.0,
                    "p99_ms": 40.0,
                    "failure_rate": 0.02,
                },
                "latencies_ms": [11.0, 21.0, 31.0],
            }
            (d / "run_1.json").write_text(json.dumps(run1), encoding="utf-8")
            (d / "run_2.json").write_text(json.dumps(run2), encoding="utf-8")

            result = aggregate_scenario(d)
            self.assertAlmostEqual(result["mean_throughput_ops_per_sec"], 90.0)
            self.assertAlmostEqual(result["mean_p99_ms"], 35.0)
            self.assertAlmostEqual(result["mean_failure_rate"], 0.015)
            self.assertEqual(len(result["latencies_ms"]), 6)


if __name__ == "__main__":
    unittest.main()
