from __future__ import annotations
from .models import AdapterDescriptor
from .enums import *
from .errors import CompatibilityError

CATALOG=(
 AdapterDescriptor('FP_CGT_TIME_ADAPTER','1.0.0',SourceContext.EXP0017,'SCGTTimeSnapshot',AdapterFamily.TIME,ReuseMode.ADAPTER,'CGT_TIME_CORE',('broker_now','utc_now','new_york_now','trading_day_start_ny','trading_day_end_ny','inside_trading_day','new_york_utc_offset_hours','trading_day_label'),('broker_time','utc_time','new_york_time','trading_day_start_ny','trading_day_end_ny','inside_trading_day','ny_utc_offset_hours','trading_day_key'),('Renames fields into context-neutral vocabulary.',)),
 AdapterDescriptor('FP_CGR_REFERENCE_ADAPTER','1.0.0',SourceContext.EXP0017,'SCGRReferencePair',AdapterFamily.REFERENCE,ReuseMode.ADAPTER,'CGR_REFERENCE_CORE',('group_name','reference_cycle_index','cycle_start_ny','cycle_end_ny','complete_cycle','ready','symbol_a','symbol_b'),('reference_id','window_code','window_start','window_end','complete','ready','symbol-local prices/times'),('Creates a neutral reference_id; does not change prices.',)),
 AdapterDescriptor('FP_CGH_HUNT_ADAPTER','1.0.0',SourceContext.EXP0017,'SCGHReferenceHuntState',AdapterFamily.HUNT,ReuseMode.ADAPTER,'CGH_HUNT_CORE',('group_name','reference_cycle_index','reference_cycle_start_ny','current_cycle_start_ny','symbol_a','symbol_b'),('observation_id','reference_id','side','pair_state','hunter/protected','prices/extremes'),('Normalizes pair-state names; preserves touch semantics.',)),
 AdapterDescriptor('FP_CGD_DIVERGENCE_ADAPTER','1.0.0',SourceContext.EXP0017,'SCGDDivergenceCandidate',AdapterFamily.DIVERGENCE,ReuseMode.ADAPTER,'CGD_DIVERGENCE_CORE',('divergence_id','direction','side','hunter_symbol','clean_symbol','data_ready'),('candidate_id','direction','side','hunter/protected','health'),('Maps BUY/SELL to BULLISH/BEARISH labels only.',)),
 AdapterDescriptor('FP_CGC_CONFIRMATION_ADAPTER','1.0.0',SourceContext.EXP0017,'SCGCFinalSignal',AdapterFamily.CONFIRMATION,ReuseMode.ADAPTER,'CGC_CONFIRMATION_CORE',('signal_id','status','direction','side','confirmation_time_utc','confirmation_timeframe_seconds'),('result_id','outcome','host close','immutable/replay flags'),('Projects final CG state; does not apply FP session policy.',)),
 AdapterDescriptor('FP_DAYE_HUNT_ADAPTER','1.0.0',SourceContext.EXP0018,'DAYE_HuntObservation',AdapterFamily.HUNT,ReuseMode.ADAPTER,'DAYE_HUNT_CORE',('observation_id','opportunity_id','relationship_id','side','pair_state','hunter_canonical_symbol','protected_canonical_symbol'),('observation_id','reference/opportunity','side','pair state','roles','timestamps'),('Drops Daye relationship family from neutral output; retains source fingerprint.',)),
 AdapterDescriptor('FP_DAYE_CONFIRMATION_ADAPTER','1.0.0',SourceContext.EXP0018,'DAYE_ConfirmationResult',AdapterFamily.CONFIRMATION,ReuseMode.ADAPTER,'DAYE_CONFIRMATION_CORE',('result_id','candidate_id','outcome','side','host_bar_open_utc','host_bar_close_utc'),('result/outcome/direction/roles/host boundary/immutability'),('Derives direction from side; does not decide FP eligibility.',)),
 AdapterDescriptor('FP_DAYE_LIFECYCLE_ADAPTER','1.0.0',SourceContext.EXP0018,'DAYE_ReferenceLifecycleRecord',AdapterFamily.LIFECYCLE,ReuseMode.ADAPTER,'DAYE_LIFECYCLE_CORE',('reference_id','side','protected_canonical_symbol','first_hunter_canonical_symbol','state','is_retired'),('reference/state/roles/use counts/timestamps'),('Projects lifecycle evidence without changing retirement policy.',)),
)

class AdapterRegistry:
    def __init__(self): self._items={};self._frozen=False
    def register(self,d):
        if self._frozen: raise CompatibilityError('registry_frozen','registry is frozen')
        if d.key in self._items: raise CompatibilityError('duplicate_adapter_key',d.key)
        self._items[d.key]=d
    def freeze(self): self._frozen=True
    def resolve(self,key):
        if key not in self._items: raise CompatibilityError('adapter_not_registered',key)
        return self._items[key]
    def snapshot(self): return tuple(self._items[k] for k in sorted(self._items))

def default_registry():
    r=AdapterRegistry()
    for d in CATALOG:r.register(d)
    r.freeze();return r
