from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .canonical import sha256_material


@dataclass(frozen=True, slots=True)
class DataSourceConfig:
    mode: str
    provider: str
    primary_symbol: str
    secondary_symbol: str
    primary_tick_jsonl: Path | None
    secondary_tick_jsonl: Path | None
    primary_m1_bar_jsonl: Path | None
    secondary_m1_bar_jsonl: Path | None
    timezone: str
    price_basis: str
    tick_size_source: str
    contract_roll_policy: str
    entitlement_id: str
    producer_version: str
    availability_time_policy: str
    source_revision: str
    start_time_ms: int | None
    end_time_ms: int | None
    max_confirmation_freshness_ms: int

    @property
    def source_paths(self) -> tuple[Path, Path]:
        if self.mode == "PAIRED_TICK_JSONL":
            if self.primary_tick_jsonl is None or self.secondary_tick_jsonl is None:
                raise ValueError("tick source paths are unresolved")
            return self.primary_tick_jsonl, self.secondary_tick_jsonl
        if self.mode == "PAIRED_M1_BAR_JSONL":
            if self.primary_m1_bar_jsonl is None or self.secondary_m1_bar_jsonl is None:
                raise ValueError("M1 source paths are unresolved")
            return self.primary_m1_bar_jsonl, self.secondary_m1_bar_jsonl
        raise ValueError(f"unsupported source mode: {self.mode}")


@dataclass(frozen=True, slots=True)
class SplitPolicy:
    minimum_mature_rows: int
    oof_train_fraction: float
    oof_calibration_fraction: float
    oof_threshold_fraction: float
    oof_holdout_fraction: float
    final_train_fraction: float
    final_calibration_fraction: float
    final_threshold_fraction: float
    final_test_fraction: float
    purge_ms: int
    embargo_ms: int


@dataclass(frozen=True, slots=True)
class ResourcePolicy:
    seed: int
    max_rows: int
    max_features: int
    max_memory_mb: int
    max_wall_seconds: float
    max_workers: int


@dataclass(frozen=True, slots=True)
class ActivationConfig:
    schema_version: str
    run_id: str
    output_root: Path
    data_source: DataSourceConfig
    split_policy: SplitPolicy
    resource_policy: ResourcePolicy
    selected_task_ids: tuple[str, ...]
    family_filter: tuple[str, ...]
    train_all_mature_tasks: bool
    retain_materialized_views: bool
    fail_on_task_insufficiency: bool

    @property
    def config_digest(self) -> str:
        return sha256_material(self)


def _path(value: Any, field: str, base: Path) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty path string")
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def _optional_path(source: dict[str, Any], field: str, base: Path) -> Path | None:
    value = source.get(field)
    return None if value in (None, "") else _path(value, field, base)


def _fraction(value: Any, field: str) -> float:
    out = float(value)
    if not 0.0 <= out <= 1.0:
        raise ValueError(f"{field} must be between zero and one")
    return out


