from __future__ import annotations
from fp_i02_kernel.enums import RelationCode,WindowKind,PriceSide,ReferenceState
from fp_i05_reference.store import window_index,get_references_for_window
from fp_i05_reference.enums import WindowBuildState,PairWindowHealth,SelectorDisposition
from .canonical import canonical_sha256,stable_id
from .contracts import RelationInstance,RelationSidePlan,RelationCompilationReport
from .enums import RelationInstanceState,SidePlanState
from .registry import resolve_relation,registry_hash
from .errors import FPI06Error

def _make_instance(snapshot,descriptor,anchor_date,reference_window,check_window,offset):
    state=RelationInstanceState.COMPILED
    reasons=['FP_HRC_RELATION_COMPILED']
    if reference_window is None or check_window is None:
        raise FPI06Error('FP_HRC_RELATION_WINDOW_MISSING','compiler requires reference and check windows')
    if not reference_window.completed:
        state=RelationInstanceState.BLOCKED;reasons=['FP_HRC_REFERENCE_WINDOW_NOT_COMPLETE']
    elif check_window.health is PairWindowHealth.BLOCKED:
        state=RelationInstanceState.BLOCKED;reasons=['FP_HRC_CHECK_WINDOW_BLOCKED']
    elif check_window.completed:
        state=RelationInstanceState.COMPLETE
    else:
        state=RelationInstanceState.ACTIVE
    material={'relation':descriptor.relation,'pair_id':snapshot.pair_id,'anchor':anchor_date,'offset':offset,'reference_pair_window_id':reference_window.pair_window_id,'reference_descriptor_id':reference_window.descriptor.descriptor_id,'check_pair_window_id':check_window.pair_window_id,'check_descriptor_id':check_window.descriptor.descriptor_id,'check_start':check_window.descriptor.start_utc_ms,'check_end':check_window.descriptor.end_utc_ms,'store':snapshot.semantic_hash,'revision':snapshot.source_revision_id}
    sem=canonical_sha256(material)
    return RelationInstance(stable_id('FPREL',material,32),descriptor.relation,snapshot.pair_id,anchor_date,offset,reference_window.pair_window_id,reference_window.descriptor.descriptor_id,reference_window.descriptor.kind,reference_window.descriptor.trading_date,check_window.pair_window_id,check_window.descriptor.descriptor_id,check_window.descriptor.kind,check_window.descriptor.start_utc_ms,check_window.descriptor.end_utc_ms,snapshot.semantic_hash,snapshot.source_revision_id,state,tuple(reasons),sem)

def _side_plans(snapshot,instance,reference_window):
    refs=get_references_for_window(snapshot,reference_window.pair_window_id)
    index={(r.canonical_symbol,r.side):r for r in refs}
    symbols=tuple(sorted({r.canonical_symbol for r in refs}))
    plans=[]
    if len(symbols)!=2:return tuple()
    for side in (PriceSide.HIGH,PriceSide.LOW):
        left=index.get((symbols[0],side));right=index.get((symbols[1],side))
        state=SidePlanState.ELIGIBLE;reasons=['FP_HRC_SIDE_PLAN_ELIGIBLE']
        if left is None or right is None:
            state=SidePlanState.REFERENCE_UNAVAILABLE;reasons=['FP_HRC_REFERENCE_PAIR_INCOMPLETE']
            continue
        terminal={ReferenceState.CONSUMED_BY_PROTECTED_TOUCH,ReferenceState.EXPIRED,ReferenceState.SUPERSEDED}
        if left.state in terminal or right.state in terminal:
            state=SidePlanState.REFERENCE_CONSUMED;reasons=['FP_HRC_REFERENCE_SIDE_NOT_REUSABLE']
        if instance.state is RelationInstanceState.BLOCKED:
            state=SidePlanState.DATA_BLOCKED;reasons=list(instance.reason_codes)
        material={'instance':instance.semantic_hash,'side':side,'left':left.semantic_hash,'left_state':left.state,'right':right.semantic_hash,'right_state':right.state,'check_start':instance.check_start_utc_ms,'check_end':instance.check_end_utc_ms}
        sem=canonical_sha256(material)
        plans.append(RelationSidePlan(stable_id('FPRELPLAN',material,32),instance.relation_instance_id,instance.relation,side,left.reference_id,left.canonical_symbol,left.price,right.reference_id,right.canonical_symbol,right.price,instance.check_start_utc_ms,instance.check_end_utc_ms,state,tuple(reasons),tuple(sorted((left.semantic_hash,right.semantic_hash))),sem))
    return tuple(plans)

def compile_relations(config,snapshot,anchor_trading_date,calendar_selection=None):
    if config.reference_store_hash!=snapshot.semantic_hash: raise FPI06Error('FP_HRC_STORE_HASH_MISMATCH','compiler config store hash mismatch')
    if config.relation_registry_hash!=registry_hash(): raise FPI06Error('FP_HRC_REGISTRY_HASH_MISMATCH','relation registry hash mismatch')
    idx=window_index(snapshot);instances=[];plans=[];skipped=[];blocked=[]
    for code in config.enabled_relations:
        desc=resolve_relation(code)
        if not desc.supported_in_phase: skipped.append(f'{code.value}:DEFERRED');continue
        check=idx.get((anchor_trading_date,desc.check_kind))
        if check is None:
            blocked.append(f'{code.value}:CHECK_WINDOW_MISSING');continue
        if not desc.historical_selector_required:
            reference=idx.get((anchor_trading_date,desc.reference_kind))
            if reference is None:blocked.append(f'{code.value}:REFERENCE_WINDOW_MISSING');continue
            instance=_make_instance(snapshot,desc,anchor_trading_date,reference,check,0);instances.append(instance);plans.extend(_side_plans(snapshot,instance,reference))
        else:
            if calendar_selection is None:blocked.append(f'{code.value}:SELECTION_REQUIRED');continue
            if calendar_selection.anchor_trading_date!=anchor_trading_date or calendar_selection.store_snapshot_hash!=snapshot.semantic_hash: raise FPI06Error('FP_HRC_SELECTION_LINEAGE_MISMATCH','calendar selection lineage mismatch')
            for item in calendar_selection.items:
                if item.disposition is not SelectorDisposition.SELECTED:
                    skipped.append(f'{code.value}:OFFSET_{item.offset}:{item.disposition.value}');continue
                reference=next((w for w in snapshot.pair_windows if w.pair_window_id==item.pair_window_id),None)
                if reference is None:blocked.append(f'{code.value}:OFFSET_{item.offset}:WINDOW_NOT_FOUND');continue
                instance=_make_instance(snapshot,desc,anchor_trading_date,reference,check,item.offset);instances.append(instance);plans.extend(_side_plans(snapshot,instance,reference))
    instances=tuple(sorted(instances,key=lambda x:(x.relation.value,x.calendar_offset,x.relation_instance_id)))
    plans=tuple(sorted(plans,key=lambda x:(x.relation.value,next(i.calendar_offset for i in instances if i.relation_instance_id==x.relation_instance_id),x.side.value,x.side_plan_id)))
    material={'anchor':anchor_trading_date,'instances':[i.semantic_hash for i in instances],'plans':[p.semantic_hash for p in plans],'skipped':sorted(skipped),'blocked':sorted(blocked),'store':snapshot.semantic_hash,'registry':registry_hash()}
    return RelationCompilationReport(stable_id('FPRELCOMP',material,32),anchor_trading_date,instances,plans,tuple(sorted(skipped)),tuple(sorted(blocked)),snapshot.semantic_hash,registry_hash(),canonical_sha256(material))
