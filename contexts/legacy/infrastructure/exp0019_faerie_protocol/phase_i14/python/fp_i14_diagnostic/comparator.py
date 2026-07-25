from __future__ import annotations
from itertools import combinations
from .contracts import *
from .canonical import sha256,stable_id

def _mm(kind,left,right,sequence=0,semantic_id="",field="",lv="",rv="",reason="FP_DIAG_DIFFERENTIAL_MISMATCH"):
    return DifferentialMismatch(stable_id("FPMM",{"kind":kind.value,"left":left.product.value,"right":right.product.value,"seq":sequence,"sid":semantic_id,"field":field,"lv":lv,"rv":rv}),kind,left.product,right.product,sequence,semantic_id,field,sha256(lv),sha256(rv),reason)

def compare_runs(left:TraceRun,right:TraceRun):
    mism=[]
    lm,rm=left.manifest,right.manifest
    if lm.semantic_manifest_hash!=rm.semantic_manifest_hash:
        if lm.config_hash!=rm.config_hash:mism.append(_mm(MismatchKind.CONFIG_MISMATCH,left,right,field="config_hash",lv=lm.config_hash,rv=rm.config_hash,reason="FP_DIAG_CONFIG_MISMATCH"))
        if lm.source_revision_id!=rm.source_revision_id:mism.append(_mm(MismatchKind.SOURCE_REVISION_MISMATCH,left,right,field="source_revision_id",lv=lm.source_revision_id,rv=rm.source_revision_id,reason="FP_DIAG_SOURCE_REVISION_MISMATCH"))
        if lm.module_versions!=rm.module_versions:mism.append(_mm(MismatchKind.MODULE_VERSION_MISMATCH,left,right,field="module_versions",lv=lm.module_versions,rv=rm.module_versions,reason="FP_DIAG_MODULE_VERSION_MISMATCH"))
        if not mism:mism.append(_mm(MismatchKind.MANIFEST_MISMATCH,left,right,field="manifest",lv=lm.semantic_manifest_hash,rv=rm.semantic_manifest_hash,reason="FP_DIAG_MANIFEST_MISMATCH"))
    n=max(len(left.events),len(right.events))
    for i in range(n):
        if i>=len(left.events):
            e=right.events[i];mism.append(_mm(MismatchKind.EVENT_MISSING_LEFT,left,right,e.sequence,e.semantic_id,"event","",e.semantic_hash,"FP_DIAG_EVENT_MISSING_LEFT"));continue
        if i>=len(right.events):
            e=left.events[i];mism.append(_mm(MismatchKind.EVENT_MISSING_RIGHT,left,right,e.sequence,e.semantic_id,"event",e.semantic_hash,"","FP_DIAG_EVENT_MISSING_RIGHT"));continue
        a,b=left.events[i],right.events[i]
        if a.sequence!=b.sequence:mism.append(_mm(MismatchKind.SEQUENCE_MISMATCH,left,right,max(a.sequence,b.sequence),a.semantic_id,"sequence",a.sequence,b.sequence,"FP_DIAG_SEQUENCE_MISMATCH"))
        if a.semantic_id!=b.semantic_id:mism.append(_mm(MismatchKind.SEMANTIC_ID_MISMATCH,left,right,max(a.sequence,b.sequence),a.semantic_id,"semantic_id",a.semantic_id,b.semantic_id,"FP_DIAG_SEMANTIC_ID_MISMATCH"))
        if a.payload_hash!=b.payload_hash:mism.append(_mm(MismatchKind.PAYLOAD_MISMATCH,left,right,max(a.sequence,b.sequence),a.semantic_id,"payload_hash",a.payload_hash,b.payload_hash,"FP_DIAG_PAYLOAD_MISMATCH"))
        if a.state!=b.state:mism.append(_mm(MismatchKind.STATE_MISMATCH,left,right,max(a.sequence,b.sequence),a.semantic_id,"state",a.state,b.state,"FP_DIAG_STATE_MISMATCH"))
        if a.event_type==TraceEventType.BUFFER and (a.buffer_index!=b.buffer_index or round(a.numeric_value,10)!=round(b.numeric_value,10)):
            mism.append(_mm(MismatchKind.BUFFER_MISMATCH,left,right,max(a.sequence,b.sequence),a.semantic_id,"buffer",(a.buffer_index,a.numeric_value),(b.buffer_index,b.numeric_value),"FP_DIAG_BUFFER_MISMATCH"))
    if left.inventory.visual_ids!=right.inventory.visual_ids:mism.append(_mm(MismatchKind.VISUAL_INVENTORY_MISMATCH,left,right,field="visual_ids",lv=left.inventory.visual_ids,rv=right.inventory.visual_ids,reason="FP_DIAG_VISUAL_INVENTORY_MISMATCH"))
    status=DifferentialStatus.PASS if not mism else DifferentialStatus.FAIL
    rid=stable_id("FPDIFF",{"left":left.run_id,"right":right.run_id,"mismatches":[m.mismatch_id for m in mism]})
    return PairwiseDifferentialReport(rid,left.run_id,right.run_id,status,min(len(left.events),len(right.events)),tuple(mism),sha256({"report_id":rid,"status":status.value,"mismatches":[m.mismatch_id for m in mism]}))

def compare_products(runs):
    by={r.product:r for r in runs};pairs=[]
    for a,b in combinations(sorted(by,key=lambda x:x.value),2):pairs.append(compare_runs(by[a],by[b]))
    status=DifferentialStatus.PASS if len(by)==3 and all(x.status==DifferentialStatus.PASS for x in pairs) else (DifferentialStatus.BLOCKED if len(by)<3 else DifferentialStatus.FAIL)
    inv=sha256(tuple(sorted((p.value,r.inventory.inventory_hash) for p,r in by.items())))
    rid=stable_id("FPXDIFF",{"fixture":runs[0].fixture_id if runs else "MISSING","products":sorted(p.value for p in by),"reports":[p.report_hash for p in pairs]})
    return CrossProductReport(rid,runs[0].fixture_id if runs else "MISSING",status,tuple(sorted(by,key=lambda x:x.value)),tuple(pairs),inv,sum(len(p.mismatches) for p in pairs),sha256({"report_id":rid,"status":status.value,"reports":[p.report_hash for p in pairs],"inventory":inv}))
