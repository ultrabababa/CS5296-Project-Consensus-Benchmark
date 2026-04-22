import tempfile
import unittest
from pathlib import Path

from analysis.figure_data import ecdf_points, load_latencies_from_runs, radar_rows


class FigureDataTests(unittest.TestCase):
    def test_ecdf_points_are_sorted_and_bounded(self):
        xs, ys = ecdf_points([30.0, 10.0, 20.0])
        self.assertEqual(xs, [10.0, 20.0, 30.0])
        self.assertEqual(ys, [1 / 3, 2 / 3, 1.0])

    def test_load_latencies_from_runs_collects_all(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "run_1.json").write_text('{"latencies_ms":[1,2,3],"summary":{}}', encoding="utf-8")
            (d / "run_2.json").write_text('{"latencies_ms":[4,5],"summary":{}}', encoding="utf-8")
            values = load_latencies_from_runs(d)
            self.assertEqual(values, [1.0, 2.0, 3.0, 4.0, 5.0])

    def test_radar_rows_match_requested_order(self):
        scores = {
            "etcd": {
                "leader_kill": 10.0,
                "partition": 20.0,
            }
        }
        rows = radar_rows(scores, systems=["etcd"], scenarios=["leader_kill", "partition"])
        self.assertEqual(rows[0]["system"], "etcd")
        self.assertEqual(rows[0]["leader_kill"], 10.0)
        self.assertEqual(rows[0]["partition"], 20.0)


if __name__ == "__main__":
    unittest.main()
