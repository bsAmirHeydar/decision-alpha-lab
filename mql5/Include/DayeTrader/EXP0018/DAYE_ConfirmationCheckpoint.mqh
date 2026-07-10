#ifndef __EXP0018_DAYE_CONFIRMATION_CHECKPOINT_MQH__
#define __EXP0018_DAYE_CONFIRMATION_CHECKPOINT_MQH__

#include <DayeTrader/EXP0018/DAYE_ConfirmationStore.mqh>

string DAYE_SanitizeCheckpointToken(string value)
{
   StringReplace(value,"/","_");
   StringReplace(value,"\\","_");
   StringReplace(value,":","_");
   StringReplace(value,"*","_");
   StringReplace(value,"?","_");
   StringReplace(value,"\"","_");
   StringReplace(value,"<","_");
   StringReplace(value,">","_");
   StringReplace(value,"|","_");
   StringReplace(value," ","_");
   return value;
}

string DAYE_BuildConfirmationCheckpointFilename(const DAYE_ConfirmationConfig &config)
{
   string a=DAYE_SanitizeCheckpointToken(config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_a);
   string b=DAYE_SanitizeCheckpointToken(config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_b);
   ENUM_TIMEFRAMES tf=DAYE_ResolveHostTimeframe(config.host_timeframe);
   return DAYE_SanitizeCheckpointToken(config.checkpoint_prefix) + "_" + a + "_" + b + "_TF" + IntegerToString((int)tf) + ".csv";
}

void DAYE_SkipCheckpointLine(const int handle)
{
   while(!FileIsEnding(handle) && !FileIsLineEnding(handle)) FileReadString(handle);
}

bool DAYE_SaveConfirmationCheckpoint(const DAYE_ConfirmationConfig &config,
                                     const datetime last_closed_host_open_utc,
                                     CDayeConfirmationStore &store,
                                     string &reason)
{
   reason="";
   if(!config.persist_checkpoint) return true;
   string filename=DAYE_BuildConfirmationCheckpointFilename(config);
   int handle=FileOpen(filename,FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_SHARE_READ,',');
   if(handle == INVALID_HANDLE)
   {
      reason="checkpoint_open_for_write_failed_" + IntegerToString(GetLastError());
      return false;
   }

   FileWrite(handle,"META",DAYE_CONFIRMATION_SCHEMA_VERSION,last_closed_host_open_utc);
   DAYE_ConfirmationCandidate candidates[];
   store.ExportCandidates(candidates);
   for(int i=0;i<ArraySize(candidates);i++)
   {
      FileWrite(handle,"CANDIDATE",
                candidates[i].schema_version,
                candidates[i].candidate_id,
                candidates[i].observation_id,
                candidates[i].opportunity_id,
                candidates[i].relationship_id,
                candidates[i].source_alias,
                candidates[i].is_major ? 1 : 0,
                candidates[i].chart_label,
                (int)candidates[i].side,
                (int)candidates[i].initial_pair_state,
                (int)candidates[i].last_pair_state,
                candidates[i].hunter_broker_symbol,
                candidates[i].hunter_canonical_symbol,
                candidates[i].protected_broker_symbol,
                candidates[i].protected_canonical_symbol,
                candidates[i].current_period_instance_id,
                candidates[i].reference_period_instance_id,
                candidates[i].hunter_reference_price,
                candidates[i].protected_reference_price,
                candidates[i].first_seen_event_time_utc,
                candidates[i].first_seen_availability_time_utc,
                candidates[i].last_seen_availability_time_utc,
                candidates[i].target_host_open_utc,
                candidates[i].target_host_close_utc,
                candidates[i].target_host_bar_id,
                candidates[i].update_count,
                candidates[i].is_replay_safe ? 1 : 0,
                (int)candidates[i].state,
                (int)candidates[i].status,
                candidates[i].reason_code);
   }

   string finalized[];
   store.ExportFinalizedIds(finalized);
   for(int i=0;i<ArraySize(finalized);i++) FileWrite(handle,"FINALIZED",finalized[i]);
   FileFlush(handle);
   FileClose(handle);
   return true;
}