def load_activation_config(path: str | Path) -> ActivationConfig:
    config_path = Path(path).resolve()
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    if raw.get("schema_version") != "1.0.0":
        raise ValueError("unsupported activation config schema_version")
    source = raw["data_source"]
    mode = source.get("mode")
    if mode not in {"PAIRED_TICK_JSONL", "PAIRED_M1_BAR_JSONL"}:
        raise ValueError("source mode must be PAIRED_TICK_JSONL or PAIRED_M1_BAR_JSONL")
    if source.get("timezone") != "America/New_York":
        raise ValueError("RTHP source timezone must be America/New_York")
    if source.get("price_basis") != "BID":
        raise ValueError("RTHP v1 price basis must be BID")
    base = config_path.parent
    data_source = DataSourceConfig(
        mode=mode,
        provider=str(source["provider"]),
        primary_symbol=str(source["primary_symbol"]),
        secondary_symbol=str(source["secondary_symbol"]),
        primary_tick_jsonl=_optional_path(source, "primary_tick_jsonl", base),
        secondary_tick_jsonl=_optional_path(source, "secondary_tick_jsonl", base),
        primary_m1_bar_jsonl=_optional_path(source, "primary_m1_bar_jsonl", base),
        secondary_m1_bar_jsonl=_optional_path(source, "secondary_m1_bar_jsonl", base),
        timezone=source["timezone"],
        price_basis=source["price_basis"],
        tick_size_source=str(source["tick_size_source"]),
        contract_roll_policy=str(source["contract_roll_policy"]),
        entitlement_id=str(source["entitlement_id"]),
        producer_version=str(source["producer_version"]),
        availability_time_policy=str(source["availability_time_policy"]),
        source_revision=str(source["source_revision"]),
        start_time_ms=None if source.get("start_time_ms") is None else int(source["start_time_ms"]),
        end_time_ms=None if source.get("end_time_ms") is None else int(source["end_time_ms"]),
        max_confirmation_freshness_ms=int(source.get("max_confirmation_freshness_ms", 0 if mode == "PAIRED_M1_BAR_JSONL" else 900_000)),
    )
    if data_source.primary_symbol == data_source.secondary_symbol:
        raise ValueError("primary and secondary symbols must differ")
    if mode == "PAIRED_TICK_JSONL" and (data_source.primary_tick_jsonl is None or data_source.secondary_tick_jsonl is None):
        raise ValueError("PAIRED_TICK_JSONL requires primary_tick_jsonl and secondary_tick_jsonl")
    if mode == "PAIRED_M1_BAR_JSONL" and (data_source.primary_m1_bar_jsonl is None or data_source.secondary_m1_bar_jsonl is None):
        raise ValueError("PAIRED_M1_BAR_JSONL requires primary_m1_bar_jsonl and secondary_m1_bar_jsonl")
    for source_path in data_source.source_paths:
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
    split = raw["split_policy"]
    split_policy = SplitPolicy(
        minimum_mature_rows=int(split.get("minimum_mature_rows", 24)),
        oof_train_fraction=_fraction(split.get("oof_train_fraction", 0.20), "oof_train_fraction"),
        oof_calibration_fraction=_fraction(split.get("oof_calibration_fraction", 0.05), "oof_calibration_fraction"),
        oof_threshold_fraction=_fraction(split.get("oof_threshold_fraction", 0.05), "oof_threshold_fraction"),
        oof_holdout_fraction=_fraction(split.get("oof_holdout_fraction", 0.10), "oof_holdout_fraction"),
        final_train_fraction=_fraction(split.get("final_train_fraction", 0.35), "final_train_fraction"),
        final_calibration_fraction=_fraction(split.get("final_calibration_fraction", 0.05), "final_calibration_fraction"),
        final_threshold_fraction=_fraction(split.get("final_threshold_fraction", 0.05), "final_threshold_fraction"),
        final_test_fraction=_fraction(split.get("final_test_fraction", 0.15), "final_test_fraction"),
        purge_ms=int(split.get("purge_ms", 3_600_000)),
        embargo_ms=int(split.get("embargo_ms", 3_600_000)),
    )
    total = sum((split_policy.oof_train_fraction, split_policy.oof_calibration_fraction, split_policy.oof_threshold_fraction,
                 split_policy.oof_holdout_fraction, split_policy.final_train_fraction, split_policy.final_calibration_fraction,
                 split_policy.final_threshold_fraction, split_policy.final_test_fraction))
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"split fractions must sum to one, got {total}")
    resource = raw.get("resource_policy", {})
    resource_policy = ResourcePolicy(
        seed=int(resource.get("seed", 1701)), max_rows=int(resource.get("max_rows", 2_000_000)),
        max_features=int(resource.get("max_features", 10_000)), max_memory_mb=int(resource.get("max_memory_mb", 8192)),
        max_wall_seconds=float(resource.get("max_wall_seconds", 3600.0)), max_workers=int(resource.get("max_workers", 1)),
    )
    return ActivationConfig(
        schema_version="1.0.0", run_id=str(raw["run_id"]), output_root=_path(raw["output_root"], "output_root", base),
        data_source=data_source, split_policy=split_policy, resource_policy=resource_policy,
        selected_task_ids=tuple(str(x) for x in raw.get("selected_task_ids", ())),
        family_filter=tuple(str(x) for x in raw.get("family_filter", ())),
        train_all_mature_tasks=bool(raw.get("train_all_mature_tasks", True)),
        retain_materialized_views=bool(raw.get("retain_materialized_views", True)),
        fail_on_task_insufficiency=bool(raw.get("fail_on_task_insufficiency", False)),
    )
