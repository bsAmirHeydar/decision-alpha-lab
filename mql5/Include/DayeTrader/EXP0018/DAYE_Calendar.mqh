#ifndef __EXP0018_DAYE_CALENDAR_MQH__
#define __EXP0018_DAYE_CALENDAR_MQH__

#include <DayeTrader/EXP0018/DAYE_Time.mqh>
#include <DayeTrader/EXP0018/DAYE_PeriodRegistry.mqh>

DAYE_PeriodId DAYE_ClassifySessionBySecond(const int second_of_day)
{
   if(second_of_day < 0 || second_of_day >= DAYE_SECONDS_PER_DAY)
      return DAYE_PERIOD_NONE;
   if(second_of_day >= 18*3600) return DAYE_PERIOD_A;
   if(second_of_day < 6*3600) return DAYE_PERIOD_L;
   if(second_of_day < 12*3600) return DAYE_PERIOD_N;
   if(second_of_day < 17*3600) return DAYE_PERIOD_P;
   return DAYE_PERIOD_NONE;
}

DAYE_PeriodId DAYE_ClassifySubcycleBySecond(const int s)
{
   if(s < 0 || s >= DAYE_SECONDS_PER_DAY)
      return DAYE_PERIOD_NONE;
   if(s >= 18*3600 && s < 19*3600+30*60) return DAYE_PERIOD_A1;
   if(s >= 19*3600+30*60 && s < 21*3600) return DAYE_PERIOD_A2;
   if(s >= 21*3600 && s < 22*3600+30*60) return DAYE_PERIOD_A3;
   if(s >= 22*3600+30*60) return DAYE_PERIOD_A4;

   if(s < 1*3600+30*60) return DAYE_PERIOD_L1;
   if(s < 3*3600) return DAYE_PERIOD_L2;
   if(s < 4*3600+30*60) return DAYE_PERIOD_L3;
   if(s < 6*3600) return DAYE_PERIOD_L4;

   if(s < 7*3600+30*60) return DAYE_PERIOD_N1;
   if(s < 9*3600) return DAYE_PERIOD_N2;
   if(s < 10*3600+30*60) return DAYE_PERIOD_N3;
   if(s < 12*3600) return DAYE_PERIOD_N4;

   if(s < 13*3600+30*60) return DAYE_PERIOD_P1;
   if(s < 15*3600) return DAYE_PERIOD_P2;
   if(s < 16*3600+30*60) return DAYE_PERIOD_P3;
   if(s < 17*3600) return DAYE_PERIOD_P4;
   return DAYE_PERIOD_NONE;
}

bool DAYE_IsDeclaredSessionGap(const int second_of_day)
{
   return (second_of_day >= 17*3600 && second_of_day < 18*3600);
}

bool DAYE_BuildTradingDayLocalBounds(const datetime new_york_time,datetime &start_ny,datetime &end_ny)
{
   int second_of_day = DAYE_SecondOfDay(new_york_time);
   if(second_of_day < 0)
      return false;
   int start_day_offset = (second_of_day >= 18*3600) ? 0 : -1;
   if(!DAYE_BuildCivilDateTime(new_york_time,start_day_offset,18*3600,start_ny))
      return false;
   end_ny = start_ny + 23*3600; // Civil wall-clock 18:00 → next-day 17:00.
   return true;
}

bool DAYE_BuildLocalBoundsForPeriod(const datetime new_york_time,const DAYE_PeriodDefinition &definition,datetime &start_ny,datetime &end_ny)
{
   if(new_york_time <= 0 || !definition.implementation_ready)
      return false;

   if(definition.id == DAYE_PERIOD_D)
      return DAYE_BuildTradingDayLocalBounds(new_york_time,start_ny,end_ny);

   int second_of_day = DAYE_SecondOfDay(new_york_time);
   if(second_of_day < 0)
      return false;

   if(definition.id == DAYE_PERIOD_GAP)
   {
      if(!DAYE_BuildCivilDateTime(new_york_time,0,17*3600,start_ny))
         return false;
      if(!DAYE_BuildCivilDateTime(new_york_time,0,18*3600,end_ny))
         return false;
      return true;
   }

   int start_second = definition.start_second;
   int end_second = definition.end_second;
   int start_day_offset = 0;
   int end_day_offset = 0;

   if(start_second >= DAYE_SECONDS_PER_DAY)
      return false;

   if(end_second == DAYE_SECONDS_PER_DAY)
      end_day_offset = 1;
   else if(definition.wraps_midnight || end_second <= start_second)
      end_day_offset = 1;

   if(!DAYE_BuildCivilDateTime(new_york_time,start_day_offset,start_second,start_ny))
      return false;

   int normalized_end_second = (end_second == DAYE_SECONDS_PER_DAY) ? 0 : end_second;
   if(!DAYE_BuildCivilDateTime(new_york_time,end_day_offset,normalized_end_second,end_ny))
      return false;
   return true;
}

