"""Pure read-only adapter functions from shared-core snapshots into neutral FP contracts."""
from __future__ import annotations
from copy import deepcopy
from typing import Any, Mapping
from .canonical import canonical_sha256
from .enums import *
from .errors import CompatibilityError
from .models import *

def _required(payload:Mapping[str,Any],fields:tuple[str,...],adapter_id:str):
    missing=[f for f in fields if f not in payload]
    if missing: raise CompatibilityError('missing_adapter_fields',f'{adapter_id} missing fields',{'missing':missing})

def _health(ready:bool,available:bool=True):
    if ready:return HealthState.READY
    return HealthState.DEGRADED if available else HealthState.BLOCKED

def adapt_cgt_time(payload:Mapping[str,Any])->CanonicalTimeSnapshot:
    fields=('broker_now','utc_now','new_york_now','trading_day_start_ny','trading_day_end_ny','inside_trading_day','new_york_utc_offset_hours','trading_day_label')
    _required(payload,fields,'FP_CGT_TIME_ADAPTER')
    source=canonical_sha256(payload)
    return CanonicalTimeSnapshot(SourceContext.EXP0017,'SCGTTimeSnapshot',source,int(payload['broker_now']),int(payload['utc_now']),int(payload['new_york_now']),int(payload['trading_day_start_ny']),int(payload['trading_day_end_ny']),bool(payload['inside_trading_day']),int(payload['new_york_utc_offset_hours']),str(payload['trading_day_label']),HealthState.READY,'CGT_SNAPSHOT_ADAPTED')

def adapt_cgr_reference(payload:Mapping[str,Any])->CanonicalReferencePair:
    fields=('group_name','reference_cycle_index','cycle_start_ny','cycle_end_ny','complete_cycle','ready','symbol_a','symbol_b')
    _required(payload,fields,'FP_CGR_REFERENCE_ADAPTER'); a=payload['symbol_a'];b=payload['symbol_b']
    for side in (a,b):_required(side,('symbol','data_ok','high','low','high_time_broker','low_time_broker'),'FP_CGR_REFERENCE_ADAPTER')
    source=canonical_sha256(payload); ready=bool(payload['ready']) and bool(a['data_ok']) and bool(b['data_ok'])
    rid=f"CGR:{payload['group_name']}:{payload['reference_cycle_index']}:{payload['cycle_start_ny']}"
    return CanonicalReferencePair(SourceContext.EXP0017,'SCGRReferencePair',source,rid,str(payload['group_name']),int(payload['cycle_start_ny']),int(payload['cycle_end_ny']),bool(payload['complete_cycle']),ready,str(a['symbol']),str(b['symbol']),float(a['high']),float(a['low']),float(b['high']),float(b['low']),int(a['high_time_broker']),int(a['low_time_broker']),int(b['high_time_broker']),int(b['low_time_broker']),bool(a['data_ok']),bool(b['data_ok']),_health(ready,bool(a['data_ok']) or bool(b['data_ok'])),'CGR_REFERENCE_ADAPTED' if ready else 'CGR_REFERENCE_NOT_READY')

