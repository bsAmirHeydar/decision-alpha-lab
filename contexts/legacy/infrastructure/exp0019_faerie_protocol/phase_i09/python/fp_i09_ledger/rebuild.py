from .events import verify_chain
from .errors import FPI09Error

def assert_snapshot_replay_parity(left,right):
    attrs=("config_hash","chain_head_hash","signal_index","session_index","relation_index")
    for a in attrs:
        if getattr(left,a)!=getattr(right,a): raise FPI09Error("FP_LDG_REPLAY_PARITY_FAILED",f"snapshot mismatch: {a}")
    if tuple(r.record_hash for r in left.records)!=tuple(r.record_hash for r in right.records): raise FPI09Error("FP_LDG_REPLAY_PARITY_FAILED","record hashes differ")
    if tuple(d.decision_hash for d in left.decisions)!=tuple(d.decision_hash for d in right.decisions): raise FPI09Error("FP_LDG_REPLAY_PARITY_FAILED","decision hashes differ")
    return True

def validate_event_stream(events):
    if not verify_chain(events): raise FPI09Error("FP_LDG_EVENT_CHAIN_INVALID","event stream is not a valid append-only chain")
    return True

def semantic_fingerprint(snapshot):
    records=tuple(sorted((r.signal.signal_id,r.disposition.value,r.quota_key_id,r.winner_signal_id) for r in snapshot.records))
    decisions=tuple(sorted((d.quota_key.quota_key_id,d.winner_signal_id,tuple(sorted(d.suppressed_signal_ids)),tuple(sorted(d.blocked_signal_ids)),d.seal_state.value) for d in snapshot.decisions))
    return (snapshot.config_hash,records,decisions,snapshot.signal_index,snapshot.session_index,snapshot.relation_index)

def assert_semantic_parity(left,right):
    if semantic_fingerprint(left)!=semantic_fingerprint(right):
        raise FPI09Error("FP_LDG_SEMANTIC_PARITY_FAILED","materialized semantic state differs")
    return True
