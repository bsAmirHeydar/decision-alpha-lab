
#ifndef __EXP0018_DAYE_PERIOD_DIAGNOSTICS_MQH__
#define __EXP0018_DAYE_PERIOD_DIAGNOSTICS_MQH__

#include <DayeTrader/EXP0018/DAYE_PeriodEvents.mqh>

string DAYE_PeriodFormatDateTime(const datetime value)
{
   if(value <= 0) return "";
   return TimeToString(value,TIME_DATE|TIME_SECONDS);
}

string DAYE_FormatPeriodStoreSummary(const DAYE_PeriodStoreSummary &s)
{
   return StringFormat("EXP0018 P03 status=%s ready=%s complete=%s source_pairs=%d periods=%d complete_periods=%d partial=%d open=%d unavailable=%d daily=%d sessions=%d subcycles=%d latest_complete=%s reason=%s",
                       DAYE_PeriodAggregateStatusToString(s.status),
                       s.is_ready ? "true" : "false",
                       s.is_complete ? "true" : "false",
                       s.source_aligned_pairs,
                       s.paired_period_count,
                       s.complete_paired_period_count,
                       s.partial_paired_period_count,
                       s.open_paired_period_count,
                       s.unavailable_paired_period_count,
                       s.daily_period_count,
                       s.session_period_count,
                       s.subcycle_period_count,
                       s.latest_complete_paired_period_id,
                       s.reason_code);
}

string DAYE_FormatSymbolPeriod(const DAYE_SymbolPeriodSnapshot &s)
{
   return StringFormat("%s %s %s [%s -> %s] O=%.8f H=%.8f L=%.8f C=%.8f bars=%d/%d coverage=%.2f%% status=%s reason=%s",
                       s.canonical_symbol,
                       s.period_code,
                       DAYE_PeriodCompletenessToString(s.completeness),
                       DAYE_PeriodFormatDateTime(s.window.start_utc),
                       DAYE_PeriodFormatDateTime(s.window.end_utc),
                       s.open,s.high,s.low,s.close,
                       s.observed_bar_count,s.expected_bar_count,s.coverage_percent,
                       DAYE_PeriodAggregateStatusToString(s.status),s.reason_code);
}

string DAYE_FormatPairedPeriod(const DAYE_PairedPeriodSnapshot &p)
{
   return StringFormat("paired=%s code=%s completeness=%s aligned=%d/%d coverage=%.2f%% A=%s B=%s",
                       p.paired_period_id,p.period_code,DAYE_PeriodCompletenessToString(p.completeness),
                       p.aligned_bar_count,p.expected_aligned_bar_count,p.aligned_coverage_percent,
                       DAYE_PeriodCompletenessToString(p.symbol_a.completeness),
                       DAYE_PeriodCompletenessToString(p.symbol_b.completeness));
}

string DAYE_FormatPeriodAggregateEvent(const DAYE_PeriodAggregateEvent &e)
{
   return StringFormat("EXP0018 P03 event=%s id=%s event_utc=%s availability_utc=%s period=%s from=%s to=%s reason=%s",
                       DAYE_PeriodAggregateEventTypeToString(e.event_type),e.event_id,
                       DAYE_PeriodFormatDateTime(e.event_time_utc),DAYE_PeriodFormatDateTime(e.availability_time_utc),
                       e.period_instance_id,DAYE_PeriodAggregateStatusToString(e.from_status),
                       DAYE_PeriodAggregateStatusToString(e.to_status),e.reason_code);
}

#endif