bool DAYE_LoadConfirmationCheckpoint(const DAYE_ConfirmationConfig &config,
                                     datetime &last_closed_host_open_utc,
                                     CDayeConfirmationStore &store,
                                     int &restored_candidates,
                                     int &restored_finalized_ids,
                                     string &reason)
{
   reason="";
   restored_candidates=0;
   restored_finalized_ids=0;
   last_closed_host_open_utc=0;
   if(!config.persist_checkpoint) return true;
   string filename=DAYE_BuildConfirmationCheckpointFilename(config);
   if(!FileIsExist(filename,FILE_COMMON)) return true;
   int handle=FileOpen(filename,FILE_READ|FILE_CSV|FILE_COMMON|FILE_SHARE_READ|FILE_SHARE_WRITE,',');
   if(handle == INVALID_HANDLE)
   {
      reason="checkpoint_open_for_read_failed_" + IntegerToString(GetLastError());
      return false;
   }

   while(!FileIsEnding(handle))
   {
      string record_type=FileReadString(handle);
      if(record_type == "")
      {
         DAYE_SkipCheckpointLine(handle);
         continue;
      }
      if(record_type == "META")
      {
         int schema=(int)StringToInteger(FileReadString(handle));
         last_closed_host_open_utc=(datetime)StringToInteger(FileReadString(handle));
         if(schema != DAYE_CONFIRMATION_SCHEMA_VERSION)
         {
            FileClose(handle);
            reason="checkpoint_schema_version_mismatch";
            return false;
         }
         DAYE_SkipCheckpointLine(handle);
      }
      else if(record_type == "CANDIDATE")
      {
         DAYE_ConfirmationCandidate c;
         ZeroMemory(c);
         c.schema_version=(int)StringToInteger(FileReadString(handle));
         c.candidate_id=FileReadString(handle);
         c.observation_id=FileReadString(handle);
         c.opportunity_id=FileReadString(handle);
         c.relationship_id=FileReadString(handle);
         c.source_alias=FileReadString(handle);
         c.is_major=((int)StringToInteger(FileReadString(handle)) != 0);
         c.chart_label=FileReadString(handle);
         c.side=(DAYE_HuntSide)StringToInteger(FileReadString(handle));
         c.initial_pair_state=(DAYE_HuntPairState)StringToInteger(FileReadString(handle));
         c.last_pair_state=(DAYE_HuntPairState)StringToInteger(FileReadString(handle));
         c.hunter_broker_symbol=FileReadString(handle);
         c.hunter_canonical_symbol=FileReadString(handle);
         c.protected_broker_symbol=FileReadString(handle);
         c.protected_canonical_symbol=FileReadString(handle);
         c.current_period_instance_id=FileReadString(handle);
         c.reference_period_instance_id=FileReadString(handle);
         c.hunter_reference_price=StringToDouble(FileReadString(handle));
         c.protected_reference_price=StringToDouble(FileReadString(handle));
         c.first_seen_event_time_utc=(datetime)StringToInteger(FileReadString(handle));
         c.first_seen_availability_time_utc=(datetime)StringToInteger(FileReadString(handle));
         c.last_seen_availability_time_utc=(datetime)StringToInteger(FileReadString(handle));
         c.target_host_open_utc=(datetime)StringToInteger(FileReadString(handle));
         c.target_host_close_utc=(datetime)StringToInteger(FileReadString(handle));
         c.target_host_bar_id=FileReadString(handle);
         c.update_count=(int)StringToInteger(FileReadString(handle));
         c.is_replay_safe=((int)StringToInteger(FileReadString(handle)) != 0);
         c.state=(DAYE_ConfirmationCandidateState)StringToInteger(FileReadString(handle));
         c.status=(DAYE_ConfirmationStatus)StringToInteger(FileReadString(handle));
         c.reason_code=FileReadString(handle);
         DAYE_SkipCheckpointLine(handle);
         if(c.schema_version == DAYE_CONFIRMATION_SCHEMA_VERSION && c.state == DAYE_CONFIRM_CANDIDATE_PENDING)
         {
            if(store.AppendCandidate(c,config.maximum_pending_candidates)) restored_candidates++;
         }
      }
      else if(record_type == "FINALIZED")
      {
         string observation_id=FileReadString(handle);
         DAYE_SkipCheckpointLine(handle);
         if(store.RememberFinalizedObservation(observation_id,config.maximum_finalized_ids_to_remember)) restored_finalized_ids++;
      }
      else
      {
         DAYE_SkipCheckpointLine(handle);
      }
   }
   FileClose(handle);
   return true;
}

#endif
