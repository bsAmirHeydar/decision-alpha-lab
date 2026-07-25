from __future__ import annotations
from time import perf_counter_ns
from .contracts import *
from .identity import build_instance_identity
from .composition import build_composition
from .health import build_module_health,aggregate_health
from .channels import project_buffers
from .scheduler import IncrementalCursor,plan_incremental,apply_plan
from .events import LifecycleEventChain
from .checkpoint import validate_checkpoint
from .canonical import canonical_sha256,stable_id,require_m1
from .enums import *
from .errors import FPI10InitializationError,FPI10Error

class IndicatorEngine:
    def __init__(self):
        self.config=None; self.instance=None; self.composition=None; self.lifecycle=LifecycleState.CREATED; self.cursor=None; self.event_chain=None; self.snapshot=None; self.checkpoint_disposition=CheckpointDisposition.ABSENT; self.initialized=False
        self.counters={'calculate_calls':0,'timer_calls':0,'chart_events':0,'processed_minutes':0,'rebuilds':0}
    def _append(self,t,now,reason,payload): return self.event_chain.append(t,now,reason,payload)
    def initialize(self,*,config,chart_id,terminal_instance_id,modules,now_m1,checkpoint=None):
        require_m1(now_m1,'now_m1'); self.config=config; self.lifecycle=LifecycleState.INITIALIZING
        self.instance=build_instance_identity(config,chart_id,terminal_instance_id); self.event_chain=LifecycleEventChain(self.instance.instance_id)
        self._append(LifecycleEventType.INIT_STARTED,now_m1,'FP_IND_INIT_STARTED',{'config_hash':config.config_hash})
        self._append(LifecycleEventType.INPUT_VALIDATED,now_m1,'FP_IND_INPUT_VALIDATED',{'pair_id':config.pair_id})
        self.composition=build_composition(config,modules)
        self._append(LifecycleEventType.UPSTREAM_VALIDATED,now_m1,'FP_IND_UPSTREAM_VALIDATED',{'composition_hash':self.composition.manifest_hash})
        self._append(LifecycleEventType.INSTANCE_CREATED,now_m1,'FP_IND_INSTANCE_CREATED',{'instance_id':self.instance.instance_id})
        val=validate_checkpoint(checkpoint,instance=self.instance,composition=self.composition); self.checkpoint_disposition=val.disposition
        if val.accepted:
            self.cursor=IncrementalCursor(checkpoint.last_processed_m1); self._append(LifecycleEventType.CHECKPOINT_RESTORED,now_m1,'FP_IND_CHECKPOINT_RESTORED',{'checkpoint_id':checkpoint.checkpoint_id})
        else:
            self.cursor=IncrementalCursor(0); self.counters['rebuilds']+=1; self._append(LifecycleEventType.REBUILD_STARTED,now_m1,'FP_IND_REBUILD_REQUIRED',{'disposition':val.disposition.value})
        self.lifecycle=LifecycleState.READY
        self._append(LifecycleEventType.ENGINE_READY,now_m1,'FP_IND_ENGINE_READY',{'instance_id':self.instance.instance_id})
        self.initialized=True
        initial_start=max(0,now_m1-config.history_days*1440*60000)
        return self.calculate(target_closed_m1=now_m1,upstream_state={'data_readiness':DataReadiness.PARTIAL,'history_ready':False,'source_revision_id':'REV-INIT','source_revision_sequence':0,'active_ww_direction':ActiveWWDirection.NONE,'confirmed_signal_count':0,'allowed_signal_count':0,'suppressed_by_ww_count':0,'suppressed_by_quota_count':0,'quota_winner_signal_id':'','ledger_event_count':0},trigger=ProcessTrigger.INIT,initial_history_start_m1=initial_start)
    def calculate(self,*,target_closed_m1,upstream_state,trigger=ProcessTrigger.CALCULATE,initial_history_start_m1=None):
        if not self.initialized: raise FPI10Error('FP_IND_NOT_INITIALIZED','initialize first')
        require_m1(target_closed_m1,'target_closed_m1'); start_ns=perf_counter_ns(); self.counters['calculate_calls']+=1
        plan=plan_incremental(cursor=self.cursor,target_closed_m1=target_closed_m1,max_minutes=self.config.max_incremental_minutes,trigger=trigger,initial_history_start_m1=initial_history_start_m1)
        apply_plan(self.cursor,plan); self.counters['processed_minutes']+=plan.work_minutes
        if plan.work_minutes: self._append(LifecycleEventType.CALCULATE_INCREMENTAL,target_closed_m1,'FP_IND_INCREMENTAL_PROCESSED',{'plan_hash':plan.plan_hash,'work_minutes':plan.work_minutes})
        duration=(perf_counter_ns()-start_ns)//1000
        return self._build_snapshot(now_m1=target_closed_m1,upstream_state=upstream_state,processing_us=duration,remaining=plan.remaining_minutes)
    def timer(self,*,now_m1,upstream_state):
        if not self.initialized: raise FPI10Error('FP_IND_NOT_INITIALIZED','initialize first')
        require_m1(now_m1,'now_m1'); self.counters['timer_calls']+=1; self._append(LifecycleEventType.TIMER_HEARTBEAT,now_m1,'FP_IND_TIMER_HEARTBEAT',{'timer_calls':self.counters['timer_calls']})
        return self._build_snapshot(now_m1=now_m1,upstream_state=upstream_state,processing_us=0,remaining=max(0,((now_m1-self.cursor.last_processed_m1)//60000)-1))
    def chart_event(self,*,now_m1,event_id:int,sparam=''):
        if not self.initialized: raise FPI10Error('FP_IND_NOT_INITIALIZED','initialize first')
        require_m1(now_m1,'now_m1'); self.counters['chart_events']+=1; self._append(LifecycleEventType.CHART_EVENT,now_m1,'FP_IND_CHART_EVENT_OBSERVED',{'event_id':event_id,'sparam':sparam[:128]})
        return self.snapshot
    def _build_snapshot(self,*,now_m1,upstream_state,processing_us,remaining):
        data=upstream_state.get('data_readiness',DataReadiness.BLOCKED); history=bool(upstream_state.get('history_ready',False)); source_id=upstream_state.get('source_revision_id','REV-UNKNOWN')
        mods=tuple(build_module_health(m,self.cursor.last_processed_m1,source_id,self.counters['processed_minutes']) for m in self.composition.modules)
        health=aggregate_health(lifecycle=self.lifecycle,data_readiness=data,history_ready=history,checkpoint_disposition=self.checkpoint_disposition,module_health=mods,incremental_lag_minutes=remaining,last_processing_duration_us=processing_us,generated_utc_ms=now_m1,config_hash=self.config.config_hash)
        if health.overall is HealthState.BLOCKED: self.lifecycle=LifecycleState.BLOCKED
        elif health.overall is HealthState.DEGRADED and self.lifecycle is LifecycleState.READY: self.lifecycle=LifecycleState.DEGRADED
        elif health.overall is HealthState.READY and self.lifecycle in (LifecycleState.DEGRADED,LifecycleState.INITIALIZING): self.lifecycle=LifecycleState.READY
        buffers=project_buffers(health=health.overall,lifecycle=self.lifecycle,data_readiness=data,active_ww_direction=upstream_state.get('active_ww_direction',ActiveWWDirection.NONE),confirmed_signal_count=int(upstream_state.get('confirmed_signal_count',0)),allowed_signal_count=int(upstream_state.get('allowed_signal_count',0)),suppressed_by_ww_count=int(upstream_state.get('suppressed_by_ww_count',0)),suppressed_by_quota_count=int(upstream_state.get('suppressed_by_quota_count',0)),quota_winner_signal_id=upstream_state.get('quota_winner_signal_id',''),ledger_event_count=int(upstream_state.get('ledger_event_count',0)),source_revision_sequence=int(upstream_state.get('source_revision_sequence',0)),generated_utc_ms=now_m1,enabled=self.config.enable_state_buffers)
        seq=0 if self.snapshot is None else self.snapshot.sequence+1
        payload={'sequence':seq,'instance_hash':self.instance.identity_hash,'composition_hash':self.composition.manifest_hash,'health_hash':health.report_hash,'buffer_hash':buffers.frame_hash,'active_ww_direction':int(upstream_state.get('active_ww_direction',ActiveWWDirection.NONE)),'confirmed_signal_count':int(upstream_state.get('confirmed_signal_count',0)),'allowed_signal_count':int(upstream_state.get('allowed_signal_count',0)),'suppressed_by_ww_count':int(upstream_state.get('suppressed_by_ww_count',0)),'suppressed_by_quota_count':int(upstream_state.get('suppressed_by_quota_count',0)),'quota_winner_signal_id':upstream_state.get('quota_winner_signal_id',''),'ledger_event_count':int(upstream_state.get('ledger_event_count',0)),'source_revision_sequence':int(upstream_state.get('source_revision_sequence',0)),'source_revision_id':source_id,'last_processed_m1':self.cursor.last_processed_m1,'generated_utc_ms':now_m1}
        self.snapshot=IndicatorSnapshot(stable_id('FPSNAP',payload),seq,self.instance,self.composition,health,buffers,ActiveWWDirection(payload['active_ww_direction']),payload['confirmed_signal_count'],payload['allowed_signal_count'],payload['suppressed_by_ww_count'],payload['suppressed_by_quota_count'],payload['quota_winner_signal_id'],payload['ledger_event_count'],payload['source_revision_sequence'],source_id,self.cursor.last_processed_m1,now_m1,canonical_sha256(payload)); return self.snapshot
    def deinitialize(self,*,now_m1,reason='FP_IND_DEINIT_REQUESTED'):
        if not self.initialized: return None
        self.lifecycle=LifecycleState.STOPPING; self._append(LifecycleEventType.DEINIT_STARTED,now_m1,reason,{'snapshot_hash':self.snapshot.snapshot_hash if self.snapshot else ''})
        self.lifecycle=LifecycleState.STOPPED; self._append(LifecycleEventType.DEINIT_COMPLETED,now_m1,'FP_IND_DEINIT_COMPLETED',{'instance_id':self.instance.instance_id}); self.initialized=False; return self.event_chain.head
