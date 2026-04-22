import json
import tempfile
import unittest
from pathlib import Path

from analysis.ops_timeseries import aggregate_dir_series, load_ops_events, sliding_tps


class OpsTimeSeriesTests(unittest.TestCase):
    def test_load_ops_events_reads_trace_records(self):
        payload = {
            "ops_trace": [
                {"submit_time": 0.0, "end_time": 0.2, "success": True, "op": "write"},
                {"submit_time": 0.2, "end_time": 0.5, "success": False, "op": "read"},
            ]
        }
        got = load_ops_events(payload)
        self.assertEqual(len(got), 2)
        self.assertTrue(got[0]["success"])
        self.assertFalse(got[1]["success"])

    def test_sliding_tps_counts_success_only(self):
        events = [
            {"submit_time": 0.0, "end_time": 1.0, "success": True},
            {"submit_time": 0.2, "end_time": 2.0, "success": True},
            {"submit_time": 0.4, "end_time": 3.0, "success": False},
        ]
        times, tps = sliding_tps(events, window_size=2.0, step_size=1.0, time_key="end_time", success_only=True)
        self.assertEqual(times, [2.0, 3.0])
        self.assertEqual(tps, [1.0, 0.5])

    def test_aggregate_dir_series_calculates_mean_and_std(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            run1 = {
                "ops_trace": [
                    {"submit_time": 0.0, "end_time": 1.0, "success": True},
                    {"submit_time": 0.1, "end_time": 2.0, "success": True},
                    {"submit_time": 0.2, "end_time": 3.0, "success": True},
                ]
            }
            run2 = {
                "ops_trace": [
                    {"submit_time": 0.0, "end_time": 1.0, "success": True},
                    {"submit_time": 0.1, "end_time": 1.5, "success": True},
                    {"submit_time": 0.2, "end_time": 2.0, "success": True},
                    {"submit_time": 0.3, "end_time": 3.0, "success": True},
                ]
            }
            (d / "run_1.json").write_text(json.dumps(run1), encoding="utf-8")
            (d / "run_2.json").write_text(json.dumps(run2), encoding="utf-8")

            result = aggregate_dir_series(
                d,
                window_size=2.0,
                step_size=1.0,
                time_key="end_time",
                success_only=True,
            )

            self.assertEqual(result["times"], [2.0, 3.0])
            self.assertAlmostEqual(result["mean_tps"][0], 1.25)
            self.assertAlmostEqual(result["mean_tps"][1], 1.25)
            self.assertGreater(result["std_tps"][0], 0.0)


if __name__ == "__main__":
    unittest.main()
