from __future__ import annotations
from .models import TwinStateSnapshot
from .enums import TwinState
from .canonical import content_hash

def build_snapshot(manifest,known_as_of,lifecycle_state,observations,hypothesis_states,support_evaluation,contradictions,evidence_debts,transition_events,sequence):
    payload={'twin_id':manifest.twin_id,'manifest_hash':manifest.semantic_hash,'known_as_of':known_as_of,'lifecycle_state':lifecycle_state,'twin_state':_derive_twin_state(contradictions,evidence_debts,support_evaluation).value,'observation_ids':sorted(x.observation_id for x in observations),'hypothesis_states':[{'hypothesis_id':x.hypothesis_id,'weighted_score':x.weighted_score,'total_weight':x.total_weight,'status':x.status.value,'assessment_ids':list(x.assessment_ids)} for x in hypothesis_states],'support_evaluation_id':support_evaluation.evaluation_id if support_evaluation else None,'contradiction_ids':sorted(x.contradiction_id for x in contradictions if not x.resolved),'evidence_debt_ids':sorted(x.debt_id for x in evidence_debts if not x.resolved),'transition_event_ids':sorted(x.event_id for x in transition_events),'sequence':sequence}
    h=content_hash(payload)
    return TwinStateSnapshot(manifest.twin_id,manifest.semantic_hash,known_as_of,lifecycle_state,TwinState(payload['twin_state']),tuple(payload['observation_ids']),tuple(hypothesis_states),payload['support_evaluation_id'],tuple(payload['contradiction_ids']),tuple(payload['evidence_debt_ids']),tuple(payload['transition_event_ids']),sequence,h)
def _derive_twin_state(contradictions,debt,support):
    if any(getattr(x.severity,'value',x.severity) in {'critical','material'} and not x.resolved for x in contradictions):return TwinState.CONFLICTED
    if any(getattr(x.severity,'value',x.severity)=='blocking' and not x.resolved for x in debt):return TwinState.QUARANTINED
    if support and support.status.value in {'unsupported','unknown'}:return TwinState.DEGRADED
    return TwinState.OBSERVING
