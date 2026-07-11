from __future__ import annotations

from pathlib import Path

from sf_phase00.duplicates import detect_duplicate_capabilities


def test_duplicate_persistence_and_normalization_are_detected(tmp_path: Path) -> None:
    paths = [
        "lab/core/CP0000_market_data/cache/ParquetStore.py",
        "lab/core/CP0000_market_data/connectors/MT5Connector.py",
        "lab/core/CP0000_market_data/services/MarketDataEngine.py",
        "lab/core/CP0001_structural_nodes/detectors/L_Rule.py",
        "lab/core/CP0001_structural_nodes/metrics/M0001_relative_territory_volatility.py",
    ]
    for relative in paths:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# fixture\n", encoding="utf-8")
    capabilities = {item.capability for item in detect_duplicate_capabilities(tmp_path)}
    assert "parquet_artifact_persistence" in capabilities
    assert "market_bar_normalization" in capabilities
