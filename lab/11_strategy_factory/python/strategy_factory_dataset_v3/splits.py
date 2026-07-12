from __future__ import annotations
from collections import defaultdict
from typing import Sequence
from .canonical import sha256, safe_id
from .contracts import *
from .enums import FoldRole
from .errors import ContractError

def build_purged_embargoed_plan(anchors:Sequence[OpportunityAnchor],*,plan_id:str="split.walk_forward",version:str="1.0.0",fold_count:int=3,purge_ms:int=0,embargo_ms:int=0)->SplitPlan:
    safe_id(plan_id,'plan_id')
    if fold_count<2: raise ContractError("insufficient_fold_count","at least two folds are required")
    groups=defaultdict(list)
    for a in anchors: groups[a.dependence_cluster_id].append(a)
    ordered=sorted(groups.items(),key=lambda kv:(min(x.decision_time_ms for x in kv[1]),kv[0]))
    if len(ordered)<fold_count: raise ContractError("insufficient_clusters","fold count exceeds dependence clusters")
    buckets=[[] for _ in range(fold_count)]
    for i,item in enumerate(ordered): buckets[min(fold_count-1,(i*fold_count)//len(ordered))].append(item)
    folds=[]; assignments=[]
    all_anchors=tuple(anchors)
    global_start=min(a.decision_time_ms for a in anchors); global_end=max(a.decision_time_ms for a in anchors)
    for i,bucket in enumerate(buckets):
        test_items=[a for _,xs in bucket for a in xs]
        t0=min(a.decision_time_ms for a in test_items); t1=max(a.decision_time_ms for a in test_items)
        fold_id=f"fold.{i+1:02d}"
        folds.append(FoldWindow(fold_id,global_start,max(global_start,t0-purge_ms-1),t0,t1,purge_ms,embargo_ms))
        test_clusters={a.dependence_cluster_id for a in test_items}
        for a in all_anchors:
            if a.dependence_cluster_id in test_clusters: role=FoldRole.TEST; reason="cluster_locked_test"
            elif t0-purge_ms<=a.decision_time_ms<t0: role=FoldRole.PURGED; reason="purge_window"
            elif t1<a.decision_time_ms<=t1+embargo_ms: role=FoldRole.EMBARGO; reason="embargo_window"
            elif a.decision_time_ms<t0-purge_ms: role=FoldRole.TRAIN; reason="historical_train"
            else: role=FoldRole.UNUSED; reason="future_not_available_to_fold"
            assignments.append(SplitAssignment(fold_id,a.opportunity_id,a.dependence_cluster_id,role,a.decision_time_ms,reason))
    return SplitPlan(plan_id,version,tuple(folds),tuple(assignments),sha256(sorted(groups)),True,False)

def roles_by_opportunity(plan:SplitPlan)->dict[str,dict[str,str]]:
    out=defaultdict(dict)
    for a in plan.assignments: out[a.opportunity_id][a.fold_id]=a.role.value
    return dict(out)
