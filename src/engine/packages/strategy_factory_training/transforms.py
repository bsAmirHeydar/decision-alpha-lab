from __future__ import annotations
from statistics import median
from math import sqrt
from typing import Iterable
from .enums import DatasetRole, MissingValuePolicy, ScalePolicy
from .models import DatasetRow, FeatureColumn, TransformSpec, TransformState
from .hashing import sha256_lines

def fit_transform_state(rows: Iterable[DatasetRow], columns: tuple[FeatureColumn,...],
                        feature_schema_hash: str, spec: TransformSpec) -> TransformState:
    rows=tuple(rows)
    if not rows or any(row.role != DatasetRole.TRAIN for row in rows):
        raise ValueError("transform fitting accepts training rows only")
    width=len(columns)
    if any(len(row.feature_values)!=width for row in rows):
        raise ValueError("feature width mismatch")
    impute=[]; means=[]; scales=[]
    for index,column in enumerate(columns):
        observed=[row.feature_values[index] for row in rows if not row.feature_missing[index]]
        if not observed and column.required:
            raise ValueError(f"required feature has no training observations: {column.feature_id}")
        if spec.missing_policy == MissingValuePolicy.REJECT_ROW and len(observed)!=len(rows):
            raise ValueError(f"missing training value rejected: {column.feature_id}")
        fill = median(observed) if (observed and spec.missing_policy==MissingValuePolicy.TRAIN_MEDIAN) else spec.constant_value
        completed=[row.feature_values[index] if not row.feature_missing[index] else fill for row in rows]
        mean=sum(completed)/len(completed)
        variance=sum((value-mean)**2 for value in completed)/len(completed)
        scale=max(spec.minimum_scale,sqrt(variance)) if spec.scale_policy==ScalePolicy.STANDARDIZE else 1.0
        impute.append(float(fill));means.append(float(mean));scales.append(float(scale))
    state=TransformState(feature_schema_hash=feature_schema_hash,spec_hash=spec.spec_hash,
        fitted_role=DatasetRole.TRAIN,fitted_row_count=len(rows),impute_values=tuple(impute),
        means=tuple(means),scales=tuple(scales),fitted_rowset_hash=sha256_lines(r.row_hash for r in rows)).with_hash()
    state.validate();return state

def apply_transform(row: DatasetRow, state: TransformState, spec: TransformSpec) -> tuple[float,...]:
    state.validate()
    if state.spec_hash!=spec.spec_hash:
        raise ValueError("transform specification mismatch")
    result=[]
    for index,(value,missing) in enumerate(zip(row.feature_values,row.feature_missing)):
        if missing:
            if spec.missing_policy==MissingValuePolicy.REJECT_ROW:
                raise ValueError("missing value rejected at application time")
            value=state.impute_values[index]
        result.append((value-state.means[index])/state.scales[index])
    return tuple(result)
