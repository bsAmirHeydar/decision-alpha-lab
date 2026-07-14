from __future__ import annotations
from .state import build_snapshot
from .errors import ReplayError

def replay_snapshot(manifest,known_as_of,lifecycle_state,observations,hypothesis_states,support_evaluation,contradictions,evidence_debts,transition_events,sequence,expected_hash=None):
    snap=build_snapshot(manifest,known_as_of,lifecycle_state,observations,hypothesis_states,support_evaluation,contradictions,evidence_debts,transition_events,sequence)
    if expected_hash and snap.snapshot_hash!=expected_hash:raise ReplayError('snapshot replay mismatch')
    return snap
