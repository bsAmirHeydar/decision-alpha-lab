#ifndef __EXP0018_DAYE_LIFECYCLE_CHECKPOINT_MQH__
#define __EXP0018_DAYE_LIFECYCLE_CHECKPOINT_MQH__

#include <DayeTrader/EXP0018/DAYE_LifecycleEvents.mqh>

string DAYE_LifecycleSanitizeToken(string value)
{
   StringReplace(value,"/","_"); StringReplace(value,"\\","_");
   StringReplace(value,":","_"); StringReplace(value,"*","_");
   StringReplace(value,"?","_"); StringReplace(value,"\"","_");
   StringReplace(value,"<","_"); StringReplace(value,">","_");
   StringReplace(value,"|","_"); StringReplace(value," ","_");
   return value;
}

string DAYE_BuildLifecycleCheckpointFilename(const DAYE_LifecycleConfig &config)
{
   string a=DAYE_LifecycleSanitizeToken(config.confirmation_config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_a);
   string b=DAYE_LifecycleSanitizeToken(config.confirmation_config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_b);
   ENUM_TIMEFRAMES tf=DAYE_ResolveHostTimeframe(config.confirmation_config.host_timeframe);
   return DAYE_LifecycleSanitizeToken(config.checkpoint_prefix)+"_"+a+"_"+b+"_TF"+IntegerToString((int)tf)+".csv";
}

void DAYE_LifecycleSkipLine(const int handle)
{
   while(!FileIsEnding(handle) && !FileIsLineEnding(handle)) FileReadString(handle);
}

bool DAYE_SaveLifecycleCheckpoint(const DAYE_LifecycleConfig &config,
                                  CDayeLifecycleStore &store,
                                  string &reason)
{
   reason="";
   if(!config.persist_checkpoint) return true;
   string filename=DAYE_BuildLifecycleCheckpointFilename(config);
   int handle=FileOpen(filename,FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_SHARE_READ,',');
   if(handle==INVALID_HANDLE)
   {
      reason="lifecycle_checkpoint_open_write_failed_"+IntegerToString(GetLastError());
      return false;
   }
   FileWrite(handle,"META",DAYE_LIFECYCLE_SCHEMA_VERSION);
   DAYE_ReferenceLifecycleRecord refs[]; store.ExportReferences(refs);
   for(int i=0;i<ArraySize(refs);i++)
   {
      FileWrite(handle,"REFERENCE",refs[i].schema_version,(int)refs[i].status,(int)refs[i].state,refs[i].reason_code,
                refs[i].is_replay_safe?1:0,refs[i].is_retired?1:0,refs[i].is_immutable?1:0,
                refs[i].reference_id,refs[i].reference_period_instance_id,(int)refs[i].side,
                refs[i].broker_symbol_a,refs[i].canonical_symbol_a,refs[i].broker_symbol_b,refs[i].canonical_symbol_b,
                refs[i].reference_price_a,refs[i].reference_price_b,refs[i].first_hunter_canonical_symbol,
                refs[i].protected_canonical_symbol,refs[i].first_confirmation_result_id,refs[i].latest_confirmation_result_id,
                refs[i].latest_observation_id,(int)refs[i].latest_pair_state,refs[i].activation_event_time_utc,
                refs[i].activation_availability_time_utc,refs[i].latest_use_event_time_utc,
                refs[i].latest_observation_availability_time_utc,refs[i].retirement_event_time_utc,
                refs[i].retirement_availability_time_utc,refs[i].accepted_use_count,refs[i].duplicate_use_count,
                refs[i].rejected_use_count,refs[i].retirement_evidence_id);
   }
   DAYE_ReferenceUseRecord uses[]; store.ExportUses(uses);
   for(int i=0;i<ArraySize(uses);i++)
   {
      FileWrite(handle,"USE",uses[i].schema_version,(int)uses[i].status,uses[i].reason_code,uses[i].is_accepted?1:0,
                uses[i].is_historical_immutable?1:0,uses[i].is_replay_safe?1:0,uses[i].use_id,
                uses[i].exact_opportunity_use_key,uses[i].reference_id,uses[i].result_id,uses[i].candidate_id,
                uses[i].observation_id,uses[i].opportunity_id,uses[i].relationship_id,uses[i].source_alias,
                uses[i].is_major?1:0,uses[i].chart_label,(int)uses[i].side,uses[i].hunter_broker_symbol,
                uses[i].hunter_canonical_symbol,uses[i].protected_broker_symbol,uses[i].protected_canonical_symbol,
                uses[i].current_period_instance_id,uses[i].reference_period_instance_id,uses[i].hunter_reference_price,
                uses[i].protected_reference_price,uses[i].host_bar_open_utc,uses[i].host_bar_close_utc,uses[i].host_bar_id,
                uses[i].hunter_host_open,uses[i].hunter_host_high,uses[i].hunter_host_low,uses[i].hunter_host_close,
                uses[i].confirmation_endpoint_price,uses[i].event_time_utc,uses[i].availability_time_utc,uses[i].processing_time_utc);
   }
   string processed[]; store.ExportProcessedResultIds(processed);
   for(int i=0;i<ArraySize(processed);i++) FileWrite(handle,"PROCESSED",processed[i]);
   FileFlush(handle); FileClose(handle); return true;
}

