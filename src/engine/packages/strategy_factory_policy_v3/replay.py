from __future__ import annotations
from .engine import execute_policy
from .canonical import canonical_sha256

def replay_many(graph,occurrences,manual_policy,fallback_policy,authority_matrix,*,admission=None,outputs=None,overrides=None):
    outputs=outputs or {}; overrides=overrides or {}
    decisions=[execute_policy(graph,o,manual_policy,fallback_policy,authority_matrix,admission=admission,model_output=outputs.get(o.occurrence_id),operator_override=overrides.get(o.occurrence_id)) for o in sorted(occurrences,key=lambda x:(x.known_time_ms,x.occurrence_id))]
    return tuple(decisions),canonical_sha256([d.decision_hash for d in decisions])
