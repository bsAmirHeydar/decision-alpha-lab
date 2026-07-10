
#ifndef __EXP0018_DAYE_PERIOD_IDENTITY_MQH__
#define __EXP0018_DAYE_PERIOD_IDENTITY_MQH__

#include <DayeTrader/EXP0018/DAYE_Calendar.mqh>
#include <DayeTrader/EXP0018/DAYE_PeriodTypes.mqh>

int DAYE_PeriodLinkFamilyKey(const DAYE_PeriodFamily family)
{
   if(family == DAYE_FAMILY_DAILY) return 1;
   if(family == DAYE_FAMILY_SESSION) return 2;
   if(family == DAYE_FAMILY_SUBCYCLE_90M || family == DAYE_FAMILY_SUBCYCLE_TAIL) return 3;
   if(family == DAYE_FAMILY_WEEKLY) return 4;
   return 0;
}

int DAYE_PeriodSortRank(const DAYE_PeriodFamily family)
{
   if(family == DAYE_FAMILY_DAILY) return 1;
   if(family == DAYE_FAMILY_SESSION) return 2;
   if(family == DAYE_FAMILY_SUBCYCLE_90M || family == DAYE_FAMILY_SUBCYCLE_TAIL) return 3;
   if(family == DAYE_FAMILY_WEEKLY) return 4;
   return 9;
}

string DAYE_BuildSourceBarId(const DAYE_SymbolBar &bar)
{
   return "EXP0018|P02BAR|" + bar.canonical_symbol + "|" + EnumToString(bar.timeframe) + "|" + IntegerToString((long)bar.event_time_utc);
}

string DAYE_BuildSymbolPeriodSnapshotId(const DAYE_SymbolPeriodSnapshot &snapshot)
{
   return "EXP0018|P03|SYMBOL|" + snapshot.period_instance_id + "|" + snapshot.canonical_symbol;
}

string DAYE_BuildPairedPeriodId(const string period_instance_id,const string canonical_a,const string canonical_b)
{
   return "EXP0018|P03|PAIR|" + period_instance_id + "|" + canonical_a + "|" + canonical_b;
}

bool DAYE_BuildTimeSnapshotFromUtc(const datetime utc_time,
                                   const DAYE_TimeConfig &config,
                                   const DAYE_PeriodDefinition &registry[],
                                   DAYE_TimeSnapshot &snapshot)
{
   ZeroMemory(snapshot);
   snapshot.schema_version = DAYE_TIME_SCHEMA_VERSION;
   snapshot.utc_time = utc_time;
   snapshot.broker_time = 0;
   snapshot.is_replay_safe = true;

   string reason = "";
   if(!DAYE_UtcToNewYork(utc_time,
                         config,
                         snapshot.new_york_time,
                         snapshot.is_new_york_dst,
                         snapshot.new_york_utc_offset_minutes,
                         snapshot.new_york_fold,
                         reason))
   {
      snapshot.status = DAYE_STATUS_UNAVAILABLE;
      snapshot.reason_code = reason;
      return false;
   }

   snapshot.second_of_day_ny = DAYE_SecondOfDay(snapshot.new_york_time);
   if(snapshot.second_of_day_ny < 0)
   {
      snapshot.status = DAYE_STATUS_INVALID_INPUT;
      snapshot.reason_code = "second_of_day_failed";
      return false;
   }

   snapshot.minute_of_day_ny = snapshot.second_of_day_ny / 60;
   snapshot.new_york_date_key = DAYE_DateKey(snapshot.new_york_time);
   snapshot.trading_day_key = DAYE_TradingDayKeyNy(snapshot.new_york_time);
   snapshot.in_declared_session_gap = DAYE_IsDeclaredSessionGap(snapshot.second_of_day_ny);
   snapshot.session_id = DAYE_ClassifySessionBySecond(snapshot.second_of_day_ny);
   snapshot.subcycle_id = DAYE_ClassifySubcycleBySecond(snapshot.second_of_day_ny);

   DAYE_PeriodDefinition definition;
   if(!DAYE_FindPeriodDefinition(registry,DAYE_PERIOD_D,definition) ||
      DAYE_BuildPeriodWindow(snapshot.new_york_time,config,definition,snapshot.trading_day_window) != DAYE_STATUS_OK)
   {
      snapshot.status = DAYE_STATUS_UNAVAILABLE;
      snapshot.reason_code = "trading_day_window_failed:" + snapshot.trading_day_window.reason_code;
      return false;
   }

   if(snapshot.in_declared_session_gap)
   {
      if(DAYE_FindPeriodDefinition(registry,DAYE_PERIOD_GAP,definition))
         DAYE_BuildPeriodWindow(snapshot.new_york_time,config,definition,snapshot.session_window);
      snapshot.subcycle_window.status = DAYE_STATUS_UNAVAILABLE;
      snapshot.subcycle_window.reason_code = "no_subcycle_in_declared_gap";
   }
   else
   {
      if(!DAYE_FindPeriodDefinition(registry,snapshot.session_id,definition) ||
         DAYE_BuildPeriodWindow(snapshot.new_york_time,config,definition,snapshot.session_window) != DAYE_STATUS_OK)
      {
         snapshot.status = DAYE_STATUS_UNAVAILABLE;
         snapshot.reason_code = "session_window_failed:" + snapshot.session_window.reason_code;
         return false;
      }
      if(!DAYE_FindPeriodDefinition(registry,snapshot.subcycle_id,definition) ||
         DAYE_BuildPeriodWindow(snapshot.new_york_time,config,definition,snapshot.subcycle_window) != DAYE_STATUS_OK)
      {
         snapshot.status = DAYE_STATUS_UNAVAILABLE;
         snapshot.reason_code = "subcycle_window_failed:" + snapshot.subcycle_window.reason_code;
         return false;
      }
   }

   snapshot.status = DAYE_STATUS_OK;
   snapshot.reason_code = "";
   snapshot.is_valid = true;
   return true;
}

bool DAYE_PeriodWindowContainsBar(const DAYE_PeriodWindow &window,const DAYE_SymbolBar &bar)
{
   return (bar.event_time_utc >= window.start_utc && bar.event_time_utc < window.end_utc);
}

#endif
