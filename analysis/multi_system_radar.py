#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from analysis.figures import fig2_radar_multi, radar_scenarios
from analysis.multi_scenario import load_sensitivity_by_scenario

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-root", type=Path, required=True)
    parser.add_argument("--systems", nargs="+", required=True)
    parser.add_argument("--out-png", type=Path, required=True)
    parser.add_argument("--out-csv", type=Path, required=True)
    args = parser.parse_args()

    scenarios_files = {s: f"report_{s}.json" for s in radar_scenarios()}
    
    score_table = {}
    for system in args.systems:
        system_dir = args.results_root / system
        if not system_dir.exists():
            print(f"Warning: {system_dir} not found, skipping {system}")
            continue
        
        try:
            scores = load_sensitivity_by_scenario(system_dir, scenarios_files)
            score_table[system] = scores
        except Exception as e:
            print(f"Failed to load {system}: {e}")

    if not score_table:
        print("No systems loaded")
        return 1

    fig2_radar_multi(score_table, args.out_png, args.out_csv)
    print(f"Generated {args.out_png}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
