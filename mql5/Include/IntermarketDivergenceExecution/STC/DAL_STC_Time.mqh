#ifndef __DAL_STC_TIME_MQH__
#define __DAL_STC_TIME_MQH__
#property strict

#include <IntermarketDivergenceExecution/STC/DAL_STC_Utils.mqh>

#define STC_MIN_20_00 1200
#define STC_DAY_ACTIVE_MINUTES 1170

int STC_ModInt(const int value, const int divisor)
{
   if(divisor == 0) return 0;
   int r = value % divisor;
   if(r < 0) r += divisor;
   return r;
}

datetime STC_MakeDateTime(const int year, const int month, const int day, const int hour, const int minute, const int second)
{
   MqlDateTime dt;
   dt.year = year;
   dt.mon = month;
   dt.day = day;
   dt.hour = hour;
   dt.min = minute;
   dt.sec = second;
   return StructToTime(dt);
}

string STC_YYYYMMDDFromTime(const datetime t)
{
   MqlDateTime dt;
   TimeToStruct(t, dt);
   return StringFormat("%04d%02d%02d", dt.year, dt.mon, dt.day);
}

int STC_DayOfWeek(const int year, const int month, const int day)
{
   datetime t = STC_MakeDateTime(year, month, day, 0, 0, 0);
   MqlDateTime dt;
   TimeToStruct(t, dt);
   return dt.day_of_week; // Sunday = 0 in MQL5.
}

int STC_NthSundayOfMonth(const int year, const int month, const int nth)
{
   int dow_first = STC_DayOfWeek(year, month, 1);
   int first_sunday = 1 + STC_ModInt(7 - dow_first, 7);
   return first_sunday + 7 * (nth - 1);
}

datetime STC_USDstStartUtc(const int year)
{
   int day = STC_NthSundayOfMonth(year, 3, 2);
   // New York DST starts at 02:00 local standard time = 07:00 UTC.
   return STC_MakeDateTime(year, 3, day, 7, 0, 0);
}

datetime STC_USDstEndUtc(const int year)
{
   int day = STC_NthSundayOfMonth(year, 11, 1);
   // New York DST ends at 02:00 local daylight time = 06:00 UTC.
   return STC_MakeDateTime(year, 11, day, 6, 0, 0);
}

bool STC_IsNewYorkDstUtc(const datetime utc_time)
{
   MqlDateTime u;
   TimeToStruct(utc_time, u);
   datetime start_utc = STC_USDstStartUtc(u.year);
   datetime end_utc = STC_USDstEndUtc(u.year);
   return (utc_time >= start_utc && utc_time < end_utc);
}

int STC_NewYorkUtcOffsetSeconds(const datetime utc_time)
{
   return STC_IsNewYorkDstUtc(utc_time) ? (-4 * 3600) : (-5 * 3600);
}

datetime STC_ServerToUtc(const datetime server_time, const double broker_utc_offset_hours)
{
   int offset_seconds = (int)MathRound(broker_utc_offset_hours * 3600.0);
   return (datetime)((long)server_time - offset_seconds);
}

datetime STC_UtcToNewYork(const datetime utc_time, int &ny_offset_seconds, bool &ny_dst)
{
   ny_dst = STC_IsNewYorkDstUtc(utc_time);
   ny_offset_seconds = ny_dst ? (-4 * 3600) : (-5 * 3600);
   return (datetime)((long)utc_time + ny_offset_seconds);
}

datetime STC_NewYorkMidnight(const datetime ny_time)
{
   MqlDateTime dt;
   TimeToStruct(ny_time, dt);
   return (datetime)((long)ny_time - (dt.hour * 3600 + dt.min * 60 + dt.sec));
}

int STC_NewYorkMinuteOfDay(const datetime ny_time)
{
   MqlDateTime dt;
   TimeToStruct(ny_time, dt);
   return dt.hour * 60 + dt.min;
}

