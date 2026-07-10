#ifndef __EXP0018_DAYE_TIME_MQH__
#define __EXP0018_DAYE_TIME_MQH__

#include <DayeTrader/EXP0018/DAYE_Types.mqh>

const int DAYE_SECONDS_PER_DAY = 86400;
const int DAYE_MINUTES_PER_DAY = 1440;
const int DAYE_TRADING_DAY_START_SECOND_NY = 18 * 3600;
const int DAYE_TRADING_DAY_END_SECOND_NY = 17 * 3600;

bool DAYE_TimeToParts(const datetime value,MqlDateTime &parts)
{
   ZeroMemory(parts);
   if(value <= 0)
      return false;
   return TimeToStruct(value,parts);
}

bool DAYE_SameCivilSecond(const datetime left,const datetime right)
{
   MqlDateTime a;
   MqlDateTime b;
   if(!DAYE_TimeToParts(left,a) || !DAYE_TimeToParts(right,b))
      return false;
   return (a.year == b.year &&
           a.mon == b.mon &&
           a.day == b.day &&
           a.hour == b.hour &&
           a.min == b.min &&
           a.sec == b.sec);
}

datetime DAYE_ShiftMinutes(const datetime source_time,const int minutes)
{
   return source_time + (datetime)((long)minutes * 60);
}

datetime DAYE_ShiftSeconds(const datetime source_time,const int seconds)
{
   return source_time + (datetime)seconds;
}

int DAYE_FirstSundayDayOfMonth(const int year,const int month)
{
   MqlDateTime first_day;
   ZeroMemory(first_day);
   first_day.year = year;
   first_day.mon = month;
   first_day.day = 1;
   datetime first_time = StructToTime(first_day);
   MqlDateTime normalized;
   ZeroMemory(normalized);
   if(!TimeToStruct(first_time,normalized))
      return -1;
   int days_until_sunday = (7 - normalized.day_of_week) % 7;
   return 1 + days_until_sunday;
}

datetime DAYE_NewYorkDstStartUtc(const int year)
{
   int first_sunday = DAYE_FirstSundayDayOfMonth(year,3);
   if(first_sunday < 1)
      return 0;
   MqlDateTime value;
   ZeroMemory(value);
   value.year = year;
   value.mon = 3;
   value.day = first_sunday + 7;
   value.hour = 7; // 02:00 EST = 07:00 UTC.
   return StructToTime(value);
}

datetime DAYE_NewYorkDstEndUtc(const int year)
{
   int first_sunday = DAYE_FirstSundayDayOfMonth(year,11);
   if(first_sunday < 1)
      return 0;
   MqlDateTime value;
   ZeroMemory(value);
   value.year = year;
   value.mon = 11;
   value.day = first_sunday;
   value.hour = 6; // 02:00 EDT = 06:00 UTC.
   return StructToTime(value);
}

bool DAYE_IsNewYorkDstUtc(const datetime utc_time)
{
   MqlDateTime value;
   if(!DAYE_TimeToParts(utc_time,value))
      return false;
   datetime start_utc = DAYE_NewYorkDstStartUtc(value.year);
   datetime end_utc = DAYE_NewYorkDstEndUtc(value.year);
   return (start_utc > 0 && end_utc > 0 && utc_time >= start_utc && utc_time < end_utc);
}

int DAYE_NewYorkFoldForUtc(const datetime utc_time)
{
   MqlDateTime value;
   if(!DAYE_TimeToParts(utc_time,value))
      return 0;
   datetime end_utc = DAYE_NewYorkDstEndUtc(value.year);
   if(end_utc > 0 && utc_time >= end_utc && utc_time < end_utc + 3600)
      return 1; // Second occurrence of the repeated 01:xx hour.
   return 0;
}

