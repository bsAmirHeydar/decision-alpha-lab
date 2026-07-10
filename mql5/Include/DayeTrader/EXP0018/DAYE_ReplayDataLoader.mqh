#ifndef __EXP0018_DAYE_REPLAY_DATA_LOADER_MQH__
#define __EXP0018_DAYE_REPLAY_DATA_LOADER_MQH__

#include <DayeTrader/EXP0018/DAYE_ReplayIdentity.mqh>

bool DAYE_ValidateReplayConfig(const DAYE_ReplayConfig &config,const DAYE_TimeConfig &time_config,string &reason)
{
   reason="";
   if(config.schema_version!=DAYE_REPLAY_SCHEMA_VERSION) { reason="replay_schema_version_mismatch"; return false; }
   if(config.replay_start_new_york<=0 || config.replay_end_new_york<=config.replay_start_new_york)
   { reason="invalid_replay_new_york_range"; return false; }
   if(config.maximum_replay_bars<10) { reason="maximum_replay_bars_too_small"; return false; }
   if(config.cursor_steps_per_timer<1) { reason="cursor_steps_per_timer_must_be_positive"; return false; }
   if(config.output_prefix=="") { reason="output_prefix_empty"; return false; }
   if(config.require_manual_fixed_broker_offset && time_config.broker_offset_mode!=DAYE_BROKER_OFFSET_MANUAL_FIXED)
   { reason="historical_replay_requires_manual_fixed_broker_offset"; return false; }
   string nested="";
   if(!DAYE_ValidateConfirmationConfig(config.lifecycle_config.confirmation_config,nested))
   { reason="confirmation_config:"+nested; return false; }
   if(config.lifecycle_config.schema_version!=DAYE_LIFECYCLE_SCHEMA_VERSION)
   { reason="lifecycle_schema_version_mismatch"; return false; }
   if(!config.lifecycle_config.allow_repeat_across_new_opportunities_while_protected_survives ||
      !config.lifecycle_config.suppress_duplicate_exact_opportunity ||
      !config.lifecycle_config.retire_on_protected_touch)
   { reason="core_lifecycle_policy_not_enabled"; return false; }
   return true;
}

bool DAYE_ReplayUtcToBroker(const datetime utc_time,const DAYE_TimeConfig &time_config,datetime &broker_time,string &reason)
{
   reason="";
   int offset=0; bool replay_safe=true;
   if(!DAYE_ResolveBrokerOffsetMinutes(time_config,offset,replay_safe,reason)) return false;
   if(!replay_safe) { reason="broker_offset_not_replay_safe"; return false; }
   broker_time=DAYE_ShiftMinutes(utc_time,offset);
   return broker_time>0;
}

bool DAYE_ResolveReplayRange(const DAYE_ReplayConfig &config,const DAYE_TimeConfig &time_config,
                             datetime &start_utc,datetime &end_utc,datetime &start_broker,datetime &end_broker,
                             string &reason)
{
   reason="";
   DAYE_StatusCode start_status=DAYE_ResolveNewYorkLocalToUtc(config.replay_start_new_york,time_config,
                                                              time_config.ambiguous_start_policy,start_utc,reason);
   if(start_status!=DAYE_STATUS_OK) { reason="start_"+reason; return false; }
   DAYE_StatusCode end_status=DAYE_ResolveNewYorkLocalToUtc(config.replay_end_new_york,time_config,
                                                            time_config.ambiguous_end_policy,end_utc,reason);
   if(end_status!=DAYE_STATUS_OK) { reason="end_"+reason; return false; }
   if(end_utc<=start_utc) { reason="resolved_utc_range_not_positive"; return false; }
   if(!DAYE_ReplayUtcToBroker(start_utc,time_config,start_broker,reason)) return false;
   if(!DAYE_ReplayUtcToBroker(end_utc,time_config,end_broker,reason)) return false;
   return true;
}