def adapt_cgh_hunt(payload:Mapping[str,Any])->CanonicalHuntObservation:
    fields=('group_name','reference_cycle_index','reference_cycle_start_ny','current_cycle_start_ny','symbol_a','symbol_b','reference_ready','current_range_ready')
    _required(payload,fields,'FP_CGH_HUNT_ADAPTER');a=payload['symbol_a'];b=payload['symbol_b']
    for side in (a,b):_required(side,('symbol','reference_high','reference_low','current_high','current_low','high_hunted','low_hunted'),'FP_CGH_HUNT_ADAPTER')
    high_a,high_b=bool(a['high_hunted']),bool(b['high_hunted']);low_a,low_b=bool(a['low_hunted']),bool(b['low_hunted'])
    side=HuntSide.HIGH if high_a or high_b else HuntSide.LOW if low_a or low_b else HuntSide.NONE
    ah=high_a if side is HuntSide.HIGH else low_a; bh=high_b if side is HuntSide.HIGH else low_b
    pair=PairState.BOTH if ah and bh else PairState.A_ONLY if ah else PairState.B_ONLY if bh else PairState.NONE
    hunter=str(a['symbol']) if pair is PairState.A_ONLY else str(b['symbol']) if pair is PairState.B_ONLY else ''
    protected=str(b['symbol']) if pair is PairState.A_ONLY else str(a['symbol']) if pair is PairState.B_ONLY else ''
    ready=bool(payload['reference_ready']) and bool(payload['current_range_ready'])
    source=canonical_sha256(payload);rid=f"CGR:{payload['group_name']}:{payload['reference_cycle_index']}:{payload['reference_cycle_start_ny']}";oid=f"CGH:{rid}:{payload['current_cycle_start_ny']}:{side.value}"
    refa=float(a['reference_high'] if side is HuntSide.HIGH else a['reference_low'] if side is HuntSide.LOW else 0.0);refb=float(b['reference_high'] if side is HuntSide.HIGH else b['reference_low'] if side is HuntSide.LOW else 0.0)
    exta=float(a['current_high'] if side is HuntSide.HIGH else a['current_low'] if side is HuntSide.LOW else 0.0);extb=float(b['current_high'] if side is HuntSide.HIGH else b['current_low'] if side is HuntSide.LOW else 0.0)
    return CanonicalHuntObservation(SourceContext.EXP0017,'SCGHReferenceHuntState',source,oid,rid,str(payload['current_cycle_start_ny']),side,pair,hunter,protected,refa,refb,exta,extb,int(payload.get('event_time_utc',payload['current_cycle_start_ny'])),int(payload.get('availability_time_utc',payload['current_cycle_start_ny'])),True,_health(ready),'CGH_HUNT_ADAPTED' if ready else 'CGH_HUNT_NOT_READY')

def adapt_cgd_candidate(payload:Mapping[str,Any])->CanonicalDivergenceCandidate:
    fields=('divergence_id','group_name','reference_cycle_index','current_cycle_index','direction','side','hunter_symbol','clean_symbol','one_sided_hunt','both_symbols_hunted_same_side','data_ready','hunter_reference_price','clean_reference_price','current_cycle_start_ny','reference_cycle_start_ny')
    _required(payload,fields,'FP_CGD_DIVERGENCE_ADAPTER')
    direction=Direction.BULLISH if str(payload['direction']).upper() in ('BUY','BULLISH','1') or payload['direction']==1 else Direction.BEARISH if str(payload['direction']).upper() in ('SELL','BEARISH','2') or payload['direction']==2 else Direction.NONE
    side=HuntSide.LOW if str(payload['side']).upper() in ('LOW','1') or payload['side']==1 else HuntSide.HIGH if str(payload['side']).upper() in ('HIGH','2') or payload['side']==2 else HuntSide.NONE
    source=canonical_sha256(payload);rid=f"CGR:{payload['group_name']}:{payload['reference_cycle_index']}:{payload['reference_cycle_start_ny']}";opp=str(payload['current_cycle_index'])
    ready=bool(payload['data_ready'])
    return CanonicalDivergenceCandidate(SourceContext.EXP0017,'SCGDDivergenceCandidate',source,str(payload['divergence_id']),rid,opp,direction,side,str(payload['hunter_symbol']),str(payload['clean_symbol']),bool(payload['one_sided_hunt']),bool(payload['both_symbols_hunted_same_side']),ready,float(payload['hunter_reference_price']),float(payload['clean_reference_price']),int(payload['current_cycle_start_ny']),_health(ready),'CGD_CANDIDATE_ADAPTED' if ready else 'CGD_CANDIDATE_NOT_READY')

def adapt_cgc_confirmation(payload:Mapping[str,Any])->CanonicalConfirmationResult:
    fields=('signal_id','direction','side','status','hunter_symbol','clean_symbol','confirmation_timeframe_seconds','confirmation_time_utc','confirmation_time_broker','clean_stop_reference_price','one_sided_hunt','double_hunt_invalidated','data_ready')
    _required(payload,fields,'FP_CGC_CONFIRMATION_ADAPTER')
    direction=Direction.BULLISH if payload['direction']==1 or str(payload['direction']).upper() in ('BUY','BULLISH') else Direction.BEARISH if payload['direction']==2 or str(payload['direction']).upper() in ('SELL','BEARISH') else Direction.NONE
    side=HuntSide.LOW if payload['side']==1 or str(payload['side']).upper()=='LOW' else HuntSide.HIGH if payload['side']==2 or str(payload['side']).upper()=='HIGH' else HuntSide.NONE
    status=payload['status']; outcome=ConfirmationOutcome.CONFIRMED if status==1 or str(status).upper()=='CONFIRMED_TRADEABLE' else ConfirmationOutcome.INVALIDATED_DOUBLE_HUNT if status==2 or bool(payload['double_hunt_invalidated']) else ConfirmationOutcome.UNAVAILABLE
    final=outcome in (ConfirmationOutcome.CONFIRMED,ConfirmationOutcome.INVALIDATED_DOUBLE_HUNT)
    source=canonical_sha256(payload)
    return CanonicalConfirmationResult(SourceContext.EXP0017,'SCGCFinalSignal',source,str(payload['signal_id']),str(payload.get('candidate_id',payload['signal_id'])),str(payload.get('observation_id','')),str(payload.get('current_cycle_index','')),outcome,direction,side,str(payload['hunter_symbol']),str(payload['clean_symbol']),int(payload['confirmation_timeframe_seconds']),int(payload.get('host_bar_open_utc',payload['confirmation_time_utc']-int(payload['confirmation_timeframe_seconds']))),int(payload['confirmation_time_utc']),float(payload['clean_stop_reference_price']),final,final,True,_health(bool(payload['data_ready'])),'CGC_CONFIRMATION_ADAPTED')

