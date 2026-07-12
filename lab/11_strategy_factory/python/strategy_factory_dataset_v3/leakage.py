from __future__ import annotations
from collections import defaultdict
from typing import Mapping, Sequence
from .contracts import *
from .enums import LeakageSeverity, FoldRole
from .canonical import sha256

def audit_dataset(*,dataset_id:str,anchors:Sequence[OpportunityAnchor],rows:Sequence[DatasetRow],split_plan:SplitPlan,transform_plans:Sequence[TransformPlan],rebuild_hash_a:str,rebuild_hash_b:str,future_perturbation_passed:bool=True)->DatasetLeakageReport:
    findings=[]
    seen=set()
    for a in anchors:
        if a.opportunity_id in seen: findings.append(LeakageFinding("duplicate_opportunity",LeakageSeverity.FATAL,True,"duplicate opportunity anchor",{"opportunity_id":a.opportunity_id}))
        seen.add(a.opportunity_id)
        if any(s.available_time_ms>a.known_time_ms for s in a.source_inventory): findings.append(LeakageFinding("future_source",LeakageSeverity.FATAL,True,"anchor uses a source unavailable at decision cut",{"opportunity_id":a.opportunity_id}))
    by_fold_cluster=defaultdict(lambda:defaultdict(set))
    by_fold_opp=defaultdict(lambda:defaultdict(set))
    for a in split_plan.assignments:
        by_fold_cluster[a.fold_id][a.dependence_cluster_id].add(a.role)
        by_fold_opp[a.fold_id][a.opportunity_id].add(a.role)
    forbidden={FoldRole.TRAIN,FoldRole.TEST}
    for fold,clusters in by_fold_cluster.items():
        for cluster,roles in clusters.items():
            if forbidden.issubset(roles): findings.append(LeakageFinding("cluster_crosses_train_test",LeakageSeverity.FATAL,True,"dependence cluster crosses train and test",{"fold_id":fold,"cluster_id":cluster}))
    for fold,opps in by_fold_opp.items():
        for opp,roles in opps.items():
            if forbidden.issubset(roles): findings.append(LeakageFinding("sibling_opportunity_crosses_train_test",LeakageSeverity.FATAL,True,"treatment siblings cross train and test",{"fold_id":fold,"opportunity_id":opp}))
    role_index={(a.fold_id,a.opportunity_id):a.role for a in split_plan.assignments}
    for t in transform_plans:
        bad=[oid for oid in t.fit_opportunity_ids if role_index.get((t.fold_id,oid))!=FoldRole.TRAIN]
        if bad: findings.append(LeakageFinding("transform_fit_leakage",LeakageSeverity.FATAL,True,"transform fitted on non-training rows",{"fold_id":t.fold_id,"opportunity_ids":bad}))
    for r in rows:
        if r.row_known_time_ms<r.label.known_time_ms: findings.append(LeakageFinding("row_known_time_precedes_label_evidence",LeakageSeverity.ERROR,True,"row known time precedes label evidence",{"row_id":r.row_id}))
    reproducible=rebuild_hash_a==rebuild_hash_b
    if not reproducible: findings.append(LeakageFinding("non_reproducible_dataset",LeakageSeverity.FATAL,True,"identical manifest inputs rebuilt to different hashes",{"a":rebuild_hash_a,"b":rebuild_hash_b}))
    if not future_perturbation_passed: findings.append(LeakageFinding("future_perturbation_changed_past",LeakageSeverity.FATAL,True,"future-only mutation changed past anchor or feature identity"))
    source_ok=len({tuple((s.source_id,s.revision,s.content_hash) for s in a.source_inventory) for a in anchors})>=1
    return DatasetLeakageReport(dataset_id,tuple(findings),future_perturbation_passed,reproducible,source_ok)
