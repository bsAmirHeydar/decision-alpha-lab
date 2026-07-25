from __future__ import annotations
from collections import defaultdict
from .canonical import canonical_sha256,stable_id
from .contracts import SignalLedgerRecord,LedgerSnapshot
from .enums import *

def materialize(config,signals,gate_by_signal,eligibility_by_signal,decisions,events,created_utc_ms):
    decision_by_signal={}
    reservations=[]
    for d in decisions:
        if d.reservation: reservations.append(d.reservation)
        if d.winner_signal_id: decision_by_signal[d.winner_signal_id]=(d,LedgerDisposition.QUOTA_WINNER)
        for sid in d.suppressed_signal_ids:
            # WW suppression is determined from eligibility, otherwise quota.
            e=eligibility_by_signal.get(sid)
            disp=LedgerDisposition.SUPPRESSED_BY_WW if e and e.gate_eligibility.value=="SUPPRESSED" else LedgerDisposition.SUPPRESSED_BY_QUOTA
            decision_by_signal[sid]=(d,disp)
        for sid in d.blocked_signal_ids: decision_by_signal[sid]=(d,LedgerDisposition.BLOCKED)
    event_seq_by_signal=defaultdict(list)
    for e in events:
        if e.signal_id: event_seq_by_signal[e.signal_id].append(e.sequence)
    records=[]
    for s in sorted(signals,key=lambda x:x.signal_id):
        gate=gate_by_signal[s.signal_id]; elig=eligibility_by_signal[s.signal_id]
        d,disp=decision_by_signal.get(s.signal_id,(None,LedgerDisposition.OBSERVED))
        winner=d.winner_signal_id if d else ""; res=d.reservation.reservation_id if d and d.reservation and winner==s.signal_id else ""
        qid=d.quota_key.quota_key_id if d else ""
        reasons=tuple(sorted(set(elig.reason_codes + (("FP_LDG_QUOTA_WINNER",) if disp is LedgerDisposition.QUOTA_WINNER else ()) + (("FP_LDG_SUPPRESSED_BY_QUOTA",) if disp is LedgerDisposition.SUPPRESSED_BY_QUOTA else ()))))
        seqs=event_seq_by_signal.get(s.signal_id,[0]); p={"signal_id":s.signal_id,"gate_decision_id":gate.decision_id,"eligibility_id":elig.evidence_id,"disposition":disp.value,"quota_key_id":qid,"winner_signal_id":winner,"reservation_id":res,"reason_codes":reasons,"first_event_sequence":min(seqs),"last_event_sequence":max(seqs)}
        h=canonical_sha256(p); records.append(SignalLedgerRecord(stable_id("FPLR",p),s,gate,elig,disp,qid,winner,res,reasons,min(seqs),max(seqs),h))
    signal_index=tuple((r.signal.signal_id,i) for i,r in enumerate(records))
    session=defaultdict(list); relation=defaultdict(list)
    for r in records:
        session[r.signal.owner_session_id].append(r.signal.signal_id); relation[r.signal.relation.value].append(r.signal.signal_id)
    session_index=tuple((k,tuple(sorted(v))) for k,v in sorted(session.items())); relation_index=tuple((k,tuple(sorted(v))) for k,v in sorted(relation.items()))
    head=events[-1].event_hash if events else ""
    p={"config_hash":config.config_hash,"event_ids":[e.event_id for e in events],"record_hashes":[r.record_hash for r in records],"decision_hashes":[d.decision_hash for d in decisions],"reservation_hashes":[r.reservation_hash for r in reservations],"chain_head_hash":head,"signal_index":signal_index,"session_index":session_index,"relation_index":relation_index,"created_utc_ms":created_utc_ms}
    h=canonical_sha256(p); return LedgerSnapshot(stable_id("FPLS",p),config.config_hash,tuple(events),tuple(records),tuple(decisions),tuple(reservations),head,signal_index,session_index,relation_index,EngineHealth.READY,(),created_utc_ms,h)