def adapt_daye_hunt(payload:Mapping[str,Any])->CanonicalHuntObservation:
    fields=('observation_id','opportunity_id','relationship_id','side','pair_state','hunter_canonical_symbol','protected_canonical_symbol','reference_price_a','reference_price_b','current_extreme_a','current_extreme_b','event_time_utc','availability_time_utc','is_replay_safe','status')
    _required(payload,fields,'FP_DAYE_HUNT_ADAPTER')
    side=HuntSide.HIGH if payload['side']==1 or str(payload['side']).upper()=='HIGH' else HuntSide.LOW if payload['side']==2 or str(payload['side']).upper()=='LOW' else HuntSide.NONE
    ps=payload['pair_state'];pair={1:PairState.NONE,2:PairState.A_ONLY,3:PairState.B_ONLY,4:PairState.BOTH,5:PairState.UNAVAILABLE}.get(ps,PairState.UNAVAILABLE)
    if isinstance(ps,str): pair={'NONE':PairState.NONE,'A_ONLY':PairState.A_ONLY,'B_ONLY':PairState.B_ONLY,'BOTH':PairState.BOTH}.get(ps.upper(),PairState.UNAVAILABLE)
    ready=payload['status']==1 or str(payload['status']).upper()=='READY'
    return CanonicalHuntObservation(SourceContext.EXP0018,'DAYE_HuntObservation',canonical_sha256(payload),str(payload['observation_id']),str(payload.get('reference_id',payload['relationship_id'])),str(payload['opportunity_id']),side,pair,str(payload['hunter_canonical_symbol']),str(payload['protected_canonical_symbol']),float(payload['reference_price_a']),float(payload['reference_price_b']),float(payload['current_extreme_a']),float(payload['current_extreme_b']),int(payload['event_time_utc']),int(payload['availability_time_utc']),bool(payload['is_replay_safe']),_health(ready),'DAYE_HUNT_ADAPTED' if ready else 'DAYE_HUNT_NOT_READY')

