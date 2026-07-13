#ifndef __EXP0019_FP_I03_SESSION_CALENDAR_MQH__
#define __EXP0019_FP_I03_SESSION_CALENDAR_MQH__

#include "FP_I03_TimeMath.mqh"
#include "FP_I03_SessionRegistry.mqh"

bool FP_I03_DateAddDays(const datetime local_value,const int days,datetime &result)
  {
   MqlDateTime p;ZeroMemory(p);if(!TimeToStruct(local_value,p))return false;
   p.hour=0;p.min=0;p.sec=0;result=StructToTime(p)+(datetime)(days*86400);return true;
  }

string FP_I03_TradingDateKey(const datetime ny_time)
  {
   MqlDateTime p;ZeroMemory(p);if(!TimeToStruct(ny_time,p))return "";
   datetime date_midnight=0;FP_I03_DateAddDays(ny_time,(DAYE_SecondOfDay(ny_time)>=FP_I03_A_START ? 1 : 0),date_midnight);
   return DAYE_DateKey(date_midnight);
  }

bool FP_I03_BuildLocalForTradingDate(const string trading_date,const int day_offset,const int second_of_day,datetime &result)
  {
   string text=trading_date+" 00:00:00";datetime midnight=StringToTime(text);
   if(midnight<=0 || second_of_day<0 || second_of_day>=86400)return false;
   result=midnight+(datetime)(day_offset*86400+second_of_day);return true;
  }

bool FP_I03_ResolveBoundary(const datetime local_value,const FP_I03_LocalResolutionPolicy policy,const FP_I03_TimeKernelConfig &config,datetime &utc_value,string &reason)
  {
   FP_I03_LocalResolution r;if(!FP_I03_ResolveLocal(local_value,policy,config,r)){reason=r.reason_code;return false;}
   utc_value=r.selected_utc;reason=r.reason_code;return true;
  }

bool FP_I03_BuildTradingDay(const string trading_date,const FP_I03_TimeKernelConfig &config,FP_I03_TradingDayWindow &window,string &reason)
  {
   ZeroMemory(window);datetime start_ny=0,end_ny=0;
   if(!FP_I03_BuildLocalForTradingDate(trading_date,-1,FP_I03_A_START,start_ny) || !FP_I03_BuildLocalForTradingDate(trading_date,0,FP_I03_GAP_START,end_ny)){reason="FP_TRC_TRADING_DAY_LOCAL_FAILED";return false;}
   datetime start_utc=0,end_utc=0;string r1="",r2="";
   if(!FP_I03_ResolveBoundary(start_ny,config.ambiguous_start_policy,config,start_utc,r1) || !FP_I03_ResolveBoundary(end_ny,config.ambiguous_end_policy,config,end_utc,r2)){reason="FP_TRC_BOUNDARY_UNRESOLVED";return false;}
   window.trading_day_id="NYDAY-"+trading_date;window.trading_date=trading_date;window.start_ny=start_ny;window.end_ny=end_ny;window.start_utc=start_utc;window.end_utc=end_utc;
   window.elapsed_seconds=(int)((long)end_utc-(long)start_utc);
   window.window_id=FP_I02_CompactId("FPTDAY",window.trading_day_id+"|"+IntegerToString((long)start_utc)+"|"+IntegerToString((long)end_utc)+"|"+config.calendar_version);
   reason="FP_TRC_READY";return (end_utc>start_utc);
  }

bool FP_I03_BuildSession(const string trading_date,const FP_I03_CalendarSegment code,const datetime reference_utc,const FP_I03_TimeKernelConfig &config,FP_I03_SessionWindow &window,string &reason)
  {
   ZeroMemory(window);if(code!=FP_I03_SEGMENT_A && code!=FP_I03_SEGMENT_L && code!=FP_I03_SEGMENT_N){reason="FP_TRC_SESSION_CODE_INVALID";return false;}
   FP_I03_SessionDefinition d;FP_I03_BuildSessionDefinition(code,d);int start_offset=(code==FP_I03_SEGMENT_A ? -1 : 0);int end_offset=0;
   datetime start_ny=0,end_ny=0;if(!FP_I03_BuildLocalForTradingDate(trading_date,start_offset,d.start_second,start_ny) || !FP_I03_BuildLocalForTradingDate(trading_date,end_offset,d.end_second,end_ny)){reason="FP_TRC_SESSION_LOCAL_FAILED";return false;}
   datetime start_utc=0,end_utc=0;string r1="",r2="";
   if(!FP_I03_ResolveBoundary(start_ny,config.ambiguous_start_policy,config,start_utc,r1) || !FP_I03_ResolveBoundary(end_ny,config.ambiguous_end_policy,config,end_utc,r2)){reason="FP_TRC_BOUNDARY_UNRESOLVED";return false;}
   window.session_id="FPSESSION-"+trading_date+"-"+FP_I03_SegmentToString(code);window.session_code=code;window.trading_day_id="NYDAY-"+trading_date;window.trading_date=trading_date;
   window.start_ny=start_ny;window.end_ny=end_ny;window.start_utc=start_utc;window.end_utc=end_utc;window.elapsed_seconds=(int)((long)end_utc-(long)start_utc);
   window.contains_reference_time=(reference_utc>0 && reference_utc>=start_utc && reference_utc<end_utc);
   window.window_id=FP_I02_CompactId("FPSESS",window.session_id+"|"+IntegerToString((long)start_utc)+"|"+IntegerToString((long)end_utc)+"|"+config.session_registry_version);
   reason="FP_TRC_READY";return (end_utc>start_utc);
  }

bool FP_I03_BuildGap(const string trading_date,const FP_I03_TimeKernelConfig &config,datetime &start_utc,datetime &end_utc,string &reason)
  {
   datetime start_ny=0,end_ny=0;if(!FP_I03_BuildLocalForTradingDate(trading_date,0,FP_I03_GAP_START,start_ny) || !FP_I03_BuildLocalForTradingDate(trading_date,0,FP_I03_GAP_END,end_ny)){reason="FP_TRC_GAP_LOCAL_FAILED";return false;}
   string r1="",r2="";if(!FP_I03_ResolveBoundary(start_ny,config.ambiguous_start_policy,config,start_utc,r1) || !FP_I03_ResolveBoundary(end_ny,config.ambiguous_end_policy,config,end_utc,r2)){reason="FP_TRC_BOUNDARY_UNRESOLVED";return false;}
   reason="FP_TRC_READY";return true;
  }

#endif
