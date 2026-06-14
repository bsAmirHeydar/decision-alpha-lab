from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from apps.api.core.config import settings


def list_cached_datasets() -> List[Dict[str, object]]:
    datasets: List[Dict[str, object]] = []
    root: Path = settings.cache_data_path
    if not root.exists():
        return datasets

    for symbol_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        symbol = symbol_dir.name
        for tf_dir in sorted(p for p in symbol_dir.iterdir() if p.is_dir()):
            timeframe = tf_dir.name
            parquet = tf_dir / f"{symbol}_{timeframe}.parquet"
            if parquet.exists():
                datasets.append(
                    {
                        "dataset_id": f"{symbol}:{timeframe}:cache:latest",
                        "source": "cache",
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "path": str(parquet.relative_to(settings.root_path)),
                    }
                )
    return datasets
