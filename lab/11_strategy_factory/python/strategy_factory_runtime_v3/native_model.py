from __future__ import annotations
import math
from typing import Sequence
from .contracts import NativeModelArtifact
from .enums import ModelKind,Precision
from .preprocessing import f32,cast_precision
from .errors import RuntimeContractError

def _dot(row:Sequence[float],x:Sequence[float],precision:Precision)->float:
    if len(row)!=len(x):raise RuntimeContractError('inference_shape_mismatch','input width differs from model')
    acc=cast_precision(0.0,precision)
    for w,v in zip(row,x):acc=cast_precision(acc+cast_precision(w*v,precision),precision)
    return acc

def logits(model:NativeModelArtifact,x:Sequence[float])->tuple[float,...]:
    if len(x)!=len(model.input_names):raise RuntimeContractError('inference_shape_mismatch','input width differs from model')
    return tuple(cast_precision(_dot(row,x,model.precision)+b,model.precision) for row,b in zip(model.weights,model.bias))

def predict(model:NativeModelArtifact,x:Sequence[float])->tuple[float,...]:
    z=logits(model,x)
    if model.kind is ModelKind.LINEAR_SCALAR:return z
    m=max(z); ex=[math.exp(float(v-m)) for v in z]; s=sum(ex)
    return tuple(cast_precision(v/s,model.precision) for v in ex)

def decision(model:NativeModelArtifact,outputs:Sequence[float])->str:
    if len(outputs)!=len(model.output_names):raise RuntimeContractError('output_shape_mismatch','output width differs from model')
    return sorted(zip(model.output_names,outputs),key=lambda kv:(-float(kv[1]),kv[0]))[0][0]
