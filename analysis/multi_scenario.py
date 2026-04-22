from __future__ import annotations

import json
from pathlib import Path


def load_sensitivity_by_scenario(results_root: Path, scenarios: dict[str, str]) -> dict[str, float]:
    out: dict[str, float] = {}
    for scenario, rel_path in scenarios.items():
        p = results_root / rel_path
        if not p.exists():
            out[scenario] = float("inf")
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        out[scenario] = float(data.get("sensitivity_score", 0.0))
    return out
