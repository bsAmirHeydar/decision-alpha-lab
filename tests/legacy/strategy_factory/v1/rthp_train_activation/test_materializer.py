from __future__ import annotations

import json
from pathlib import Path

from strategy_factory_rthp_train_activation_v1.config import load_activation_config
from strategy_factory_rthp_train_activation_v1.materializer import RTHPHistoricalMaterializer


def test_materializer_builds_all_four_ledgers(smoke_config_path: Path, tmp_path: Path):
    config = load_activation_config(smoke_config_path)
    result = RTHPHistoricalMaterializer(config).materialize(tmp_path / "materialized")
    assert result.occurrence_count > 100
    assert result.family_counts == {"M15_CYCLE_GROUP": result.occurrence_count}
    for path in (result.occurrence_ledger, result.reference_state_ledger, result.cycle_instance_ledger, result.role_price_path_ledger, result.data_binding):
        assert path.is_file() and path.stat().st_size > 0
    binding = json.loads(result.data_binding.read_text(encoding="utf-8"))
    assert binding["binding_status"] == "RESOLVED"
    assert len(binding["sources"]) == 4
    assert all(x["content_hash"].startswith("sha256:") for x in binding["sources"])


def test_materialized_occurrences_are_context_only(smoke_config_path: Path, tmp_path: Path):
    config = load_activation_config(smoke_config_path)
    result = RTHPHistoricalMaterializer(config).materialize(tmp_path / "materialized")
    first = json.loads(result.occurrence_ledger.read_text(encoding="utf-8").splitlines()[0])
    assert first["confirmed_context_event"] is True
    assert first["family"] == "M15_CYCLE_GROUP"
    forbidden = {"entry", "stop_loss", "take_profit", "position_size", "order_id"}
    assert not forbidden.intersection(first)
