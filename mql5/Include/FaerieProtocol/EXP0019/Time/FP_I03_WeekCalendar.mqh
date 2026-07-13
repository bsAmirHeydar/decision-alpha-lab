#ifndef __EXP0019_FP_I03_WEEK_CALENDAR_MQH__
#define __EXP0019_FP_I03_WEEK_CALENDAR_MQH__

#include "FP_I03_SessionCalendar.mqh"

bool FP_I03_MostRecentSunday(const datetime ny_time,datetime &sunday_midnight)
  {
   MqlDateTime p;ZeroMemory(p);if(!TimeToStruct(ny_time,p))return false;
   int days_since_sunday=p.day_of_week; // Sunday=0 in MQL5.
   p.hour=0;p.min=0;p.sec=0;sunday_midnight=StructToTime(p)-(datetime)(days_since_sunday*86400);
   datetime sunday_open=sunday_midnight+(datetime)FP_I03_A_START;
   if(ny_time<sunday_open)sunday_midnight-=7*86400;
   return true;
  }

bool FP_I03_BuildWeek(const datetime sunday_midnight,const datetime reference_utc,const FP_I03_TimeKernelConfig &config,FP_I03_WeekWindow &window,string &reason)
  {
   ZeroMemory(window);MqlDateTime p;ZeroMemory(p);if(!TimeToStruct(sunday_midnight,p) || p.day_of_week!=0){reason="FP_TRC_WEEK_START_NOT_SUNDAY";return false;}
   datetime start_ny=sunday_midnight+(datetime)FP_I03_A_START;datetime end_ny=sunday_midnight+5*86400+(datetime)FP_I03_GAP_START;
   datetime start_utc=0,end_utc=0;string r1="",r2="";
   if(!FP_I03_ResolveBoundary(start_ny,config.ambiguous_start_policy,config,start_utc,r1) || !FP_I03_ResolveBoundary(end_ny,config.ambiguous_end_policy,config,end_utc,r2)){reason="FP_TRC_BOUNDARY_UNRESOLVED";return false;}
   window.start_date=DAYE_DateKey(sunday_midnight);window.end_date=DAYE_DateKey(sunday_midnight+5*86400);window.week_id="NYWEEK-"+window.start_date;
   window.start_ny=start_ny;window.end_ny=end_ny;window.start_utc=start_utc;window.end_utc=end_utc;window.elapsed_seconds=(int)((long)end_utc-(long)start_utc);
   window.contains_reference_time=(reference_utc>0 && reference_utc>=start_utc && reference_utc<end_utc);
   if(window.contains_reference_time)window.state=FP_I03_WEEK_ACTIVE;
   else if(reference_utc>=end_utc)window.state=FP_I03_WEEK_CLOSED_AFTER_FRIDAY;
   else window.state=FP_I03_WEEK_CLOSED_BEFORE_SUNDAY_OPEN;
   window.window_id=FP_I02_CompactId("FPWEEK",window.week_id+"|"+IntegerToString((long)start_utc)+"|"+IntegerToString((long)end_utc)+"|"+config.calendar_version);
   reason="FP_TRC_READY";return true;
  }

#endif