def adapt_daye_confirmation(payload:Mapping[str,Any])->CanonicalConfirmationResult:
    fields=('result_id','candidate_id','observation_id','opportunity_id','outcome','side','hunter_canonical_symbol','protected_canonical_symbol','host_bar_open_utc','host_bar_close_utc','confirmation_endpoint_price','is_final','is_immutable','is_replay_safe','status','reason_code')
    _required(payload,fields,'FP_DAYE_CONFIRMATION_ADAPTER')
    raw=payload['outcome']; outcome={1:ConfirmationOutcome.CONFIRMED,2:ConfirmationOutcome.INVALIDATED_DOUBLE_HUNT,3:ConfirmationOutcome.NO_SIGNAL_AT_CLOSE,4:ConfirmationOutcome.UNAVAILABLE,5:ConfirmationOutcome.ROLE_CHANGED,6:ConfirmationOutcome.MISSED_CLOSE}.get(raw,ConfirmationOutcome.NONE)
    if isinstance(raw,str): outcome={'CONFIRMED':ConfirmationOutcome.CONFIRMED,'INVALIDATED_DOUBLE_HUNT':ConfirmationOutcome.INVALIDATED_DOUBLE_HUNT,'NO_SIGNAL_AT_CLOSE':ConfirmationOutcome.NO_SIGNAL_AT_CLOSE,'UNAVAILABLE_AT_CLOSE':ConfirmationOutcome.UNAVAILABLE,'INVALIDATED_ROLE_CHANGED':ConfirmationOutcome.ROLE_CHANGED,'MISSED_CLOSE_REPLAY_REQUIRED':ConfirmationOutcome.MISSED_CLOSE}.get(raw.upper(),ConfirmationOutcome.NONE)
    side=HuntSide.HIGH if payload['side']==1 or str(payload['side']).upper()=='HIGH' else HuntSide.LOW if payload['side']==2 or str(payload['side']).upper()=='LOW' else HuntSide.NONE
    direction=Direction.BEARISH if side is HuntSide.HIGH else Direction.BULLISH if side is HuntSide.LOW else Direction.NONE
    ready=payload['status']==1 or str(payload['status']).upper()=='READY'
    return CanonicalConfirmationResult(SourceContext.EXP0018,'DAYE_ConfirmationResult',canonical_sha256(payload),str(payload['result_id']),str(payload['candidate_id']),str(payload['observation_id']),str(payload['opportunity_id']),outcome,direction,side,str(payload['hunter_canonical_symbol']),str(payload['protected_canonical_symbol']),int(payload.get('host_timeframe_seconds',int(payload['host_bar_close_utc'])-int(payload['host_bar_open_utc']))),int(payload['host_bar_open_utc']),int(payload['host_bar_close_utc']),float(payload['confirmation_endpoint_price']),bool(payload['is_final']),bool(payload['is_immutable']),bool(payload['is_replay_safe']),_health(ready),str(payload['reason_code']))

def adapt_daye_lifecycle(payload:Mapping[str,Any])->CanonicalLifecycleRecord:
    fields=('reference_id','side','protected_canonical_symbol','first_hunter_canonical_symbol','state','is_retired','accepted_use_count','duplicate_use_count','rejected_use_count','activation_event_time_utc','retirement_event_time_utc','is_immutable','is_replay_safe','status','reason_code')
    _required(payload,fields,'FP_DAYE_LIFECYCLE_ADAPTER')
    side=HuntSide.HIGH if payload['side']==1 or str(payload['side']).upper()=='HIGH' else HuntSide.LOW if payload['side']==2 or str(payload['side']).upper()=='LOW' else HuntSide.NONE
    ready=payload['status']==1 or str(payload['status']).upper() in ('READY','PROTECTED_SURVIVES')
    return CanonicalLifecycleRecord(SourceContext.EXP0018,'DAYE_ReferenceLifecycleRecord',canonical_sha256(payload),str(payload['reference_id']),side,str(payload['protected_canonical_symbol']),str(payload['first_hunter_canonical_symbol']),str(payload['state']),bool(payload['is_retired']),int(payload['accepted_use_count']),int(payload['duplicate_use_count']),int(payload['rejected_use_count']),int(payload['activation_event_time_utc']),int(payload['retirement_event_time_utc']),bool(payload['is_immutable']),bool(payload['is_replay_safe']),_health(ready),str(payload['reason_code']))

ADAPTERS={
 'FP_CGT_TIME_ADAPTER@1.0.0':adapt_cgt_time,
 'FP_CGR_REFERENCE_ADAPTER@1.0.0':adapt_cgr_reference,
 'FP_CGH_HUNT_ADAPTER@1.0.0':adapt_cgh_hunt,
 'FP_CGD_DIVERGENCE_ADAPTER@1.0.0':adapt_cgd_candidate,
 'FP_CGC_CONFIRMATION_ADAPTER@1.0.0':adapt_cgc_confirmation,
 'FP_DAYE_HUNT_ADAPTER@1.0.0':adapt_daye_hunt,
 'FP_DAYE_CONFIRMATION_ADAPTER@1.0.0':adapt_daye_confirmation,
 'FP_DAYE_LIFECYCLE_ADAPTER@1.0.0':adapt_daye_lifecycle,
}

def run_read_only_adapter(adapter_key:str,payload:Mapping[str,Any]):
    if adapter_key not in ADAPTERS: raise CompatibilityError('unknown_adapter',f'unknown_adapter: {adapter_key}')
    before=canonical_sha256(payload); frozen=deepcopy(payload)
    output=ADAPTERS[adapter_key](payload); after=canonical_sha256(payload)
    if payload!=frozen or before!=after: raise CompatibilityError('source_mutation_detected',adapter_key)
    repeated=ADAPTERS[adapter_key](payload)
    return output,before,after,output.snapshot_hash,repeated.snapshot_hash
