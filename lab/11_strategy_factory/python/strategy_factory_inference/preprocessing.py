from __future__ import annotations
from .models import PreprocessingManifest
import math

def transform(values, missing, manifest: PreprocessingManifest) -> tuple[float,...]:
    manifest.validate(len(values))
    if len(values)!=len(missing): raise ValueError("value/missing width mismatch")
    out=[]
    for value,is_missing,impute,mean,scale in zip(values,missing,manifest.impute_values,manifest.means,manifest.scales):
        source=impute if is_missing else float(value)
        if not math.isfinite(source): raise ValueError("non-finite observed feature")
        out.append((source-mean)/scale)
    return tuple(out)
