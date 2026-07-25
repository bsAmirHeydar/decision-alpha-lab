"""Reproducible run artifact writing and content hashing."""
from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Optional
import hashlib
import json
import os
import subprocess

import pandas as pd


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json(value: Any) -> str:
    if is_dataclass(value):
        value = asdict(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def object_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def current_git_commit(repo_root: str | Path) -> Optional[str]:
    try:
        output = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=Path(repo_root), stderr=subprocess.DEVNULL, text=True
        )
        return output.strip()
    except Exception:
        return None


def write_json(path: str | Path, payload: Any) -> Path:
    resolved = Path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    if is_dataclass(payload):
        payload = asdict(payload)
    with resolved.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True, default=str)
        handle.write("\n")
    return resolved


def write_frame(path: str | Path, frame: pd.DataFrame) -> Path:
    resolved = Path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    suffix = resolved.suffix.lower()
    if suffix == ".parquet":
        try:
            frame.to_parquet(resolved, index=False)
            return resolved
        except ImportError:
            # Development fallback. Official production runs should install
            # pyarrow and treat format fallback as a warning in the run QA.
            fallback = resolved.with_suffix(".csv")
            frame.to_csv(fallback, index=False)
            return fallback
    if suffix == ".csv":
        frame.to_csv(resolved, index=False)
        return resolved
    raise ValueError("frame artifact must be .parquet or .csv")


def build_run_manifest(
    *,
    run_id: str,
    repo_root: str | Path,
    strategy_id: str,
    strategy_version: str,
    manifest_hash: str,
    dataset_hash: Optional[str] = None,
    feature_set_hash: Optional[str] = None,
    candidate_set_hash: Optional[str] = None,
    label_set_hash: Optional[str] = None,
    fold_plan_hash: Optional[str] = None,
    model_hash: Optional[str] = None,
    random_seed: int = 7,
    status: str = "created",
) -> Mapping[str, Any]:
    return {
        "run_id": run_id,
        "created_time_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": current_git_commit(repo_root),
        "strategy_id": strategy_id,
        "strategy_version": strategy_version,
        "manifest_hash": manifest_hash,
        "dataset_hash": dataset_hash,
        "feature_set_hash": feature_set_hash,
        "candidate_set_hash": candidate_set_hash,
        "label_set_hash": label_set_hash,
        "fold_plan_hash": fold_plan_hash,
        "model_hash": model_hash,
        "random_seed": random_seed,
        "status": status,
        "environment": {
            "python": os.sys.version,
            "platform": os.sys.platform,
        },
    }
