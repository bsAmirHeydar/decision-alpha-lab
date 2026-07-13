#ifndef __EXP0019_FP_I03_IDENTITY_MQH__
#define __EXP0019_FP_I03_IDENTITY_MQH__

#include "FP_I03_WeekCalendar.mqh"

string FP_I03_SnapshotMaterial(const FP_I03_CalendarSnapshot &s)
  {
   return IntegerToString((long)s.reference_utc)+"|"+s.ny_timestamp.timestamp_id+"|"+s.trading_day.window_id+"|"+
          FP_I03_SegmentToString(s.segment)+"|"+(s.has_session?s.session.window_id:"")+"|"+s.week.window_id+"|"+
          s.config_hash+"|"+s.boundary_evidence_hash;
  }

#endif
