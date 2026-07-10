#ifndef __EXP0018_DAYE_REPLAY_IDENTITY_MQH__
#define __EXP0018_DAYE_REPLAY_IDENTITY_MQH__

#include <DayeTrader/EXP0018/DAYE_ReplayTypes.mqh>

uint DAYE_ReplayHash32(const string value)
{
   uint hash=2166136261;
   for(int i=0;i<StringLen(value);i++)
   {
      hash^=(uint)StringGetCharacter(value,i);
      hash*=16777619;
   }
   return hash;
}

string DAYE_ReplayHashText(const string value)
{
   return StringFormat("%08X",DAYE_ReplayHash32(value));
}

string DAYE_ReplayAppendHash(const string previous_hash,const string canonical_row)
{
   return DAYE_ReplayHashText(previous_hash+"|"+canonical_row);
}

string DAYE_BuildReplayRunId(const DAYE_ReplayConfig &config,const datetime start_utc,const datetime end_utc)
{
   DAYE_DataSyncConfig data=config.lifecycle_config.confirmation_config.hunt_config.relationship_config.period_config.data_config;
   ENUM_TIMEFRAMES host=DAYE_ResolveHostTimeframe(config.lifecycle_config.confirmation_config.host_timeframe);
   string raw="EXP0018|P11|"+data.canonical_symbol_a+"|"+data.canonical_symbol_b+"|"+
              IntegerToString((int)data.base_timeframe)+"|"+IntegerToString((int)host)+"|"+
              IntegerToString((long)start_utc)+"|"+IntegerToString((long)end_utc);
   return raw+"|"+DAYE_ReplayHashText(raw);
}

string DAYE_BuildReplayEventId(const string run_id,const DAYE_ReplayEventType type,
                               const string subject_id,const datetime event_time_utc)
{
   string raw=run_id+"|"+IntegerToString((int)type)+"|"+subject_id+"|"+IntegerToString((long)event_time_utc);
   return "EXP0018|P11|EVENT|"+DAYE_ReplayHashText(raw);
}

string DAYE_ReplayCanonicalConfirmation(const DAYE_ConfirmationResult &result)
{
   return result.result_id+"|"+DAYE_ConfirmationOutcomeToString(result.outcome)+"|"+
          result.relationship_id+"|"+DAYE_HuntSideToString(result.side)+"|"+
          result.hunter_canonical_symbol+"|"+result.protected_canonical_symbol+"|"+
          IntegerToString((long)result.host_bar_close_utc);
}

string DAYE_ReplayCanonicalReference(const DAYE_ReferenceLifecycleRecord &record)
{
   return record.reference_id+"|"+DAYE_ReferenceLifecycleStateToString(record.state)+"|"+
          IntegerToString(record.accepted_use_count)+"|"+IntegerToString((long)record.retirement_event_time_utc);
}

string DAYE_ReplayCanonicalUse(const DAYE_ReferenceUseRecord &use)
{
   return use.use_id+"|"+DAYE_ReferenceUseStatusToString(use.status)+"|"+use.reference_id+"|"+
          use.relationship_id+"|"+IntegerToString((long)use.host_bar_close_utc);
}

#endif
