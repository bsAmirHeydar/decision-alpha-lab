#ifndef __EXP0019_FP_I03_DIAGNOSTICS_MQH__
#define __EXP0019_FP_I03_DIAGNOSTICS_MQH__

#include "FP_I03_Calendar.mqh"

string FP_I03_DiagnosticLine(const FP_I03_CalendarSnapshot &s)
  {
   return "FP-I03|"+s.snapshot_id+"|NY="+s.ny_timestamp.local_iso+"|TD="+s.trading_day.trading_day_id+"|SEG="+FP_I03_SegmentToString(s.segment)+"|WEEK="+s.week.week_id+"|REASON="+s.reason_code;
  }

#endif
