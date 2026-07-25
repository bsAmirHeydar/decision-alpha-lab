from __future__ import annotations
from decimal import Decimal
from .contracts import ReservationEvent,ReservationRecord
from .enums import LedgerAction,ReservationState
from .errors import ReservationError
from .utils import dec,stable_id
class ReservationLedger:
    GENESIS='0'*64
    def __init__(self): self.events=[]; self.records={}; self._idempotency={}
    @property
    def head_hash(self): return self.events[-1].event_hash if self.events else self.GENESIS
    @property
    def total_open_cash(self): return sum((r.open_cash for r in self.records.values()),Decimal('0'))
    def _append(self,action,reservation_id,account_id,treatment_id,symbol,strategy_id,group,amount,event_time_ms,known_time_ms,reason='',metadata=None,idempotency_key=''):
        amount=dec(amount)
        if amount<0: raise ReservationError('negative_ledger_amount','ledger amount cannot be negative')
        if known_time_ms<event_time_ms: raise ReservationError('known_time_violation','known time before event time')
        if idempotency_key and idempotency_key in self._idempotency: return self.events[self._idempotency[idempotency_key]]
        e=ReservationEvent(len(self.events)+1,action,reservation_id,account_id,treatment_id,symbol,strategy_id,group,amount,event_time_ms,known_time_ms,self.head_hash,reason,metadata or {})
        self._apply(e); self.events.append(e)
        if idempotency_key: self._idempotency[idempotency_key]=len(self.events)-1
        return e
    def _apply(self,e):
        r=self.records.get(e.reservation_id)
        if e.action is LedgerAction.RESERVE:
            if r is not None: raise ReservationError('duplicate_reservation','reservation already exists')
            self.records[e.reservation_id]=ReservationRecord(e.reservation_id,e.account_id,e.treatment_id,e.symbol,e.strategy_id,e.correlation_group,e.amount_cash,Decimal('0'),Decimal('0'),ReservationState.RESERVED,e.sequence,e.event_hash); return
        if r is None: raise ReservationError('missing_reservation','reservation not found')
        reserved,consumed,released=r.reserved_cash,r.consumed_cash,r.released_cash
        if e.action is LedgerAction.ADJUST:
            if e.amount_cash<consumed+released: raise ReservationError('adjust_below_used','cannot reduce reservation below consumed/released')
            reserved=e.amount_cash; state=ReservationState.ADJUSTED
        elif e.action is LedgerAction.CONSUME:
            if e.amount_cash>r.open_cash: raise ReservationError('consume_exceeds_open','consume exceeds open reservation')
            consumed+=e.amount_cash; state=ReservationState.CONSUMED if consumed+released>=reserved else ReservationState.PARTIALLY_CONSUMED
        elif e.action in (LedgerAction.RELEASE,LedgerAction.CANCEL):
            if e.amount_cash>r.open_cash: raise ReservationError('release_exceeds_open','release exceeds open reservation')
            released+=e.amount_cash; state=ReservationState.CANCELLED if e.action is LedgerAction.CANCEL and consumed==0 else ReservationState.RELEASED if consumed+released>=reserved else ReservationState.ADJUSTED
        elif e.action is LedgerAction.RECONCILE:
            if e.amount_cash<consumed: raise ReservationError('reconcile_below_consumed','reconciled reserved amount below consumed')
            reserved=e.amount_cash; released=max(released,reserved-consumed); state=ReservationState.RECONCILED
        self.records[e.reservation_id]=ReservationRecord(r.reservation_id,r.account_id,r.treatment_id,r.symbol,r.strategy_id,r.correlation_group,reserved,consumed,released,state,e.sequence,e.event_hash)
    def reserve(self,envelope,account_id,strategy_id,group,event_time_ms,known_time_ms,idempotency_key=''):
        rid=stable_id('uceriskres',{'envelope_id':envelope.envelope_id,'account_id':account_id,'strategy_id':strategy_id,'group':group})
        return self._append(LedgerAction.RESERVE,rid,account_id,envelope.treatment_id,envelope.metadata.get('symbol','') if envelope.metadata else '',strategy_id,group,envelope.maximum_loss_cash,event_time_ms,known_time_ms,'pre_intent_reservation',{'envelope_id':envelope.envelope_id},idempotency_key)
    def adjust(self,rid,new_total,event_time_ms,known_time_ms,reason='fill_adjustment'): r=self.records[rid]; return self._append(LedgerAction.ADJUST,rid,r.account_id,r.treatment_id,r.symbol,r.strategy_id,r.correlation_group,new_total,event_time_ms,known_time_ms,reason)
    def consume(self,rid,amount,event_time_ms,known_time_ms,reason='fill_consumption'): r=self.records[rid]; return self._append(LedgerAction.CONSUME,rid,r.account_id,r.treatment_id,r.symbol,r.strategy_id,r.correlation_group,amount,event_time_ms,known_time_ms,reason)
    def release(self,rid,amount,event_time_ms,known_time_ms,reason='release'): r=self.records[rid]; return self._append(LedgerAction.RELEASE,rid,r.account_id,r.treatment_id,r.symbol,r.strategy_id,r.correlation_group,amount,event_time_ms,known_time_ms,reason)
    def replay(self,events):
        self.events=[]; self.records={}; self._idempotency={}; prior=self.GENESIS
        for e in events:
            if e.prior_hash!=prior: raise ReservationError('hash_chain_break','reservation ledger hash chain mismatch',{'sequence':e.sequence})
            self._apply(e); self.events.append(e); prior=e.event_hash
        return self
    def snapshot(self): return {'head_hash':self.head_hash,'total_open_cash':str(self.total_open_cash),'records':[self.records[k].to_dict() for k in sorted(self.records)]}
