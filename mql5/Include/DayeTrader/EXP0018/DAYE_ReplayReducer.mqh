#ifndef __EXP0018_DAYE_REPLAY_REDUCER_MQH__
#define __EXP0018_DAYE_REPLAY_REDUCER_MQH__

#include <DayeTrader/EXP0018/DAYE_ReplayDataLoader.mqh>

bool DAYE_FindReplayObservation(const DAYE_HuntObservation &items[],const string observation_id,DAYE_HuntObservation &result)
{
   for(int i=0;i<ArraySize(items);i++) if(items[i].observation_id==observation_id) { result=items[i]; return true; }
   return false;
}

void DAYE_CopyReplayPrefix(const DAYE_SynchronizedBarPair &source[],const int count,
                           DAYE_SymbolBar &bars_a[],DAYE_SymbolBar &bars_b[],DAYE_SynchronizedBarPair &pairs[])
{
   int n=count; if(n<0) n=0; if(n>ArraySize(source)) n=ArraySize(source);
   ArrayResize(bars_a,n); ArrayResize(bars_b,n); ArrayResize(pairs,n);
   for(int i=0;i<n;i++) { pairs[i]=source[i]; bars_a[i]=source[i].symbol_a; bars_b[i]=source[i].symbol_b; }
}

bool DAYE_BuildReplayPipelineFrame(const DAYE_ReplayConfig &config,const DAYE_TimeConfig &time_config,
                                   const DAYE_PeriodDefinition &period_registry[],
                                   const DAYE_RelationshipDefinition &relationship_registry[],
                                   const DAYE_SynchronizedBarPair &source_pairs[],const int prefix_count,
                                   DAYE_PairedPeriodSnapshot &periods[],DAYE_RelationshipResolution &resolutions[],
                                   DAYE_HuntObservation &observations[],string &reason)
{
   reason="";
   DAYE_SymbolBar bars_a[],bars_b[]; DAYE_SynchronizedBarPair pairs[];
   DAYE_CopyReplayPrefix(source_pairs,prefix_count,bars_a,bars_b,pairs);
   if(ArraySize(pairs)<1) { reason="empty_replay_prefix"; return false; }
   datetime as_of_utc=pairs[ArraySize(pairs)-1].availability_time_utc;

   DAYE_PeriodAggregationConfig period_config=config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config;
   DAYE_SymbolPeriodSnapshot periods_a[],periods_b[];
   string reason_a="",reason_b="";
   if(!DAYE_AggregateSymbolBars(bars_a,period_config,time_config,period_registry,as_of_utc,as_of_utc,periods_a,reason_a))
   { reason="aggregate_a:"+reason_a; return false; }
   if(!DAYE_AggregateSymbolBars(bars_b,period_config,time_config,period_registry,as_of_utc,as_of_utc,periods_b,reason_b))
   { reason="aggregate_b:"+reason_b; return false; }
   DAYE_BuildPairedPeriodSnapshots(periods_a,periods_b,pairs,period_config,as_of_utc,periods);

   DAYE_RelationshipStoreSummary relationship_summary;
   DAYE_RelationshipConfig relationship_config=config.lifecycle_config.confirmation_config.hunt_config.relationship_config;
   DAYE_ResolveRelationshipOpportunities(periods,relationship_registry,relationship_config,as_of_utc,resolutions,relationship_summary);
   if(config.fail_on_pipeline_error && relationship_summary.status==DAYE_REL_RESOLUTION_INVALID_REGISTRY)
   { reason="relationship_registry_invalid:"+relationship_summary.reason_code; return false; }

   DAYE_HuntStoreSummary hunt_summary;
   DAYE_HuntConfig hunt_config=config.lifecycle_config.confirmation_config.hunt_config;
   DAYE_ClassifyHuntObservations(resolutions,hunt_config,as_of_utc,observations,hunt_summary);
   if(config.fail_on_pipeline_error && hunt_summary.status==DAYE_HUNT_STATUS_DUPLICATE_OBSERVATION_ID)
   { reason="hunt_pipeline_failed:"+hunt_summary.reason_code; return false; }
   return true;
}

bool DAYE_ResolveReplayHostWindow(const datetime availability_utc,const ENUM_TIMEFRAMES host_timeframe,
                                  const DAYE_TimeConfig &time_config,datetime &open_utc,datetime &close_utc,string &reason)
{
   reason="";
   int host_seconds=PeriodSeconds(host_timeframe); if(host_seconds<=0) { reason="invalid_host_timeframe"; return false; }
   int offset_minutes=0; bool replay_safe=true;
   if(!DAYE_ResolveBrokerOffsetMinutes(time_config,offset_minutes,replay_safe,reason) || !replay_safe) return false;
   long broker_value=(long)DAYE_ShiftMinutes(availability_utc,offset_minutes);
   long remainder=broker_value%(long)host_seconds;
   long close_broker=(remainder==0 ? broker_value : broker_value+((long)host_seconds-remainder));
   long open_broker=close_broker-(long)host_seconds;
   open_utc=DAYE_ShiftMinutes((datetime)open_broker,-offset_minutes);
   close_utc=DAYE_ShiftMinutes((datetime)close_broker,-offset_minutes);
   return open_utc>0 && close_utc>open_utc;
}