int DAYE_ResolveNewYorkUtcOffsetMinutes(const datetime utc_time,const DAYE_TimeConfig &config,bool &is_dst)
{
   if(config.ny_offset_mode == DAYE_NY_MANUAL_UTC_OFFSET)
   {
      is_dst = (config.manual_new_york_utc_offset_minutes == -240);
      return config.manual_new_york_utc_offset_minutes;
   }

   is_dst = DAYE_IsNewYorkDstUtc(utc_time);
   return is_dst ? -240 : -300;
}

bool DAYE_ValidateTimeConfig(const DAYE_TimeConfig &config,string &reason_code)
{
   reason_code = "";
   if(config.schema_version != DAYE_TIME_SCHEMA_VERSION)
   {
      reason_code = "schema_version_mismatch";
      return false;
   }
   if(config.broker_utc_offset_minutes < -840 || config.broker_utc_offset_minutes > 840)
   {
      reason_code = "broker_offset_out_of_range";
      return false;
   }
   if(config.manual_new_york_utc_offset_minutes < -840 || config.manual_new_york_utc_offset_minutes > 840)
   {
      reason_code = "manual_ny_offset_out_of_range";
      return false;
   }
   if(config.ambiguous_start_policy == DAYE_LOCAL_REJECT || config.ambiguous_end_policy == DAYE_LOCAL_REJECT)
   {
      // Valid but period-window construction can reject repeated local boundaries.
   }
   return true;
}

int DAYE_DetectCurrentBrokerUtcOffsetMinutes(bool &available)
{
   available = false;
   datetime broker_now = TimeTradeServer();
   if(broker_now <= 0)
      broker_now = TimeCurrent();
   datetime utc_now = TimeGMT();
   if(broker_now <= 0 || utc_now <= 0)
      return 0;
   long difference_seconds = (long)broker_now - (long)utc_now;
   available = true;
   return (int)MathRound((double)difference_seconds / 60.0);
}

bool DAYE_ResolveBrokerOffsetMinutes(const DAYE_TimeConfig &config,int &offset_minutes,bool &replay_safe,string &reason_code)
{
   reason_code = "";
   replay_safe = true;
   if(config.broker_offset_mode == DAYE_BROKER_OFFSET_MANUAL_FIXED)
   {
      offset_minutes = config.broker_utc_offset_minutes;
      return true;
   }

   bool available = false;
   offset_minutes = DAYE_DetectCurrentBrokerUtcOffsetMinutes(available);
   replay_safe = false;
   if(!available)
   {
      reason_code = "auto_broker_offset_unavailable";
      return false;
   }
   return true;
}

bool DAYE_BrokerToUtc(const datetime broker_time,const DAYE_TimeConfig &config,datetime &utc_time,int &resolved_broker_offset,bool &replay_safe,string &reason_code)
{
   reason_code = "";
   if(broker_time <= 0)
   {
      reason_code = "invalid_broker_time";
      return false;
   }
   if(!DAYE_ResolveBrokerOffsetMinutes(config,resolved_broker_offset,replay_safe,reason_code))
      return false;
   utc_time = DAYE_ShiftMinutes(broker_time,-resolved_broker_offset);
   return true;
}

bool DAYE_UtcToNewYork(const datetime utc_time,const DAYE_TimeConfig &config,datetime &new_york_time,bool &is_dst,int &offset_minutes,int &fold,string &reason_code)
{
   reason_code = "";
   if(utc_time <= 0)
   {
      reason_code = "invalid_utc_time";
      return false;
   }
   offset_minutes = DAYE_ResolveNewYorkUtcOffsetMinutes(utc_time,config,is_dst);
   new_york_time = DAYE_ShiftMinutes(utc_time,offset_minutes);
   fold = (config.ny_offset_mode == DAYE_NY_AUTO_US_DST) ? DAYE_NewYorkFoldForUtc(utc_time) : 0;
   return true;
}

int DAYE_SecondOfDay(const datetime time_value)
{
   MqlDateTime value;
   if(!DAYE_TimeToParts(time_value,value))
      return -1;
   return value.hour * 3600 + value.min * 60 + value.sec;
}

