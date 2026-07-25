from __future__ import annotations
from dataclasses import replace
from decimal import Decimal
from .contracts import PathSnapshot,PathEvent,CompiledTreatment
from .enums import PathState,PathEventType
from .errors import PathTransitionError
from .utils import dec

_ALLOWED={
 PathState.DRAFT:{PathEventType.SUBMIT:PathState.PENDING,PathEventType.REJECT:PathState.REJECTED},
 PathState.PENDING:{PathEventType.TRIGGER:PathState.TRIGGERED,PathEventType.FILL:PathState.PARTIALLY_FILLED,PathEventType.CANCEL:PathState.CANCELED,PathEventType.TIMEOUT:PathState.TIMED_OUT,PathEventType.REJECT:PathState.REJECTED},
 PathState.TRIGGERED:{PathEventType.FILL:PathState.PARTIALLY_FILLED,PathEventType.CANCEL:PathState.CANCELED,PathEventType.TIMEOUT:PathState.TIMED_OUT,PathEventType.REJECT:PathState.REJECTED},
 PathState.PARTIALLY_FILLED:{PathEventType.FILL:PathState.PARTIALLY_FILLED,PathEventType.SCALE:PathState.SCALED,PathEventType.PARTIAL_EXIT:PathState.PARTIALLY_EXITED,PathEventType.STOP_HIT:PathState.STOPPED,PathEventType.TARGET_HIT:PathState.TARGETED,PathEventType.TRAIL_UPDATE:PathState.TRAILED,PathEventType.CANCEL:PathState.PARTIALLY_FILLED,PathEventType.TIMEOUT:PathState.TIMED_OUT,PathEventType.CLOSE:PathState.CLOSED},
 PathState.OPEN:{PathEventType.SCALE:PathState.SCALED,PathEventType.PARTIAL_EXIT:PathState.PARTIALLY_EXITED,PathEventType.TRAIL_UPDATE:PathState.TRAILED,PathEventType.STOP_HIT:PathState.STOPPED,PathEventType.TARGET_HIT:PathState.TARGETED,PathEventType.TIMEOUT:PathState.TIMED_OUT,PathEventType.CLOSE:PathState.CLOSED},
 PathState.SCALED:{PathEventType.SCALE:PathState.SCALED,PathEventType.PARTIAL_EXIT:PathState.PARTIALLY_EXITED,PathEventType.TRAIL_UPDATE:PathState.TRAILED,PathEventType.STOP_HIT:PathState.STOPPED,PathEventType.TARGET_HIT:PathState.TARGETED,PathEventType.TIMEOUT:PathState.TIMED_OUT,PathEventType.CLOSE:PathState.CLOSED},
 PathState.PARTIALLY_EXITED:{PathEventType.PARTIAL_EXIT:PathState.PARTIALLY_EXITED,PathEventType.TRAIL_UPDATE:PathState.TRAILED,PathEventType.SCALE:PathState.SCALED,PathEventType.STOP_HIT:PathState.STOPPED,PathEventType.TARGET_HIT:PathState.TARGETED,PathEventType.TIMEOUT:PathState.TIMED_OUT,PathEventType.CLOSE:PathState.CLOSED},
 PathState.TRAILED:{PathEventType.TRAIL_UPDATE:PathState.TRAILED,PathEventType.PARTIAL_EXIT:PathState.PARTIALLY_EXITED,PathEventType.STOP_HIT:PathState.STOPPED,PathEventType.TARGET_HIT:PathState.TARGETED,PathEventType.TIMEOUT:PathState.TIMED_OUT,PathEventType.CLOSE:PathState.CLOSED},
 PathState.STOPPED:{PathEventType.CLOSE:PathState.CLOSED},PathState.TARGETED:{PathEventType.CLOSE:PathState.CLOSED},PathState.TIMED_OUT:{PathEventType.CLOSE:PathState.CLOSED},PathState.CANCELED:{PathEventType.CLOSE:PathState.CLOSED},PathState.REJECTED:{PathEventType.CLOSE:PathState.CLOSED},PathState.CLOSED:{}
}
class CausalPathStateMachine:
    def initial(self,treatment:CompiledTreatment)->PathSnapshot:
        return PathSnapshot(treatment.treatment_id,PathState.DRAFT,0,treatment.decision_time_ms,treatment.decision_time_ms,active_stop_price=treatment.stop.stop_price)
    def apply(self,s:PathSnapshot,e:PathEvent)->PathSnapshot:
        if e.sequence!=s.last_sequence+1: raise PathTransitionError('sequence_gap','event sequence must be contiguous',{'expected':s.last_sequence+1,'actual':e.sequence})
        if e.event_time_ms<s.last_event_time_ms: raise PathTransitionError('event_time_regression','event time regressed')
        if e.known_time_ms<s.last_known_time_ms: raise PathTransitionError('known_time_regression','known time regressed')
        if e.known_time_ms<e.event_time_ms: raise PathTransitionError('future_knowledge','known time precedes event time')
        if e.event_type not in _ALLOWED[s.state]: raise PathTransitionError('illegal_transition',f'{s.state.value} cannot accept {e.event_type.value}')
        ns=_ALLOWED[s.state][e.event_type]; filled=s.filled_fraction; openf=s.open_fraction; exited=s.exited_fraction; avg=s.average_entry_price; trail=s.last_trail_price; reason=s.terminal_reason
        qty=max(Decimal('0'),dec(e.quantity_fraction))
        if e.event_type in (PathEventType.FILL,PathEventType.SCALE):
            if qty<=0: raise PathTransitionError('nonpositive_fill','fill quantity must be positive')
            if filled+qty>Decimal('1.0000000001'): raise PathTransitionError('overfill','filled fraction exceeds one')
            old_notional=(avg or Decimal('0'))*openf; filled+=qty; openf+=qty
            if e.price is not None: avg=(old_notional+dec(e.price)*qty)/openf
            if filled>=Decimal('0.9999999999') and ns is PathState.PARTIALLY_FILLED: ns=PathState.OPEN
        elif e.event_type is PathEventType.PARTIAL_EXIT:
            if qty<=0 or qty>=openf+Decimal('0.0000000001'): raise PathTransitionError('invalid_partial_exit','partial exit must be positive and no greater than open fraction')
            openf-=qty; exited+=qty
            if openf<=Decimal('0.0000000001'): ns=PathState.CLOSED; reason=e.reason or 'fully_exited'
        elif e.event_type in (PathEventType.STOP_HIT,PathEventType.TARGET_HIT,PathEventType.TIMEOUT,PathEventType.CLOSE):
            exited+=openf; openf=Decimal('0'); reason=e.reason or e.event_type.value
        elif e.event_type is PathEventType.TRAIL_UPDATE:
            if e.price is None: raise PathTransitionError('missing_trail_price','trail update requires price')
            trail=dec(e.price)
            if s.last_trail_price is not None:
                direction=e.metadata.get('side','')
                if direction=='long' and trail<s.last_trail_price: raise PathTransitionError('trail_loosened','long trail cannot move down')
                if direction=='short' and trail>s.last_trail_price: raise PathTransitionError('trail_loosened','short trail cannot move up')
        terminal=ns in (PathState.STOPPED,PathState.TARGETED,PathState.TIMED_OUT,PathState.CANCELED,PathState.REJECTED,PathState.CLOSED)
        if terminal and not reason: reason=e.reason or ns.value
        return PathSnapshot(s.treatment_id,ns,e.sequence,e.event_time_ms,e.known_time_ms,filled,openf,exited,avg,s.active_stop_price,trail,reason,s.transition_count+1)
    def replay(self,treatment,events):
        s=self.initial(treatment)
        for e in events:s=self.apply(s,e)
        return s
