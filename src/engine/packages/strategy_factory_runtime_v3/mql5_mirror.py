from __future__ import annotations
import math,struct
from typing import Mapping,Any,Sequence
from .contracts import PreprocessingContract,NativeModelArtifact
from .enums import FeatureKind,MissingPolicy,ScalingKind
from .errors import RuntimeContractError

def _f(x):return struct.unpack('<f',struct.pack('<f',float(x)))[0]
def preprocess_mirror(contract:PreprocessingContract,features:Mapping[str,Any])->tuple[float,...]:
    if contract.reject_unknown_features and set(features)-set(contract.feature_order):raise RuntimeContractError('unknown_features','MQL5 mirror rejects unknown features')
    out=[]
    for r in contract.rules:
        if r.name not in features or features[r.name] is None:
            if r.missing is MissingPolicy.ERROR:raise RuntimeContractError('missing_feature',f'missing {r.name}')
            v=0.0 if r.missing is MissingPolicy.ZERO else r.missing_value
        else:v=features[r.name]
        if r.kind is FeatureKind.CATEGORICAL:
            if v not in r.categories:raise RuntimeContractError('unknown_category',f'unknown {r.name}')
            for c in r.categories:
                out.append(_f(1.0 if v==c else 0.0))
            continue
        if r.kind is FeatureKind.BOOLEAN:
            out.append(_f(1.0 if bool(v) else 0.0))
            continue
        x=float(v)
        if r.clip_min is not None:x=max(x,r.clip_min)
        if r.clip_max is not None:x=min(x,r.clip_max)
        if r.scaling is ScalingKind.ZSCORE:x=(x-r.mean)/r.scale
        elif r.scaling is ScalingKind.MINMAX:x=(x-r.minimum)/(r.maximum-r.minimum)
        out.append(_f(x))
    return tuple(out)
def predict_mirror(model:NativeModelArtifact,x:Sequence[float])->tuple[float,...]:
    z=[]
    for row,b in zip(model.weights,model.bias):
        acc=_f(0.0)
        for w,v in zip(row,x):acc=_f(acc+_f(w*v))
        z.append(_f(acc+b))
    if model.kind.value=='linear_scalar':return tuple(z)
    m=max(z);ex=[math.exp(float(v-m)) for v in z];s=sum(ex);return tuple(_f(v/s) for v in ex)
def decision_mirror(model:NativeModelArtifact,y:Sequence[float])->str:return sorted(zip(model.output_names,y),key=lambda kv:(-float(kv[1]),kv[0]))[0][0]
