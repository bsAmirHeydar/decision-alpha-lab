#ifndef __EXP0018_DAYE_SESSION_BOX_GEOMETRY_MQH__
#define __EXP0018_DAYE_SESSION_BOX_GEOMETRY_MQH__

#include <DayeTrader/EXP0018/DAYE_SessionBoxPolicy.mqh>

bool DAYE_BuildSessionBoxGeometry(const DAYE_SymbolPeriodSnapshot &snapshot,
                                  const DAYE_TimeConfig &time_config,
                                  DAYE_SessionBoxGeometry &geometry,
                                  bool &replay_safe)
{
   ZeroMemory(geometry);
   replay_safe=snapshot.is_replay_safe;
   geometry.start_time_utc=snapshot.window.start_utc;
   geometry.end_time_utc=snapshot.window.end_utc;
   geometry.high_price=snapshot.high;
   geometry.low_price=snapshot.low;

   if(geometry.start_time_utc<=0 || geometry.end_time_utc<=geometry.start_time_utc)
   {
      geometry.reason_code="invalid_session_utc_window";
      return false;
   }
   if(geometry.high_price<=0.0 || geometry.low_price<=0.0 || geometry.high_price<geometry.low_price)
   {
      geometry.reason_code="invalid_symbol_local_session_range";
      return false;
   }

   string reason="";
   bool replay_safe_start=true,replay_safe_end=true;
   if(!DAYE_UtcToBrokerSessionBoxTime(geometry.start_time_utc,time_config,geometry.start_time_broker,replay_safe_start,reason))
   {
      geometry.reason_code="start_utc_to_broker_failed:"+reason;
      return false;
   }
   if(!DAYE_UtcToBrokerSessionBoxTime(geometry.end_time_utc,time_config,geometry.end_time_broker,replay_safe_end,reason))
   {
      geometry.reason_code="end_utc_to_broker_failed:"+reason;
      return false;
   }
   replay_safe=replay_safe && replay_safe_start && replay_safe_end;
   if(geometry.end_time_broker<=geometry.start_time_broker)
   {
      geometry.reason_code="broker_session_window_not_chronological";
      return false;
   }
   geometry.is_valid=true;
   geometry.reason_code="symbol_local_session_geometry_resolved";
   return true;
}

#endif
