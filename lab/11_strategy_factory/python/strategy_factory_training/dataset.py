from __future__ import annotations
from dataclasses import dataclass
from collections import Counter
from typing import Mapping, Iterable
from .enums import DatasetRole
from .models import FeatureColumn, LabelContract, DatasetRow, DatasetManifest
from .labels import derive_label
from .hashing import stable_id, sha256_lines

@dataclass(frozen=True, slots=True)
class SourceObservation:
    fold_id: str
    role: DatasetRole
    event_id: str
    cluster_id: str
    candidate_id: str
    outcome_id: str
    feature_snapshot_id: str
    known_time_utc_msc: int
    decision_time_utc_msc: int
    resolved_time_utc_msc: int
    features: Mapping[str, float | None]
    net_r: float
    ambiguous: bool = False
    filled: bool = True
    terminal: bool = True

@dataclass(frozen=True, slots=True)
class DatasetBundle:
    columns: tuple[FeatureColumn, ...]
    rows: tuple[DatasetRow, ...]
    manifest: DatasetManifest

def feature_schema_hash(columns: Iterable[FeatureColumn]) -> str:
    ordered = tuple(sorted(columns, key=lambda c: c.ordinal))
    if not ordered:
        raise ValueError("empty feature schema")
    seen_ids=set(); seen_ordinals=set(); hashes=[]
    for index, column in enumerate(ordered):
        column.validate()
        if column.feature_id in seen_ids or column.ordinal in seen_ordinals:
            raise ValueError("duplicate feature identity or ordinal")
        if column.ordinal != index:
            raise ValueError("feature ordinals must be contiguous and zero-based")
        seen_ids.add(column.feature_id); seen_ordinals.add(column.ordinal)
        hashes.append(column.column_hash or column.with_hash().column_hash)
    return stable_id("fsch", "|".join(hashes))

def build_dataset(*, dataset_id: str, dataset_version: str, strategy_id: str,
                  source_run_id: str, source_manifest_hash: str, source_artifact_hash: str,
                  validation_plan_hash: str, columns: Iterable[FeatureColumn],
                  label_contract: LabelContract, observations: Iterable[SourceObservation],
                  created_at_utc_msc: int, code_revision: str) -> DatasetBundle:
    ordered=tuple(sorted(((c if c.column_hash else c.with_hash()) for c in columns), key=lambda c:c.ordinal))
    schema_hash=feature_schema_hash(ordered)
    label_contract = label_contract if label_contract.label_hash else label_contract.with_hash()
    label_contract.validate()
    rows=[]; seen_rows=set(); cluster_roles={}
    for source in observations:
        key=(source.fold_id, source.cluster_id)
        previous=cluster_roles.get(key)
        if previous is not None and previous != source.role:
            raise ValueError("cluster split across dataset roles within a fold")
        cluster_roles[key]=source.role
        values=[]; missing=[]
        for column in ordered:
            value=source.features.get(column.feature_id)
            values.append(0.0 if value is None else float(value))
            missing.append(value is None)
        derived=derive_label(source.net_r, source.ambiguous, source.filled, source.terminal, label_contract)
        if source.role in (DatasetRole.PURGED, DatasetRole.EMBARGO):
            derived=type(derived)(None,False,"excluded_role")
        row=DatasetRow(dataset_id=dataset_id,fold_id=source.fold_id,role=source.role,event_id=source.event_id,
            cluster_id=source.cluster_id,candidate_id=source.candidate_id,outcome_id=source.outcome_id,
            feature_snapshot_id=source.feature_snapshot_id,known_time_utc_msc=source.known_time_utc_msc,
            decision_time_utc_msc=source.decision_time_utc_msc,resolved_time_utc_msc=source.resolved_time_utc_msc,
            feature_values=tuple(values),feature_missing=tuple(missing),label_value=derived.value,
            label_available=derived.available,ambiguous=source.ambiguous,source_manifest_hash=source_manifest_hash,
            source_artifact_hash=source_artifact_hash).with_hashes()
        row.validate(len(ordered))
        if row.row_id in seen_rows:
            raise ValueError("duplicate dataset-row identity")
        seen_rows.add(row.row_id); rows.append(row)
    rows=tuple(sorted(rows,key=lambda r:(r.fold_id,int(r.role),r.decision_time_utc_msc,r.row_id)))
    counts=Counter(r.role for r in rows)
    excluded=counts[DatasetRole.PURGED]+counts[DatasetRole.EMBARGO]
    manifest=DatasetManifest(dataset_id=dataset_id,dataset_version=dataset_version,strategy_id=strategy_id,
        source_run_id=source_run_id,source_manifest_hash=source_manifest_hash,source_artifact_hash=source_artifact_hash,
        validation_plan_hash=validation_plan_hash,feature_schema_hash=schema_hash,
        label_contract_hash=label_contract.label_hash,row_count=len(rows),train_count=counts[DatasetRole.TRAIN],
        validation_count=counts[DatasetRole.VALIDATION],test_count=counts[DatasetRole.TEST],excluded_count=excluded,
        rowset_hash=stable_id("rowset", "".join(r.row_hash+"|" for r in rows)),created_at_utc_msc=created_at_utc_msc,
        code_revision=code_revision).with_hash()
    manifest.validate()
    if min(manifest.train_count,manifest.validation_count,manifest.test_count)<1:
        raise ValueError("dataset requires train, validation and test observations")
    return DatasetBundle(ordered,rows,manifest)

def rows_for_role(rows: Iterable[DatasetRow], role: DatasetRole, require_label: bool=True) -> tuple[DatasetRow,...]:
    result=tuple(row for row in rows if row.role==role and (row.label_available or not require_label))
    if require_label and not result:
        raise ValueError(f"no labeled rows for role {role.name}")
    return result