void STC_AssignMCycle(STC_TimeSnapshot &snap)
{
   snap.m_cycle = STC_M_NONE;
   snap.w_cycle = STC_W_NONE;
   snap.m_start_elapsed_minutes = -1;
   snap.m_end_elapsed_minutes = -1;
   snap.w_start_elapsed_minutes = -1;
   snap.w_end_elapsed_minutes = -1;

   int e = snap.elapsed_minutes_from_2000;
   if(e >= 0 && e < 360)
   {
      snap.m_cycle = STC_M1;
      snap.m_start_elapsed_minutes = 0;
      snap.m_end_elapsed_minutes = 360;
      int w = e / 90;
      snap.w_cycle = (STC_WCycle)(w + 1);
      snap.w_start_elapsed_minutes = w * 90;
      snap.w_end_elapsed_minutes = snap.w_start_elapsed_minutes + 90;
   }
   else if(e >= 420 && e < 780)
   {
      snap.m_cycle = STC_M2;
      snap.m_start_elapsed_minutes = 420;
      snap.m_end_elapsed_minutes = 780;
      int w = (e - 420) / 90;
      snap.w_cycle = (STC_WCycle)(w + 1);
      snap.w_start_elapsed_minutes = 420 + w * 90;
      snap.w_end_elapsed_minutes = snap.w_start_elapsed_minutes + 90;
   }
   else if(e >= 810 && e < 1170)
   {
      snap.m_cycle = STC_M3;
      snap.m_start_elapsed_minutes = 810;
      snap.m_end_elapsed_minutes = 1170;
      int w = (e - 810) / 90;
      snap.w_cycle = (STC_WCycle)(w + 1);
      snap.w_start_elapsed_minutes = 810 + w * 90;
      snap.w_end_elapsed_minutes = snap.w_start_elapsed_minutes + 90;
   }
}

void STC_AssignPhase(STC_TimeSnapshot &snap)
{
   snap.inside_stc_day = (snap.elapsed_minutes_from_2000 >= 0 && snap.elapsed_minutes_from_2000 < STC_DAY_ACTIVE_MINUTES);
   snap.hard_close_due = (snap.elapsed_minutes_from_2000 >= STC_DAY_ACTIVE_MINUTES);
   snap.detection_allowed = false;
   snap.entry_allowed_now = false;
   snap.phase = STC_PHASE_PRE_DAY_OR_POST_CLOSE;
   snap.phase_reason = "outside_active_stc_day";

   if(snap.hard_close_due)
   {
      snap.phase = STC_PHASE_HARD_CLOSE_ZONE;
      snap.phase_reason = "ny_time_is_at_or_after_15_30_hard_close";
      return;
   }

   if(!snap.inside_stc_day)
      return;

   if(snap.m_cycle != STC_M_NONE)
   {
      snap.phase = STC_PHASE_ACTIVE_M;
      snap.phase_reason = "inside_active_M_cycle";
      snap.detection_allowed = true;
      snap.entry_allowed_now = true;
      return;
   }

   snap.phase = STC_PHASE_M_GAP;
   snap.phase_reason = "inside_M_gap_no_entry_no_detection";
}

void STC_AssignCheckCandle(STC_TimeSnapshot &snap, const int check_minutes)
{
   snap.check_minutes = check_minutes;
   snap.check_index = -1;
   snap.check_start_elapsed_minutes = -1;
   snap.check_end_elapsed_minutes = -1;
   snap.check_start_ny = 0;
   snap.check_end_ny = 0;
   snap.check_inside_active_m = false;
   snap.check_close_inside_m = false;
   snap.final_check_of_m = false;
   snap.check_entry_allowed_at_close = false;

   if(check_minutes <= 0 || snap.elapsed_minutes_from_2000 < 0)
      return;

   int e = snap.elapsed_minutes_from_2000;
   snap.check_index = e / check_minutes;
   snap.check_start_elapsed_minutes = snap.check_index * check_minutes;
   snap.check_end_elapsed_minutes = snap.check_start_elapsed_minutes + check_minutes;
   snap.check_start_ny = (datetime)((long)snap.stc_day_start_ny + snap.check_start_elapsed_minutes * 60);
   snap.check_end_ny = (datetime)((long)snap.stc_day_start_ny + snap.check_end_elapsed_minutes * 60);

   if(snap.m_cycle == STC_M_NONE)
      return;

   snap.check_inside_active_m = (snap.check_start_elapsed_minutes >= snap.m_start_elapsed_minutes && snap.check_start_elapsed_minutes < snap.m_end_elapsed_minutes);
   snap.check_close_inside_m = (snap.check_end_elapsed_minutes < snap.m_end_elapsed_minutes);
   snap.final_check_of_m = (snap.check_end_elapsed_minutes >= snap.m_end_elapsed_minutes);
   snap.check_entry_allowed_at_close = (snap.check_inside_active_m && snap.check_close_inside_m && !snap.final_check_of_m);
}