void DAYE_InitReplayHostBar(const string broker_symbol,const string canonical_symbol,const ENUM_TIMEFRAMES timeframe,
                            const datetime open_utc,const datetime close_utc,const int broker_offset_minutes,
                            DAYE_HostBarSnapshot &bar)
{
   ZeroMemory(bar); bar.schema_version=DAYE_CONFIRMATION_SCHEMA_VERSION;
   bar.status=DAYE_HOST_CLOCK_SYMBOL_A_UNAVAILABLE; bar.reason_code="host_source_window_empty";
   bar.broker_symbol=broker_symbol; bar.canonical_symbol=canonical_symbol; bar.timeframe=timeframe;
   bar.timeframe_seconds=PeriodSeconds(timeframe); bar.open_time_utc=open_utc; bar.close_time_utc=close_utc;
   bar.broker_open_time=DAYE_ShiftMinutes(open_utc,broker_offset_minutes); bar.is_replay_safe=true;
}

bool DAYE_BuildReplayHostBarPair(const DAYE_SynchronizedBarPair &source_pairs[],const datetime open_utc,
                                 const datetime close_utc,const DAYE_ConfirmationConfig &confirmation_config,
                                 const DAYE_TimeConfig &time_config,DAYE_HostBarPair &host_pair,string &reason)
{
   reason="";
   DAYE_DataSyncConfig data=confirmation_config.hunt_config.relationship_config.period_config.data_config;
   ENUM_TIMEFRAMES host=DAYE_ResolveHostTimeframe(confirmation_config.host_timeframe);
   int host_seconds=PeriodSeconds(host); int base_seconds=PeriodSeconds(data.base_timeframe);
   if(host_seconds<=0 || base_seconds<=0 || host_seconds%base_seconds!=0) { reason="invalid_host_base_ratio"; return false; }
   int offset_minutes=0; bool replay_safe=true;
   if(!DAYE_ResolveBrokerOffsetMinutes(time_config,offset_minutes,replay_safe,reason) || !replay_safe) return false;

   DAYE_HostBarSnapshot a,b;
   DAYE_InitReplayHostBar(data.broker_symbol_a,data.canonical_symbol_a,host,open_utc,close_utc,offset_minutes,a);
   DAYE_InitReplayHostBar(data.broker_symbol_b,data.canonical_symbol_b,host,open_utc,close_utc,offset_minutes,b);
   int count=0; bool first=true;
   for(int i=0;i<ArraySize(source_pairs);i++)
   {
      if(source_pairs[i].event_time_utc<open_utc || source_pairs[i].event_time_utc>=close_utc) continue;
      if(first)
      {
         a.open=source_pairs[i].symbol_a.open; a.high=source_pairs[i].symbol_a.high; a.low=source_pairs[i].symbol_a.low;
         b.open=source_pairs[i].symbol_b.open; b.high=source_pairs[i].symbol_b.high; b.low=source_pairs[i].symbol_b.low;
         first=false;
      }
      if(source_pairs[i].symbol_a.high>a.high) a.high=source_pairs[i].symbol_a.high;
      if(source_pairs[i].symbol_a.low<a.low) a.low=source_pairs[i].symbol_a.low;
      if(source_pairs[i].symbol_b.high>b.high) b.high=source_pairs[i].symbol_b.high;
      if(source_pairs[i].symbol_b.low<b.low) b.low=source_pairs[i].symbol_b.low;
      a.close=source_pairs[i].symbol_a.close; b.close=source_pairs[i].symbol_b.close;
      a.tick_volume+=source_pairs[i].symbol_a.tick_volume; b.tick_volume+=source_pairs[i].symbol_b.tick_volume;
      a.real_volume+=source_pairs[i].symbol_a.real_volume; b.real_volume+=source_pairs[i].symbol_b.real_volume;
      a.spread=source_pairs[i].symbol_a.spread; b.spread=source_pairs[i].symbol_b.spread;
      count++;
   }
   int expected=host_seconds/base_seconds;
   if(count!=expected) { reason="host_window_source_count_"+IntegerToString(count)+"_expected_"+IntegerToString(expected); return false; }
   a.is_available=true; b.is_available=true; a.status=DAYE_HOST_CLOCK_READY; b.status=DAYE_HOST_CLOCK_READY;
   a.reason_code="replay_host_bar_ready"; b.reason_code="replay_host_bar_ready";
   if(!DAYE_BuildHostBarPair(a,b,confirmation_config.require_exact_host_symbol_alignment,host_pair))
   { reason=host_pair.reason_code; return false; }
   return true;
}

