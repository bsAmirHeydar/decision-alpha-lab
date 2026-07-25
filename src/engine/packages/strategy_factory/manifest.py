"""Versioned Strategy Factory manifest loading and validation."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Sequence
import json

from .contracts import ContractError, stable_hash


REQUIRED_TOP_LEVEL = {
    "strategy",
    "anatomy_adapter",
    "features",
    "candidate_universe",
    "labels",
    "validation",
    "models",
    "execution",
}


@dataclass(frozen=True)
class StrategyManifest:
    path: Path
    raw: Mapping[str, Any]
    manifest_hash: str

    @property
    def strategy_id(self) -> str:
        return str(self.raw["strategy"]["id"])

    @property
    def version(self) -> str:
        return str(self.raw["strategy"]["version"])

    @property
    def status(self) -> str:
        return str(self.raw["strategy"].get("status", "draft"))

    def section(self, name: str) -> Mapping[str, Any]:
        value = self.raw.get(name)
        if not isinstance(value, Mapping):
            raise ContractError(f"manifest section {name!r} must be an object")
        return value

    def list_section(self, section: str, key: str) -> Sequence[Any]:
        value = self.section(section).get(key, [])
        if not isinstance(value, list):
            raise ContractError(f"manifest {section}.{key} must be a list")
        return value


def _require(mapping: Mapping[str, Any], keys: Iterable[str], context: str) -> None:
    missing = [key for key in keys if key not in mapping]
    if missing:
        raise ContractError(f"{context} missing required keys: {missing}")


def validate_manifest_dict(raw: Mapping[str, Any]) -> None:
    missing_top = REQUIRED_TOP_LEVEL - set(raw)
    if missing_top:
        raise ContractError(f"manifest missing top-level sections: {sorted(missing_top)}")

    strategy = raw["strategy"]
    if not isinstance(strategy, Mapping):
        raise ContractError("strategy section must be an object")
    _require(strategy, ("id", "version", "owner", "thesis", "null_hypothesis"), "strategy")
    if strategy.get("status") not in {
        None,
        "draft",
        "anatomy_defined",
        "dataset_ready",
        "baseline_tested",
        "oos_validated",
        "paper_ready",
        "paper_running",
        "micro_live",
        "live_approved",
        "scaled",
        "retired",
    }:
        raise ContractError("strategy.status is not a recognized lifecycle state")

    adapter = raw["anatomy_adapter"]
    if not isinstance(adapter, Mapping):
        raise ContractError("anatomy_adapter must be an object")
    _require(adapter, ("type", "version", "known_time_field", "event_id_fields"), "anatomy_adapter")
    if not isinstance(adapter["event_id_fields"], list) or not adapter["event_id_fields"]:
        raise ContractError("anatomy_adapter.event_id_fields must be a non-empty list")

    features = raw["features"]
    if not isinstance(features, Mapping):
        raise ContractError("features must be an object")
    _require(features, ("schema_version", "shared", "strategy_specific"), "features")
    if not isinstance(features["shared"], list) or not isinstance(features["strategy_specific"], list):
        raise ContractError("feature lists must be arrays")

    universe = raw["candidate_universe"]
    if not isinstance(universe, Mapping):
        raise ContractError("candidate_universe must be an object")
    _require(universe, ("entries", "stops", "exits", "max_candidates_per_event"), "candidate_universe")
    for key in ("entries", "stops", "exits"):
        if not isinstance(universe[key], list) or not universe[key]:
            raise ContractError(f"candidate_universe.{key} must be a non-empty list")
    max_candidates = int(universe["max_candidates_per_event"])
    theoretical = len(universe["entries"]) * len(universe["stops"]) * len(universe["exits"])
    if max_candidates <= 0:
        raise ContractError("max_candidates_per_event must be positive")
    if theoretical > max_candidates and not universe.get("explicit_allow_pruning", False):
        raise ContractError(
            "candidate Cartesian product exceeds max_candidates_per_event; "
            "define compatibility rules or set explicit_allow_pruning"
        )

    labels = raw["labels"]
    if not isinstance(labels, Mapping):
        raise ContractError("labels must be an object")
    _require(labels, ("version", "primary", "label_horizon"), "labels")

    validation = raw["validation"]
    if not isinstance(validation, Mapping):
        raise ContractError("validation must be an object")
    _require(
        validation,
        ("splitter", "cluster_key", "purge_by_label_end", "embargo_seconds", "anti_overfit_suite"),
        "validation",
    )
    if validation["splitter"] not in {"purged_walk_forward", "anchored_walk_forward", "combinatorial_purged_cv"}:
        raise ContractError("validation.splitter is unsupported")
    if not validation["purge_by_label_end"]:
        raise ContractError("purge_by_label_end must be true for official research")

    models = raw["models"]
    if not isinstance(models, Mapping):
        raise ContractError("models must be an object")
    _require(models, ("baselines", "challengers", "selection_metric"), "models")
    if not models["baselines"]:
        raise ContractError("at least one simple baseline is mandatory")

    execution = raw["execution"]
    if not isinstance(execution, Mapping):
        raise ContractError("execution must be an object")
    _require(execution, ("paper_enabled", "live_enabled", "risk_policy", "broker_adapter"), "execution")
    if execution.get("live_enabled") and strategy.get("status") not in {"micro_live", "live_approved", "scaled"}:
        raise ContractError("live_enabled requires a promoted lifecycle state")


def load_manifest(path: str | Path) -> StrategyManifest:
    resolved = Path(path).expanduser().resolve()
    with resolved.open("r", encoding="utf-8") as handle:
        raw: Dict[str, Any] = json.load(handle)
    validate_manifest_dict(raw)
    return StrategyManifest(path=resolved, raw=raw, manifest_hash=stable_hash(raw, prefix="manifest_"))