bool STC_BuildTimeSnapshot(STC_Config &cfg, const datetime server_time, STC_TimeSnapshot &snap)
{
   STC_ResetTimeSnapshot(snap);
   snap.server_time = server_time;
   snap.broker_utc_offset_seconds = (int)MathRound(cfg.broker_utc_offset_hours * 3600.0);
   snap.utc_time = STC_ServerToUtc(server_time, cfg.broker_utc_offset_hours);
   snap.ny_time = STC_UtcToNewYork(snap.utc_time, snap.ny_utc_offset_seconds, snap.ny_dst);

   MqlDateTime ny;
   TimeToStruct(snap.ny_time, ny);
   snap.ny_year = ny.year;
   snap.ny_month = ny.mon;
   snap.ny_day = ny.day;
   snap.ny_hour = ny.hour;
   snap.ny_minute = ny.min;
   snap.ny_second = ny.sec;

   datetime midnight = STC_NewYorkMidnight(snap.ny_time);
   int minute_of_day = STC_NewYorkMinuteOfDay(snap.ny_time);
   if(minute_of_day >= STC_MIN_20_00)
      snap.stc_day_start_ny = (datetime)((long)midnight + STC_MIN_20_00 * 60);
   else
      snap.stc_day_start_ny = (datetime)((long)midnight - 24 * 3600 + STC_MIN_20_00 * 60);

   snap.stc_day_end_ny = (datetime)((long)snap.stc_day_start_ny + STC_DAY_ACTIVE_MINUTES * 60);
   snap.stc_day_id = STC_YYYYMMDDFromTime(snap.stc_day_start_ny);
   snap.elapsed_seconds_from_2000 = (int)((long)snap.ny_time - (long)snap.stc_day_start_ny);
   snap.elapsed_minutes_from_2000 = snap.elapsed_seconds_from_2000 / 60;

   STC_AssignMCycle(snap);
   if(snap.m_cycle != STC_M_NONE)
   {
      snap.m_start_ny = (datetime)((long)snap.stc_day_start_ny + snap.m_start_elapsed_minutes * 60);
      snap.m_end_ny = (datetime)((long)snap.stc_day_start_ny + snap.m_end_elapsed_minutes * 60);
      snap.w_start_ny = (datetime)((long)snap.stc_day_start_ny + snap.w_start_elapsed_minutes * 60);
      snap.w_end_ny = (datetime)((long)snap.stc_day_start_ny + snap.w_end_elapsed_minutes * 60);
   }

   STC_AssignPhase(snap);
   STC_AssignCheckCandle(snap, cfg.check_minutes);
   return true;
}

string STC_TimeSnapshotOneLine(STC_TimeSnapshot &snap)
{
   return "server=" + STC_TimeText(snap.server_time)
      + "*utc=" + STC_TimeText(snap.utc_time)
      + "*ny=" + STC_TimeText(snap.ny_time)
      + "*nyDst=" + STC_BoolText(snap.ny_dst)
      + "*nyOffsetHours=" + DoubleToString((double)snap.ny_utc_offset_seconds / 3600.0, 1)
      + "*stcDay=" + snap.stc_day_id
      + "*elapsedMin=" + IntegerToString(snap.elapsed_minutes_from_2000)
      + "*phase=" + STC_TimePhaseText(snap.phase)
      + "*M=" + STC_MCycleText(snap.m_cycle)
      + "*W=" + STC_WCycleText(snap.w_cycle)
      + "*checkStart=" + STC_TimeText(snap.check_start_ny)
      + "*checkEnd=" + STC_TimeText(snap.check_end_ny)
      + "*finalCheck=" + STC_BoolText(snap.final_check_of_m)
      + "*checkEntryAllowed=" + STC_BoolText(snap.check_entry_allowed_at_close)
      + "*hardCloseDue=" + STC_BoolText(snap.hard_close_due);
}

#endif
