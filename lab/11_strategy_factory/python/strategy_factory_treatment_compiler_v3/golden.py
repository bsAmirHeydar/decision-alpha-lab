from __future__ import annotations
from decimal import Decimal
from strategy_factory_treatments_v3.catalog import build_default_catalog
from strategy_factory_treatments_v3.enums import TradeSide,RuntimeMode,TreatmentKind
from strategy_factory_treatments_v3.fixtures import reference_context
from .contracts import *
from .enums import *
from .compiler import TreatmentCompiler
from .state_machine import CausalPathStateMachine

def baseline_draft(side=TradeSide.LONG):
    S=AtomSelection; K=TreatmentKind
    return TreatmentDraft('golden.fixed_r',side,RuntimeMode.RESEARCH,CompilerMode.RESEARCH,(
      S(K.ENTRY,'entry.immediate_market@1.0.0',{'max_age_ms':2000}),
      S(K.STOP,'stop.fixed_distance@1.0.0',{'distance_points':'100'}),
      S(K.TARGET,'target.fixed_r@1.0.0',{'reward_multiple':'2','risk_points':'100'}),
      S(K.TRAILING,'trailing.none@1.0.0',{}),
      S(K.MANAGEMENT,'management.max_holding_time@1.0.0',{'holding_ms':14400000}),
      S(K.SIZING,'sizing.fixed_cash@1.0.0',{'cash_amount':'100'}),
    ),IntrabarPolicy(max_quote_age_ms=100000000))

def runner_draft(side=TradeSide.LONG):
    S=AtomSelection; K=TreatmentKind
    return TreatmentDraft('golden.runner',side,RuntimeMode.RESEARCH,CompilerMode.RESEARCH,(
      S(K.ENTRY,'entry.retest_limit@1.0.0',{'offset_points':'0','ttl_ms':600000}),
      S(K.STOP,'stop.structural@1.0.0',{'buffer_points':'2'}),
      S(K.TARGET,'target.runner@1.0.0',{'runner_fraction':'1'}),
      S(K.TRAILING,'trailing.swing_node@1.0.0',{'activation_r':'1','buffer_points':'2'}),
      S(K.MANAGEMENT,'management.partial_exit_r@1.0.0',{'activation_r':'1','quantity_fraction':'0.5'}),
      S(K.MANAGEMENT,'management.session_close@1.0.0',{'lead_ms':300000}),
      S(K.SIZING,'sizing.equity_fraction@1.0.0',{'fraction':'0.01'}),
    ),IntrabarPolicy(ambiguity=AmbiguityPolicy.WORST_CASE,max_quote_age_ms=100000000))

def compile_golden(side=TradeSide.LONG,runner=False):
    c=TreatmentCompiler(build_default_catalog()); ctx=reference_context(side); return c.compile(runner_draft(side) if runner else baseline_draft(side),ctx)

def path_scenarios(treatment):
    t=treatment.decision_time_ms; p=treatment.entry.legs[0].trigger_price; q=Decimal
    return {
      'market_target':(
       PathEvent(1,PathEventType.SUBMIT,t,t),PathEvent(2,PathEventType.FILL,t+1,t+1,p,q('1'),'golden'),PathEvent(3,PathEventType.TARGET_HIT,t+2,t+2,p+q('2'),q('1'),'golden'),PathEvent(4,PathEventType.CLOSE,t+3,t+3,p+q('2'),q('0'),'golden')),
      'market_stop':(
       PathEvent(1,PathEventType.SUBMIT,t,t),PathEvent(2,PathEventType.FILL,t+1,t+1,p,q('1'),'golden'),PathEvent(3,PathEventType.STOP_HIT,t+2,t+2,p-q('1'),q('1'),'golden'),PathEvent(4,PathEventType.CLOSE,t+3,t+3,p-q('1'),q('0'),'golden')),
      'partial_trail_close':(
       PathEvent(1,PathEventType.SUBMIT,t,t),PathEvent(2,PathEventType.FILL,t+1,t+1,p,q('1'),'golden'),PathEvent(3,PathEventType.PARTIAL_EXIT,t+2,t+2,p+q('1'),q('0.5'),'golden'),PathEvent(4,PathEventType.TRAIL_UPDATE,t+3,t+3,p+q('0.2'),q('0'),'golden','',{'side':treatment.side.value}),PathEvent(5,PathEventType.CLOSE,t+4,t+4,p+q('1.5'),q('0.5'),'golden')),
      'pending_cancel':(PathEvent(1,PathEventType.SUBMIT,t,t),PathEvent(2,PathEventType.CANCEL,t+1,t+1,None,q('0'),'golden','expired'),PathEvent(3,PathEventType.CLOSE,t+2,t+2,None,q('0'),'golden')),
      'partial_fill_timeout':(PathEvent(1,PathEventType.SUBMIT,t,t),PathEvent(2,PathEventType.FILL,t+1,t+1,p,q('0.4'),'golden'),PathEvent(3,PathEventType.TIMEOUT,t+2,t+2,p,q('0.4'),'golden','time_exit'),PathEvent(4,PathEventType.CLOSE,t+3,t+3,p,q('0'),'golden')),
    }

def run_golden_paths():
    treatment,_=compile_golden(); sm=CausalPathStateMachine(); out={}
    for name,events in path_scenarios(treatment).items(): out[name]=sm.replay(treatment,events).to_dict()
    return treatment.to_dict(),out
