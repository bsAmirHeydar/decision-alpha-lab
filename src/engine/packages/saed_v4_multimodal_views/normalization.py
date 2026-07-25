from __future__ import annotations
from .enums import NormalizationKind
from .errors import NormalizationError

def normalize(value,spec):
    if value is None:return None
    if spec.kind==NormalizationKind.NONE:return value
    if not isinstance(value,(int,float)) or isinstance(value,bool):raise NormalizationError('numeric normalization requires number')
    x=float(value)
    if spec.kind==NormalizationKind.STATIC_ZSCORE:
        if spec.center is None or spec.scale is None or spec.scale<=0:raise NormalizationError('invalid zscore statistics')
        return (x-spec.center)/spec.scale
    if spec.kind==NormalizationKind.STATIC_ROBUST:
        if spec.center is None or spec.scale is None or spec.scale<=0:raise NormalizationError('invalid robust statistics')
        return (x-spec.center)/spec.scale
    if spec.kind==NormalizationKind.STATIC_MINMAX:
        if spec.minimum is None or spec.maximum is None or spec.maximum<=spec.minimum:raise NormalizationError('invalid minmax statistics')
        return (x-spec.minimum)/(spec.maximum-spec.minimum)
    raise NormalizationError('unsupported normalizer')

def validate_static_normalizer(spec):
    if spec.kind!=NormalizationKind.NONE and (not spec.statistics_artifact_id or not spec.statistics_hash or len(spec.statistics_hash)!=64):raise NormalizationError('normalizer must be exact-version artifact backed')
