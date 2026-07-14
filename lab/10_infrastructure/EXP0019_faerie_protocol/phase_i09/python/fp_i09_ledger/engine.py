from __future__ import annotations
from collections import defaultdict
from .store import AppendOnlyLedger
from .events import LedgerEventType
from .identity import build_contender
from .arbiter import resolve_pair_session
from .eligibility import evaluate_eligibility
from .materialize import materialize
from .enums import *

class LedgerEngine:
    def __init__(self,config):
        self.config=config; self.ledger=AppendOnlyLedger(); self.signals={}; self.gates={}; self.eligibility={}; self.contenders=defaultdict(dict); self.decisions={}
    def ingest(self,signal,gate,eligibility,quota_key,occurred_utc_ms,seal_state=SessionSealState.OPEN):
        _,fresh=self.ledger.ingest_signal(signal,occurred_utc_ms)
        if fresh:
            self.signals[signal.signal_id]=signal; self.gates[signal.signal_id]=gate; self.eligibility[signal.signal_id]=eligibility
            self.ledger.append_fact(LedgerEventType.GATE_DECISION_ATTACHED,signal.signal_id,occurred_utc_ms,{"gate_decision_id":gate.decision_id},signal_id=signal.signal_id,quota_key_id=quota_key.quota_key_id,reason_code="FP_LDG_GATE_DECISION_ATTACHED")
            out=evaluate_eligibility(eligibility)
            self.ledger.append_fact(LedgerEventType.ELIGIBILITY_EVALUATED,signal.signal_id,occurred_utc_ms,{"eligibility_id":eligibility.evidence_id,"outcome":out.value},signal_id=signal.signal_id,quota_key_id=quota_key.quota_key_id,reason_code=f"FP_LDG_{out.value}")
            c=build_contender(signal,quota_key,eligibility); self.contenders[quota_key.quota_key_id][signal.signal_id]=c
            self.ledger.append_fact(LedgerEventType.CONTENDER_REGISTERED,c.contender_id,occurred_utc_ms,{"contender_id":c.contender_id,"rank_key":c.rank_key},signal_id=signal.signal_id,quota_key_id=quota_key.quota_key_id,reason_code="FP_LDG_CONTENDER_REGISTERED")
        prior=self.decisions.get(quota_key.quota_key_id)
        d=resolve_pair_session(quota_key,tuple(self.contenders[quota_key.quota_key_id].values()),evaluated_utc_ms=occurred_utc_ms,seal_state=seal_state,prior_reservation=prior.reservation if prior else None)
        changed=not prior or prior.decision_hash!=d.decision_hash
        self.decisions[quota_key.quota_key_id]=d
        if changed and d.reservation:
            typ=LedgerEventType.QUOTA_RESERVED if not prior or not prior.reservation else (LedgerEventType.RESERVATION_SUPERSEDED if prior.reservation.winner_signal_id!=d.reservation.winner_signal_id else LedgerEventType.QUOTA_RESERVED)
            self.ledger.append_fact(typ,d.reservation.reservation_id,occurred_utc_ms,{"reservation_id":d.reservation.reservation_id,"winner_signal_id":d.winner_signal_id,"generation":d.reservation.generation},signal_id=d.winner_signal_id,quota_key_id=quota_key.quota_key_id,reason_code=d.reservation.reason_code)
        return d
    def seal(self,quota_key,occurred_utc_ms):
        prior=self.decisions.get(quota_key.quota_key_id)
        d=resolve_pair_session(quota_key,tuple(self.contenders[quota_key.quota_key_id].values()),evaluated_utc_ms=occurred_utc_ms,seal_state=SessionSealState.SEALED,prior_reservation=prior.reservation if prior else None)
        self.decisions[quota_key.quota_key_id]=d
        self.ledger.append_fact(LedgerEventType.SESSION_SEALED,quota_key.quota_key_id,occurred_utc_ms,{"decision_id":d.decision_id,"winner_signal_id":d.winner_signal_id},signal_id=d.winner_signal_id,quota_key_id=quota_key.quota_key_id,reason_code="FP_LDG_SESSION_SEALED")
        return d
    def snapshot(self,created_utc_ms):
        return materialize(self.config,tuple(self.signals.values()),self.gates,self.eligibility,tuple(self.decisions[k] for k in sorted(self.decisions)),self.ledger.events,created_utc_ms)
