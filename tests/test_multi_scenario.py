import tempfile
import unittest
from pathlib import Path

from analysis.multi_scenario import load_sensitivity_by_scenario


class MultiScenarioTests(unittest.TestCase):
    def test_load_sensitivity_by_scenario_reads_report_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "leader_kill").mkdir(parents=True)
            (root / "partition").mkdir(parents=True)
            (root / "leader_kill" / "report.json").write_text('{"sensitivity_score": 10.5}', encoding="utf-8")
            (root / "partition" / "report.json").write_text('{"sensitivity_score": 99.0}', encoding="utf-8")

            got = load_sensitivity_by_scenario(
                root,
                scenarios={
                    "leader_kill": "leader_kill/report.json",
                    "partition": "partition/report.json",
                },
            )

            self.assertEqual(got["leader_kill"], 10.5)
            self.assertEqual(got["partition"], 99.0)


if __name__ == "__main__":
    unittest.main()
