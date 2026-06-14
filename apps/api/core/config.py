from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ApiSettings:
    """Runtime paths for the Quant Lab API.

    The API is intentionally path-based so it can run from the repository root
    without importing UI concerns into the research lab.
    """

    app_name: str = "Decision Alpha Lab API"
    contract_version: str = "visualization.v1"
    root_path: Path = Path(__file__).resolve().parents[3]
    cache_data_path: Path = root_path / "lab" / "cache_data"
    cache_nodes_path: Path = root_path / "lab" / "cache_nodes"
    cache_metrics_path: Path = root_path / "lab" / "cache_metrics"


settings = ApiSettings()