bool DAYE_LoadReplaySymbolRange(const DAYE_SymbolDescriptor &descriptor,
                                const DAYE_DataSyncConfig &data_config,
                                const DAYE_TimeConfig &time_config,
                                const datetime start_utc,const datetime end_utc,
                                const datetime start_broker,const datetime end_broker,
                                const int maximum_replay_bars,
                                DAYE_SymbolBar &bars[],string &reason)
{
   ArrayResize(bars,0); reason="";
   MqlRates raw[]; ArraySetAsSeries(raw,false);
   ResetLastError();
   int copied=CopyRates(descriptor.broker_symbol,data_config.base_timeframe,start_broker,end_broker,raw);
   if(copied<=0) { reason="copy_rates_range_failed_"+IntegerToString(GetLastError()); return false; }
   if(copied>maximum_replay_bars) { reason="source_range_exceeds_maximum_replay_bars"; return false; }

   int base_seconds=PeriodSeconds(data_config.base_timeframe);
   datetime replay_current_broker=end_broker+(datetime)base_seconds+1;
   ArrayResize(bars,copied);
   int accepted=0;
   for(int i=0;i<copied;i++)
   {
      DAYE_SymbolBar built;
      if(!DAYE_BuildSymbolBar(raw[i],descriptor,data_config.base_timeframe,time_config,replay_current_broker,built))
      {
         if(data_config.fail_on_any_invalid_bar) { reason="invalid_source_bar:"+built.reason_code; ArrayResize(bars,0); return false; }
         continue;
      }
      if(built.event_time_utc<start_utc || built.close_time_utc>end_utc) continue;
      if(built.completeness!=DAYE_BAR_COMPLETENESS_CLOSED) continue;
      bars[accepted++]=built;
   }
   ArrayResize(bars,accepted);
   if(accepted<2) { reason="replay_range_contains_insufficient_closed_bars"; return false; }

   DAYE_SymbolDataHealth health; ZeroMemory(health);
   health.schema_version=DAYE_DATA_SCHEMA_VERSION;
   health.broker_symbol=descriptor.broker_symbol; health.canonical_symbol=descriptor.canonical_symbol;
   if(!DAYE_ValidateChronologicalBars(bars,health)) { reason=health.reason_code; return false; }
   return true;
}

bool DAYE_LoadReplaySource(const DAYE_ReplayConfig &config,const DAYE_TimeConfig &time_config,
                           DAYE_ReplaySource &source)
{
   ZeroMemory(source); ArrayResize(source.pairs,0);
   string reason="";
   if(!DAYE_ResolveReplayRange(config,time_config,source.start_utc,source.end_utc,
                               source.start_broker,source.end_broker,reason))
   { source.reason_code=reason; return false; }

   DAYE_DataSyncConfig data_config=config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config;
   DAYE_SymbolDescriptor descriptor_a,descriptor_b;
   if(!DAYE_LoadSymbolDescriptor(data_config.broker_symbol_a,data_config.canonical_symbol_a,descriptor_a))
   { source.reason_code="symbol_a:"+descriptor_a.reason_code; return false; }
   if(!DAYE_LoadSymbolDescriptor(data_config.broker_symbol_b,data_config.canonical_symbol_b,descriptor_b))
   { source.reason_code="symbol_b:"+descriptor_b.reason_code; return false; }

   DAYE_SymbolBar bars_a[],bars_b[];
   if(!DAYE_LoadReplaySymbolRange(descriptor_a,data_config,time_config,source.start_utc,source.end_utc,
                                  source.start_broker,source.end_broker,config.maximum_replay_bars,bars_a,reason))
   { source.reason_code="symbol_a:"+reason; return false; }
   if(!DAYE_LoadReplaySymbolRange(descriptor_b,data_config,time_config,source.start_utc,source.end_utc,
                                  source.start_broker,source.end_broker,config.maximum_replay_bars,bars_b,reason))
   { source.reason_code="symbol_b:"+reason; return false; }
   source.copied_a=ArraySize(bars_a); source.copied_b=ArraySize(bars_b);

   DAYE_DataSyncConfig replay_data=data_config;
   replay_data.minimum_common_bars=1;
   replay_data.maximum_pairs_to_publish=config.maximum_replay_bars;
   replay_data.require_complete_alignment=config.require_complete_source_alignment;
   replay_data.enforce_freshness=false;
   DAYE_DataSyncSummary sync; ZeroMemory(sync);
   sync.schema_version=DAYE_DATA_SCHEMA_VERSION;
   sync.is_replay_safe=true;
   if(!DAYE_AlignBarsByExactUtc(bars_a,bars_b,replay_data,source.end_utc,source.pairs,sync))
   { source.reason_code=sync.reason_code; source.unmatched_a=sync.unmatched_a; source.unmatched_b=sync.unmatched_b; return false; }
   source.aligned_count=ArraySize(source.pairs);
   source.unmatched_a=sync.unmatched_a; source.unmatched_b=sync.unmatched_b;
   if(config.require_complete_source_alignment && (source.unmatched_a>0 || source.unmatched_b>0))
   { source.reason_code="strict_replay_rejects_unmatched_source_timestamps"; return false; }
   source.is_replay_safe=true; source.is_ready=true; source.reason_code="historical_source_loaded_exact_utc";
   return true;
}

#endif
