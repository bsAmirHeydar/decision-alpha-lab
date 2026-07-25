import pytest
from decimal import Decimal
from strategy_factory_treatment_compiler_v3.golden import compile_golden
from strategy_factory_treatment_compiler_v3.state_machine import CausalPathStateMachine
from strategy_factory_treatment_compiler_v3.intrabar import IntrabarResolver
from strategy_factory_treatment_compiler_v3.contracts import PathEvent,BarObservation,TreatmentDraft
from strategy_factory_treatment_compiler_v3.enums import PathEventType,AmbiguityPolicy
from strategy_factory_treatment_compiler_v3.errors import PathTransitionError
def open_snapshot(t):
 sm=CausalPathStateMachine(); p=t.entry.legs[0].trigger_price; s=sm.initial(t); s=sm.apply(s,PathEvent(1,PathEventType.SUBMIT,t.decision_time_ms,t.decision_time_ms)); return sm.apply(s,PathEvent(2,PathEventType.FILL,t.decision_time_ms+1,t.decision_time_ms+1,p,Decimal('1')))
def test_worst_case_resolves_stop_first():
 t,_=compile_golden(); s=open_snapshot(t); stop=s.active_stop_price; target=t.target.legs[0].target_price
 bar=BarObservation(t.decision_time_ms+2,t.decision_time_ms+100,Decimal('100'),max(target,Decimal('102')),min(stop,Decimal('98')),Decimal('100'),t.decision_time_ms+100)
 ev=IntrabarResolver().resolve(t,s,bar,3); assert ev[0].event_type is PathEventType.STOP_HIT
def test_reject_ambiguous_policy():
 t,_=compile_golden(); p=t.intrabar_policy; from dataclasses import replace
 t=replace(t,intrabar_policy=replace(p,ambiguity=AmbiguityPolicy.REJECT)); s=open_snapshot(t); stop=s.active_stop_price; target=t.target.legs[0].target_price
 bar=BarObservation(t.decision_time_ms+2,t.decision_time_ms+100,Decimal('100'),target+1,stop-1,Decimal('100'),t.decision_time_ms+100)
 with pytest.raises(PathTransitionError): IntrabarResolver().resolve(t,s,bar,3)