string DAYE_BuildPeriodInstanceId(const DAYE_PeriodDefinition &definition,const datetime start_utc)
{
   return "EXP0018|" + DAYE_PeriodFamilyToString(definition.family) + "|" + definition.code + "|" + IntegerToString((long)start_utc);
}

DAYE_StatusCode DAYE_BuildPeriodWindow(const datetime new_york_time,const DAYE_TimeConfig &config,const DAYE_PeriodDefinition &definition,DAYE_PeriodWindow &window)
{
   ZeroMemory(window);
   window.schema_version = DAYE_TIME_SCHEMA_VERSION;
   window.period_id = definition.id;
   window.family = definition.family;
   window.code = definition.code;

   if(!definition.implementation_ready)
   {
      window.status = DAYE_STATUS_UNAVAILABLE;
      window.reason_code = definition.blocker;
      return window.status;
   }

   if(!DAYE_BuildLocalBoundsForPeriod(new_york_time,definition,window.start_ny,window.end_ny))
   {
      window.status = DAYE_STATUS_INVALID_INPUT;
      window.reason_code = "period_local_bounds_failed";
      return window.status;
   }

   string start_reason = "";
   string end_reason = "";
   DAYE_StatusCode start_status = DAYE_ResolveNewYorkLocalToUtc(window.start_ny,config,config.ambiguous_start_policy,window.start_utc,start_reason);
   DAYE_StatusCode end_status = DAYE_ResolveNewYorkLocalToUtc(window.end_ny,config,config.ambiguous_end_policy,window.end_utc,end_reason);
   if(start_status != DAYE_STATUS_OK)
   {
      window.status = start_status;
      window.reason_code = "start_" + start_reason;
      return window.status;
   }
   if(end_status != DAYE_STATUS_OK)
   {
      window.status = end_status;
      window.reason_code = "end_" + end_reason;
      return window.status;
   }

   if(window.end_utc <= window.start_utc)
   {
      window.status = DAYE_STATUS_INVALID_INPUT;
      window.reason_code = "period_utc_bounds_not_increasing";
      return window.status;
   }

   window.elapsed_minutes_utc = (int)(((long)window.end_utc - (long)window.start_utc) / 60);
   window.is_dst_variable_duration = (definition.nominal_duration_minutes > 0 && window.elapsed_minutes_utc != definition.nominal_duration_minutes);
   window.instance_id = DAYE_BuildPeriodInstanceId(definition,window.start_utc);
   window.status = DAYE_STATUS_OK;
   if(start_reason != "" || end_reason != "")
      window.reason_code = start_reason + ((start_reason != "" && end_reason != "") ? ";" : "") + end_reason;
   return window.status;
}

bool DAYE_BuildTimeSnapshot(const datetime broker_time,const DAYE_TimeConfig &config,const DAYE_PeriodDefinition &registry[],DAYE_TimeSnapshot &snapshot)
{
   ZeroMemory(snapshot);
   snapshot.schema_version = DAYE_TIME_SCHEMA_VERSION;
   snapshot.status = DAYE_STATUS_INVALID_INPUT;

   string config_reason = "";
   if(!DAYE_ValidateTimeConfig(config,config_reason))
   {
      snapshot.status = DAYE_STATUS_INVALID_CONFIG;
      snapshot.reason_code = config_reason;
      return false;
   }

   snapshot.broker_time = broker_time;
   string broker_reason = "";
   if(!DAYE_BrokerToUtc(broker_time,config,snapshot.utc_time,snapshot.broker_utc_offset_minutes,snapshot.is_replay_safe,broker_reason))
   {
      snapshot.status = DAYE_STATUS_UNAVAILABLE;
      snapshot.reason_code = broker_reason;
      return false;
   }

   string ny_reason = "";
   if(!DAYE_UtcToNewYork(snapshot.utc_time,config,snapshot.new_york_time,snapshot.is_new_york_dst,snapshot.new_york_utc_offset_minutes,snapshot.new_york_fold,ny_reason))
   {
      snapshot.status = DAYE_STATUS_UNAVAILABLE;
      snapshot.reason_code = ny_reason;
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
   if(!DAYE_FindPeriodDefinition(registry,DAYE_PERIOD_D,definition) || DAYE_BuildPeriodWindow(snapshot.new_york_time,config,definition,snapshot.trading_day_window) != DAYE_STATUS_OK)
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
      if(!DAYE_FindPeriodDefinition(registry,snapshot.session_id,definition) || DAYE_BuildPeriodWindow(snapshot.new_york_time,config,definition,snapshot.session_window) != DAYE_STATUS_OK)
      {
         snapshot.status = DAYE_STATUS_UNAVAILABLE;
         snapshot.reason_code = "session_window_failed:" + snapshot.session_window.reason_code;
         return false;
      }
      if(!DAYE_FindPeriodDefinition(registry,snapshot.subcycle_id,definition) || DAYE_BuildPeriodWindow(snapshot.new_york_time,config,definition,snapshot.subcycle_window) != DAYE_STATUS_OK)
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

#endif