bool DAYE_ReplayApplyConfirmedResult(const DAYE_LifecycleConfig &config,const DAYE_ConfirmationResult &result,
                                     const datetime processing_time_utc,CDayeLifecycleStore &store,
                                     DAYE_ReferenceUseRecord &use,bool &reference_activated,bool &reference_retired,string &reason)
{
   ZeroMemory(use); reference_activated=false; reference_retired=false; reason="";
   if(store.IsResultProcessed(result.result_id)) { reason="result_already_processed"; return false; }
   store.RememberProcessedResult(result.result_id,config.maximum_processed_result_ids);
   string validation=""; if(!DAYE_IsValidConfirmedResult(result,validation)) { reason=validation; return false; }

   string a=config.confirmation_config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_a;
   string b=config.confirmation_config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_b;
   string reference_id=DAYE_BuildReferenceLifecycleId(result.reference_period_instance_id,result.side,a,b);
   string exact_key=DAYE_BuildExactOpportunityUseKey(result);
   int ref_index=store.FindReferenceIndex(reference_id); DAYE_ReferenceLifecycleRecord ref;
   if(ref_index<0)
   {
      string init_reason=""; if(!DAYE_InitializeReferenceRecord(config,result,ref,init_reason)) { reason=init_reason; return false; }
      if(!store.AppendReference(ref,config.maximum_reference_records)) { reason="append_reference_failed"; return false; }
      ref_index=store.FindReferenceIndex(reference_id); reference_activated=true;
   }
   if(!store.GetReference(ref_index,ref)) { reason="reference_not_found_after_activation"; return false; }

   DAYE_ReferenceUseStatus status=DAYE_USE_STATUS_ACCEPTED;
   string use_reason="confirmed_use_accepted_while_protected_survives";
   if(ref.is_retired || DAYE_IsReferenceRetiredState(ref.state))
   { status=DAYE_USE_STATUS_REJECTED_REFERENCE_RETIRED; use_reason="confirmed_result_arrived_after_reference_retirement"; ref.rejected_use_count++; }
   else if(ref.protected_canonical_symbol!=result.protected_canonical_symbol)
   {
      ref.state=DAYE_REF_STATE_RETIRED_ROLE_SWITCH; ref.is_retired=true; ref.is_immutable=true;
      ref.reason_code="role_switch_on_same_reference_retires_reference";
      ref.retirement_event_time_utc=result.event_time_utc; ref.retirement_availability_time_utc=result.availability_time_utc;
      ref.retirement_evidence_id=result.result_id; ref.rejected_use_count++; reference_retired=true;
      status=DAYE_USE_STATUS_REJECTED_ROLE_SWITCH; use_reason=ref.reason_code;
   }
   else if(config.suppress_duplicate_exact_opportunity && store.HasExactOpportunityUse(exact_key))
   { status=DAYE_USE_STATUS_DUPLICATE_EXACT_OPPORTUNITY; use_reason="exact_opportunity_already_has_first_confirmed_use"; ref.duplicate_use_count++; }
   else
   {
      ref.accepted_use_count++; ref.latest_confirmation_result_id=result.result_id;
      ref.latest_use_event_time_utc=result.event_time_utc; ref.reason_code="protected_symbol_survives_after_confirmed_use";
   }
   DAYE_BuildUseRecord(result,reference_id,status,use_reason,processing_time_utc,use);
   if(use.is_accepted || config.publish_rejected_uses) store.AppendUse(use,config.maximum_use_records);
   store.SetReference(ref_index,ref); reason=use_reason; return true;
}

int DAYE_ReplayApplyObservationsToReferences(const DAYE_LifecycleConfig &config,const DAYE_HuntObservation &observations[],
                                             CDayeLifecycleStore &store,datetime processing_time_utc,
                                             DAYE_ReferenceLifecycleRecord &retired_records[])
{
   ArrayResize(retired_records,0); int changed=0;
   for(int r=0;r<store.ReferenceCount();r++)
   {
      DAYE_ReferenceLifecycleRecord ref; if(!store.GetReference(r,ref) || ref.is_retired) continue;
      for(int o=0;o<ArraySize(observations);o++)
      {
         DAYE_ReferenceLifecycleState before; DAYE_LifecycleEventType event_type; string reason="";
         if(!DAYE_ApplyObservationToReference(config,observations[o],ref,before,event_type,reason)) continue;
         store.SetReference(r,ref); changed++;
         if(ref.is_retired)
         {
            int n=ArraySize(retired_records); ArrayResize(retired_records,n+1); retired_records[n]=ref; break;
         }
      }
   }
   return changed;
}

#endif
