import json
import tempfile
import unittest
from pathlib import Path

from analysis.ops_plot_data import build_ops_series


class OpsPlotDataTests(unittest.TestCase):
    def test_build_ops_series_returns_baseline_and_fault(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            baseline = root / "etcd" / "baseline"
            fault = root / "etcd" / "fault" / "leader_kill"
            baseline.mkdir(parents=True)
            fault.mkdir(parents=True)

            baseline_payload = {
                "ops_trace": [
                    {"submit_time": 0.0, "end_time": 1.0, "success": True, "op": "write"},
                    {"submit_time": 0.1, "end_time": 2.0, "success": True, "op": "read"},
                    {"submit_time": 0.2, "end_time": 3.0, "success": True, "op": "write"},
                ]
            }
            fault_payload = {
                "ops_trace": [
                    {"submit_time": 0.0, "end_time": 1.0, "success": True, "op": "write"},
                    {"submit_time": 0.1, "end_time": 2.0, "success": False, "op": "read"},
                    {"submit_time": 0.2, "end_time": 3.0, "success": True, "op": "write"},
                ]
            }
            (baseline / "run_1.json").write_text(json.dumps(baseline_payload), encoding="utf-8")
            (fault / "run_1.json").write_text(json.dumps(fault_payload), encoding="utf-8")

            out = build_ops_series(
                results_root=root,
                system="etcd",
                scenarios=["leader_kill"],
                window_size=2.0,
                step_size=1.0,
            )

            self.assertIn("baseline", out)
            self.assertIn("leader_kill", out)
            self.assertEqual(out["baseline"]["times"], [2.0, 3.0])
            self.assertEqual(out["leader_kill"]["times"], [2.0, 3.0])
            self.assertGreater(out["baseline"]["mean_tps"][0], out["leader_kill"]["mean_tps"][0])

    def test_missing_scenario_returns_empty_series(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "etcd" / "baseline").mkdir(parents=True)
            (root / "etcd" / "baseline" / "run_1.json").write_text(
                json.dumps({"ops_trace": [{"submit_time": 0.0, "end_time": 1.0, "success": True, "op": "write"}]}),
                encoding="utf-8",
            )

            out = build_ops_series(
                results_root=root,
                system="etcd",
                scenarios=["partition"],
                window_size=1.0,
                step_size=1.0,
            )
            self.assertEqual(out["partition"]["times"], [])
            self.assertEqual(out["partition"]["mean_tps"], [])
            self.assertEqual(out["partition"]["std_tps"], [])


if __name__ == "__main__":
    unittest.main()