bool DAYE_LoadLifecycleCheckpoint(const DAYE_LifecycleConfig &config,
                                  CDayeLifecycleStore &store,
                                  int &restored_references,
                                  int &restored_uses,
                                  int &restored_processed,
                                  string &reason)
{
   reason=""; restored_references=0; restored_uses=0; restored_processed=0;
   if(!config.persist_checkpoint) return true;
   string filename=DAYE_BuildLifecycleCheckpointFilename(config);
   if(!FileIsExist(filename,FILE_COMMON)) return true;
   int handle=FileOpen(filename,FILE_READ|FILE_CSV|FILE_COMMON|FILE_SHARE_READ|FILE_SHARE_WRITE,',');
   if(handle==INVALID_HANDLE)
   {
      reason="lifecycle_checkpoint_open_read_failed_"+IntegerToString(GetLastError());
      return false;
   }
   while(!FileIsEnding(handle))
   {
      string t=FileReadString(handle);
      if(t=="") { DAYE_LifecycleSkipLine(handle); continue; }
      if(t=="META")
      {
         int schema=(int)StringToInteger(FileReadString(handle)); DAYE_LifecycleSkipLine(handle);
         if(schema!=DAYE_LIFECYCLE_SCHEMA_VERSION) { FileClose(handle); reason="lifecycle_checkpoint_schema_mismatch"; return false; }
      }
      else if(t=="REFERENCE")
      {
         DAYE_ReferenceLifecycleRecord r; ZeroMemory(r);
         r.schema_version=(int)StringToInteger(FileReadString(handle));
         r.status=(DAYE_LifecycleStatus)StringToInteger(FileReadString(handle));
         r.state=(DAYE_ReferenceLifecycleState)StringToInteger(FileReadString(handle));
         r.reason_code=FileReadString(handle); r.is_replay_safe=StringToInteger(FileReadString(handle))!=0;
         r.is_retired=StringToInteger(FileReadString(handle))!=0; r.is_immutable=StringToInteger(FileReadString(handle))!=0;
         r.reference_id=FileReadString(handle); r.reference_period_instance_id=FileReadString(handle);
         r.side=(DAYE_HuntSide)StringToInteger(FileReadString(handle)); r.broker_symbol_a=FileReadString(handle);
         r.canonical_symbol_a=FileReadString(handle); r.broker_symbol_b=FileReadString(handle); r.canonical_symbol_b=FileReadString(handle);
         r.reference_price_a=StringToDouble(FileReadString(handle)); r.reference_price_b=StringToDouble(FileReadString(handle));
         r.first_hunter_canonical_symbol=FileReadString(handle); r.protected_canonical_symbol=FileReadString(handle);
         r.first_confirmation_result_id=FileReadString(handle); r.latest_confirmation_result_id=FileReadString(handle);
         r.latest_observation_id=FileReadString(handle); r.latest_pair_state=(DAYE_HuntPairState)StringToInteger(FileReadString(handle));
         r.activation_event_time_utc=(datetime)StringToInteger(FileReadString(handle));
         r.activation_availability_time_utc=(datetime)StringToInteger(FileReadString(handle));
         r.latest_use_event_time_utc=(datetime)StringToInteger(FileReadString(handle));
         r.latest_observation_availability_time_utc=(datetime)StringToInteger(FileReadString(handle));
         r.retirement_event_time_utc=(datetime)StringToInteger(FileReadString(handle));
         r.retirement_availability_time_utc=(datetime)StringToInteger(FileReadString(handle));
         r.accepted_use_count=(int)StringToInteger(FileReadString(handle)); r.duplicate_use_count=(int)StringToInteger(FileReadString(handle));
         r.rejected_use_count=(int)StringToInteger(FileReadString(handle)); r.retirement_evidence_id=FileReadString(handle);
         DAYE_LifecycleSkipLine(handle);
         if(r.schema_version==DAYE_LIFECYCLE_SCHEMA_VERSION && store.AppendReference(r,config.maximum_reference_records)) restored_references++;
      }
      else if(t=="USE")
      {
         DAYE_ReferenceUseRecord u; ZeroMemory(u);
         u.schema_version=(int)StringToInteger(FileReadString(handle)); u.status=(DAYE_ReferenceUseStatus)StringToInteger(FileReadString(handle));
         u.reason_code=FileReadString(handle); u.is_accepted=StringToInteger(FileReadString(handle))!=0;
         u.is_historical_immutable=StringToInteger(FileReadString(handle))!=0; u.is_replay_safe=StringToInteger(FileReadString(handle))!=0;
         u.use_id=FileReadString(handle); u.exact_opportunity_use_key=FileReadString(handle); u.reference_id=FileReadString(handle);
         u.result_id=FileReadString(handle); u.candidate_id=FileReadString(handle); u.observation_id=FileReadString(handle);
         u.opportunity_id=FileReadString(handle); u.relationship_id=FileReadString(handle); u.source_alias=FileReadString(handle);
         u.is_major=StringToInteger(FileReadString(handle))!=0; u.chart_label=FileReadString(handle); u.side=(DAYE_HuntSide)StringToInteger(FileReadString(handle));
         u.hunter_broker_symbol=FileReadString(handle); u.hunter_canonical_symbol=FileReadString(handle);
         u.protected_broker_symbol=FileReadString(handle); u.protected_canonical_symbol=FileReadString(handle);
         u.current_period_instance_id=FileReadString(handle); u.reference_period_instance_id=FileReadString(handle);
         u.hunter_reference_price=StringToDouble(FileReadString(handle)); u.protected_reference_price=StringToDouble(FileReadString(handle));
         u.host_bar_open_utc=(datetime)StringToInteger(FileReadString(handle)); u.host_bar_close_utc=(datetime)StringToInteger(FileReadString(handle));
         u.host_bar_id=FileReadString(handle); u.hunter_host_open=StringToDouble(FileReadString(handle));
         u.hunter_host_high=StringToDouble(FileReadString(handle)); u.hunter_host_low=StringToDouble(FileReadString(handle));
         u.hunter_host_close=StringToDouble(FileReadString(handle)); u.confirmation_endpoint_price=StringToDouble(FileReadString(handle));
         u.event_time_utc=(datetime)StringToInteger(FileReadString(handle)); u.availability_time_utc=(datetime)StringToInteger(FileReadString(handle));
         u.processing_time_utc=(datetime)StringToInteger(FileReadString(handle)); DAYE_LifecycleSkipLine(handle);
         if(u.schema_version==DAYE_LIFECYCLE_SCHEMA_VERSION && store.AppendUse(u,config.maximum_use_records)) restored_uses++;
      }
      else if(t=="PROCESSED")
      {
         string id=FileReadString(handle); DAYE_LifecycleSkipLine(handle);
         if(store.RememberProcessedResult(id,config.maximum_processed_result_ids)) restored_processed++;
      }
      else DAYE_LifecycleSkipLine(handle);
   }
   FileClose(handle); return true;
}

#endif