string DAYE_DateKey(const datetime time_value)
{
   MqlDateTime value;
   if(!DAYE_TimeToParts(time_value,value))
      return "";
   return StringFormat("%04d-%02d-%02d",value.year,value.mon,value.day);
}

string DAYE_TradingDayKeyNy(const datetime new_york_time)
{
   if(new_york_time <= 0)
      return "";
   datetime anchored = DAYE_ShiftSeconds(new_york_time,-DAYE_TRADING_DAY_START_SECOND_NY);
   return DAYE_DateKey(anchored);
}

bool DAYE_BuildCivilDateTime(const datetime reference_local,const int day_offset,const int second_of_day,datetime &result)
{
   if(reference_local <= 0 || second_of_day < 0 || second_of_day >= DAYE_SECONDS_PER_DAY)
      return false;
   MqlDateTime parts;
   if(!DAYE_TimeToParts(reference_local,parts))
      return false;
   parts.hour = 0;
   parts.min = 0;
   parts.sec = 0;
   datetime midnight = StructToTime(parts);
   result = midnight + (datetime)((long)day_offset * DAYE_SECONDS_PER_DAY + second_of_day);
   return true;
}

int DAYE_CollectUtcCandidatesForNyLocal(const datetime local_ny,const DAYE_TimeConfig &config,datetime &candidates[])
{
   ArrayResize(candidates,0);
   if(local_ny <= 0)
      return 0;

   if(config.ny_offset_mode == DAYE_NY_MANUAL_UTC_OFFSET)
   {
      ArrayResize(candidates,1);
      candidates[0] = DAYE_ShiftMinutes(local_ny,-config.manual_new_york_utc_offset_minutes);
      return 1;
   }

   int offsets[2];
   offsets[0] = -240;
   offsets[1] = -300;
   for(int i=0;i<2;i++)
   {
      datetime candidate_utc = DAYE_ShiftMinutes(local_ny,-offsets[i]);
      datetime roundtrip_ny = 0;
      bool is_dst = false;
      int resolved_offset = 0;
      int fold = 0;
      string reason = "";
      if(!DAYE_UtcToNewYork(candidate_utc,config,roundtrip_ny,is_dst,resolved_offset,fold,reason))
         continue;
      if(!DAYE_SameCivilSecond(local_ny,roundtrip_ny))
         continue;
      int index = ArraySize(candidates);
      ArrayResize(candidates,index + 1);
      candidates[index] = candidate_utc;
   }

   if(ArraySize(candidates) == 2 && candidates[0] > candidates[1])
   {
      datetime temp = candidates[0];
      candidates[0] = candidates[1];
      candidates[1] = temp;
   }
   return ArraySize(candidates);
}

DAYE_StatusCode DAYE_ResolveNewYorkLocalToUtc(const datetime local_ny,const DAYE_TimeConfig &config,const DAYE_LocalResolutionPolicy policy,datetime &utc_result,string &reason_code)
{
   reason_code = "";
   utc_result = 0;
   datetime candidates[];
   int count = DAYE_CollectUtcCandidatesForNyLocal(local_ny,config,candidates);
   if(count == 0)
   {
      reason_code = "ny_local_time_does_not_exist";
      return DAYE_STATUS_NONEXISTENT_LOCAL_TIME;
   }
   if(count == 1)
   {
      utc_result = candidates[0];
      return DAYE_STATUS_OK;
   }
   if(policy == DAYE_LOCAL_EARLIEST)
   {
      utc_result = candidates[0];
      reason_code = "ambiguous_resolved_earliest";
      return DAYE_STATUS_OK;
   }
   if(policy == DAYE_LOCAL_LATEST)
   {
      utc_result = candidates[count - 1];
      reason_code = "ambiguous_resolved_latest";
      return DAYE_STATUS_OK;
   }
   reason_code = "ny_local_time_is_ambiguous";
   return DAYE_STATUS_AMBIGUOUS_LOCAL_TIME;
}

#endif
