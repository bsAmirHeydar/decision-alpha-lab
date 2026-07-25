from __future__ import annotations
from collections import defaultdict
from decimal import Decimal
from statistics import median
from typing import Mapping, Sequence
from .contracts import TransformPlan, SplitPlan
from .enums import FoldRole, TransformKind
from .errors import ContractError

def fit_transform_plan(*,transform_id:str,version:str,fold_id:str,feature_rows:Mapping[str,Mapping[str,Decimal|None]],split_plan:SplitPlan,kinds:Sequence[TransformKind]=(TransformKind.STANDARDIZE,TransformKind.IMPUTE_MEDIAN),missingness_mask:bool=True)->TransformPlan:
    train_ids=sorted(a.opportunity_id for a in split_plan.assignments if a.fold_id==fold_id and a.role==FoldRole.TRAIN)
    if not train_ids: raise ContractError("empty_transform_fit_set","transform fit set has no training rows")
    names=sorted({n for oid in train_ids for n in feature_rows.get(oid,{})})
    params={}
    for n in names:
        vals=[feature_rows[oid].get(n) for oid in train_ids if feature_rows.get(oid,{}).get(n) is not None]
        if not vals:
            params[n]={"median":"0","mean":"0","std":"1","min":"0","max":"0","missing_count":len(train_ids)}; continue
        vals=[Decimal(v) for v in vals]
        mean=sum(vals,Decimal("0"))/Decimal(len(vals))
        var=sum((v-mean)*(v-mean) for v in vals)/Decimal(max(1,len(vals)-1))
        std=Decimal(str(float(var)**0.5)) if var>0 else Decimal("1")
        params[n]={"median":median(vals),"mean":mean,"std":std,"min":min(vals),"max":max(vals),"missing_count":len(train_ids)-len(vals)}
    return TransformPlan(transform_id,version,fold_id,tuple(names),tuple(kinds),tuple(train_ids),params,missingness_mask)
