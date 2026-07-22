from __future__ import annotations

import json
from pathlib import Path

import pytest

from strategy_factory_rthp_train_activation_v1.config import load_activation_config
from strategy_factory_rthp_train_activation_v1.ticks import load_tick_jsonl


def test_smoke_config_is_valid(smoke_config_path: Path):
    config = load_activation_config(smoke_config_path)
    assert config.data_source.timezone == "America/New_York"
    assert config.data_source.price_basis == "BID"
    assert config.data_source.primary_symbol != config.data_source.secondary_symbol
    assert len(config.config_digest) == 64


def test_same_symbol_is_rejected(smoke_config_path: Path):
    raw = json.loads(smoke_config_path.read_text(encoding="utf-8"))
    raw["data_source"]["secondary_symbol"] = raw["data_source"]["primary_symbol"]
    smoke_config_path.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(ValueError, match="must differ"):
        load_activation_config(smoke_config_path)


def test_tick_known_time_before_event_is_rejected(tmp_path: Path):
    path = tmp_path / "bad.jsonl"
    path.write_text(json.dumps({"symbol":"X","event_time_ms":2,"known_time_ms":1,"bid":1.0,"tick_size":0.01}) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="known_time precedes"):
        load_tick_jsonl(path, "X", None, None)


def test_split_fractions_must_sum_to_one(smoke_config_path: Path):
    raw = json.loads(smoke_config_path.read_text(encoding="utf-8"))
    raw["split_policy"]["final_test_fraction"] = 0.50
    smoke_config_path.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(ValueError, match="sum to one"):
        load_activation_config(smoke_config_path)
