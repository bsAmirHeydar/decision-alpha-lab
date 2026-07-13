#ifndef __EXP0019_FP_I03_CALENDAR_MQH__
#define __EXP0019_FP_I03_CALENDAR_MQH__

#include "FP_I03_Identity.mqh"

bool FP_I03_BuildSnapshot(const datetime reference_utc,const FP_I03_TimeKernelConfig &config,FP_I03_CalendarSnapshot &snapshot,string &reason)
  {
   ZeroMemory(snapshot);snapshot.reference_utc=reference_utc;snapshot.config_hash=config.config_hash;
   if(!FP_I03_UtcToNewYork(reference_utc,config,snapshot.ny_timestamp,reason)){snapshot.health=FP_I03_HEALTH_BLOCKED;return false;}
   string trading_date=FP_I03_TradingDateKey(snapshot.ny_timestamp.ny_time);
   if(!FP_I03_BuildTradingDay(trading_date,config,snapshot.trading_day,reason)){snapshot.health=FP_I03_HEALTH_BLOCKED;return false;}
   if(!FP_I03_BuildGap(trading_date,config,snapshot.daily_gap_start_utc,snapshot.daily_gap_end_utc,reason)){snapshot.health=FP_I03_HEALTH_BLOCKED;return false;}
   datetime sunday=0;if(!FP_I03_MostRecentSunday(snapshot.ny_timestamp.ny_time,sunday) || !FP_I03_BuildWeek(sunday,reference_utc,config,snapshot.week,reason)){snapshot.health=FP_I03_HEALTH_BLOCKED;return false;}
   FP_I03_CalendarSegment intraday=FP_I03_ClassifyIntraday(snapshot.ny_timestamp.second_of_day);
   snapshot.segment=snapshot.week.contains_reference_time ? intraday : FP_I03_SEGMENT_WEEKEND_CLOSED;
   snapshot.has_session=false;
   if(snapshot.segment==FP_I03_SEGMENT_A || snapshot.segment==FP_I03_SEGMENT_L || snapshot.segment==FP_I03_SEGMENT_N)
     {
      if(!FP_I03_BuildSession(trading_date,snapshot.segment,reference_utc,config,snapshot.session,reason)){snapshot.health=FP_I03_HEALTH_BLOCKED;return false;}
      if(!snapshot.session.contains_reference_time){reason="FP_TRC_SESSION_OWNERSHIP_MISMATCH";snapshot.health=FP_I03_HEALTH_BLOCKED;return false;}
      snapshot.has_session=true;
     }
   snapshot.reason_code=(snapshot.segment==FP_I03_SEGMENT_A?"FP_TRC_SESSION_A":snapshot.segment==FP_I03_SEGMENT_L?"FP_TRC_SESSION_L":snapshot.segment==FP_I03_SEGMENT_N?"FP_TRC_SESSION_N":snapshot.segment==FP_I03_SEGMENT_DAILY_GAP?"FP_TRC_DAILY_GAP":"FP_TRC_WEEKEND_CLOSED");
   snapshot.boundary_evidence_hash=FP_I02_SHA256(snapshot.trading_day.window_id+"|"+snapshot.week.window_id+"|"+(snapshot.has_session?snapshot.session.window_id:"")+"|"+IntegerToString((long)snapshot.daily_gap_start_utc)+"|"+IntegerToString((long)snapshot.daily_gap_end_utc));
   snapshot.snapshot_id=FP_I02_CompactId("FPCAL",FP_I03_SnapshotMaterial(snapshot));snapshot.health=FP_I03_HEALTH_READY;reason=snapshot.reason_code;return true;
  }

#endif
