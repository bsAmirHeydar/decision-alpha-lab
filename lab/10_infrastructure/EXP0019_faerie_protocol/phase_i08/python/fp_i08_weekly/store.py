from __future__ import annotations
from .canonical import canonical_sha256,stable_id
from .contracts import WWEngineSnapshot
from .enums import EngineHealth,WWDataState,GateEligibility

def build_snapshot(config,contexts,transitions,active_stack,gate_decisions,source_revision_id,created_utc_ms):
    contexts=tuple(sorted(contexts,key=lambda c:(c.confirmed_utc_ms,c.ww_context_id)))
    transitions=tuple(sorted(transitions,key=lambda e:(e.ww_context_id,e.sequence,e.event_id)))
    gates=tuple(sorted(gate_decisions,key=lambda d:d.decision_id))
    if active_stack.data_state is not WWDataState.COMPLETE or any(d.eligibility is GateEligibility.BLOCKED for d in gates): health=EngineHealth.BLOCKED;reasons=("FP_WRC_ENGINE_BLOCKED_WEEKLY_DATA",)
    elif any(d.eligibility is GateEligibility.SUPPRESSED for d in gates): health=EngineHealth.DEGRADED;reasons=("FP_WRC_ENGINE_READY_WITH_SUPPRESSION",)
    else: health=EngineHealth.READY;reasons=("FP_WRC_ENGINE_READY",)
    mat={"config":config.config_hash,"contexts":[c.context_hash for c in contexts],"transitions":[e.event_hash for e in transitions],"stack":active_stack.stack_hash,"gates":[d.decision_hash for d in gates],"health":health,"revision":source_revision_id}
    return WWEngineSnapshot(stable_id("FPWWSTATE",mat,32),config.config_hash,contexts,transitions,active_stack,gates,health,reasons,source_revision_id,created_utc_ms,canonical_sha256(mat))

def upsert_context(contexts,updated):
    out=[];found=False
    for c in contexts:
        if c.ww_context_id==updated.ww_context_id: out.append(updated);found=True
        else: out.append(c)
    if not found: out.append(updated)
    return tuple(sorted(out,key=lambda c:(c.confirmed_utc_ms,c.ww_context_id)))
