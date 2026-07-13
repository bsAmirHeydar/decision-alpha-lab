from __future__ import annotations
from fp_i02_kernel.enums import WindowKind,PriceSide,ReferenceState
from fp_i05_reference.enums import PairWindowHealth
from fp_i05_reference.store import get_references_for_window
from .canonical import canonical_sha256,stable_id
from .contracts import WWRelationInstance,WWSidePlan,WWCompilationReport
from .enums import WWDataState
from .errors import FPI08Error

def _find_week(snapshot,week_id):
    return next((w for w in snapshot.pair_windows if w.descriptor.kind is WindowKind.W and w.descriptor.week_id==week_id),None)

def compile_ww(config,snapshot,previous_week_id,current_week_id):
    if snapshot.semantic_hash!=config.reference_store_hash: raise FPI08Error("FP_WRC_STORE_HASH_MISMATCH","WW config store hash mismatch")
    previous=_find_week(snapshot,previous_week_id); current=_find_week(snapshot,current_week_id); blocked=[]
    if previous is None: blocked.append("FP_WRC_PREVIOUS_WEEK_MISSING")
    if current is None: blocked.append("FP_WRC_CURRENT_WEEK_MISSING")
    if blocked:
        material={"previous":previous_week_id,"current":current_week_id,"blocked":blocked,"store":snapshot.semantic_hash}
        return WWCompilationReport(stable_id("FPWWCOMP",material,32),None,(),tuple(blocked),snapshot.semantic_hash,canonical_sha256(material))
    data_state=WWDataState.COMPLETE
    if not previous.completed or previous.health is PairWindowHealth.BLOCKED: data_state=WWDataState.INCOMPLETE;blocked.append("FP_WRC_PREVIOUS_WEEK_INCOMPLETE")
    if current.health is PairWindowHealth.BLOCKED: data_state=WWDataState.INCOMPLETE;blocked.append("FP_WRC_CURRENT_WEEK_BLOCKED")
    mat={"pair":snapshot.pair_id,"previous":previous_week_id,"current":current_week_id,"reference":previous.pair_window_id,"check":current.pair_window_id,"start":current.descriptor.start_utc_ms,"end":current.descriptor.end_utc_ms,"store":snapshot.semantic_hash,"revision":snapshot.source_revision_id,"data_state":data_state}
    instance=WWRelationInstance(stable_id("FPWWREL",mat,32),snapshot.pair_id,previous_week_id,current_week_id,previous.pair_window_id,current.pair_window_id,current.descriptor.start_utc_ms,current.descriptor.end_utc_ms,snapshot.semantic_hash,snapshot.source_revision_id,data_state,tuple(blocked or ["FP_WRC_WW_RELATION_COMPILED"]),canonical_sha256(mat))
    refs=get_references_for_window(snapshot,previous.pair_window_id); idx={(r.canonical_symbol,r.side):r for r in refs}; symbols=tuple(sorted({r.canonical_symbol for r in refs})); plans=[]
    if len(symbols)!=2: blocked.append("FP_WRC_REFERENCE_PAIR_INCOMPLETE")
    else:
        for side in (PriceSide.HIGH,PriceSide.LOW):
            left=idx.get((symbols[0],side));right=idx.get((symbols[1],side))
            if left is None or right is None: blocked.append(f"FP_WRC_{side.value}_REFERENCE_MISSING");continue
            terminal={ReferenceState.CONSUMED_BY_PROTECTED_TOUCH,ReferenceState.EXPIRED,ReferenceState.SUPERSEDED}
            pstate=data_state
            reasons=["FP_WRC_WW_SIDE_PLAN_ELIGIBLE"]
            if left.state in terminal or right.state in terminal: pstate=WWDataState.INCOMPLETE;reasons=["FP_WRC_WEEKLY_REFERENCE_NOT_REUSABLE"]
            pm={"instance":instance.semantic_hash,"side":side,"left":left.semantic_hash,"right":right.semantic_hash,"start":instance.check_start_utc_ms,"end":instance.check_end_utc_ms,"state":pstate}
            plans.append(WWSidePlan(stable_id("FPWWPLAN",pm,32),instance.relation_instance_id,snapshot.pair_id,side,left.reference_id,left.canonical_symbol,left.price,right.reference_id,right.canonical_symbol,right.price,instance.check_start_utc_ms,instance.check_end_utc_ms,tuple(sorted((left.semantic_hash,right.semantic_hash))),pstate,tuple(reasons),canonical_sha256(pm)))
    material={"instance":instance.semantic_hash,"plans":[p.semantic_hash for p in plans],"blocked":sorted(blocked),"store":snapshot.semantic_hash}
    return WWCompilationReport(stable_id("FPWWCOMP",material,32),instance,tuple(sorted(plans,key=lambda p:p.side.value)),tuple(sorted(set(blocked))),snapshot.semantic_hash,canonical_sha256(material))
