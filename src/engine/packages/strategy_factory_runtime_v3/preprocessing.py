from __future__ import annotations
import math,struct
from typing import Any,Mapping
from .contracts import PreprocessingContract,FeatureRule
from .enums import FeatureKind,MissingPolicy,ScalingKind,Precision
from .errors import RuntimeContractError

def f32(x:float)->float:return struct.unpack('<f',struct.pack('<f',float(x)))[0]
def cast_precision(x:float,precision:Precision)->float:return f32(x) if precision is Precision.FLOAT32 else float(x)

def _value(rule:FeatureRule,features:Mapping[str,Any])->Any:
    missing=rule.name not in features or features[rule.name] is None
    if not missing:return features[rule.name]
    if rule.missing is MissingPolicy.ERROR:raise RuntimeContractError('missing_feature',f'missing feature {rule.name}')
    return 0.0 if rule.missing is MissingPolicy.ZERO else rule.missing_value

def transform(contract:PreprocessingContract,features:Mapping[str,Any])->tuple[float,...]:
    if contract.reject_unknown_features:
        unknown=sorted(set(features)-set(contract.feature_order))
        if unknown:raise RuntimeContractError('unknown_features','input contains undeclared features',{'unknown':unknown})
    out=[]
    for rule in contract.rules:
        raw=_value(rule,features)
        if rule.kind is FeatureKind.CATEGORICAL:
            if raw not in rule.categories:raise RuntimeContractError('unknown_category',f'unknown category for {rule.name}',{'value':raw})
            out.extend(cast_precision(1.0 if raw==c else 0.0,contract.precision) for c in rule.categories);continue
        if rule.kind is FeatureKind.BOOLEAN:
            if raw not in (True,False,0,1):raise RuntimeContractError('invalid_boolean',f'{rule.name} is not boolean')
            out.append(cast_precision(1.0 if bool(raw) else 0.0,contract.precision));continue
        try:x=float(raw)
        except Exception as e:raise RuntimeContractError('non_numeric_feature',f'{rule.name} is not numeric',{'value':raw}) from e
        if not math.isfinite(x):raise RuntimeContractError('non_finite_feature',f'{rule.name} is non-finite')
        if rule.clip_min is not None:x=max(x,rule.clip_min)
        if rule.clip_max is not None:x=min(x,rule.clip_max)
        if rule.scaling is ScalingKind.ZSCORE:x=(x-rule.mean)/rule.scale
        elif rule.scaling is ScalingKind.MINMAX:x=(x-rule.minimum)/(rule.maximum-rule.minimum)
        out.append(cast_precision(x,contract.precision))
    return tuple(out)

def preprocessing_trace(contract:PreprocessingContract,features:Mapping[str,Any])->dict[str,Any]:
    values=transform(contract,features)
    return {'contract_hash':contract.preprocessing_hash,'input_order':list(contract.feature_order),'output_order':list(contract.output_names),'values':list(values),'precision':contract.precision.value}
