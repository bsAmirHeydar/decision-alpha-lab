from __future__ import annotations

import json
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


@pytest.fixture(scope="session")
def activation_root(repo_root: Path) -> Path:
    return repo_root / "lab" / "11_strategy_factory" / "generated_contexts" / "rthp_cross_symbol_cycle_divergence" / "train_activation" / "v1"


@pytest.fixture()
def smoke_config_path(tmp_path: Path, activation_root: Path) -> Path:
    raw = json.loads((activation_root / "configs" / "train_activation.smoke.v1.json").read_text(encoding="utf-8"))
    raw["output_root"] = (tmp_path / "run").as_posix()
    raw["data_source"]["primary_tick_jsonl"] = (activation_root / "fixtures" / "rthp_smoke_a.jsonl").as_posix()
    raw["data_source"]["secondary_tick_jsonl"] = (activation_root / "fixtures" / "rthp_smoke_b.jsonl").as_posix()
    path = tmp_path / "config.json"
    path.write_text(json.dumps(raw, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return path
