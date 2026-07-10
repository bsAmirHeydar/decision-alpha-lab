
#ifndef __EXP0018_DAYE_DATA_DIAGNOSTICS_MQH__
#define __EXP0018_DAYE_DATA_DIAGNOSTICS_MQH__

#include <DayeTrader/EXP0018/DAYE_DataEvents.mqh>

string DAYE_DataFormatDateTime(const datetime value)
{
   if(value <= 0)
      return "NA";
   return TimeToString(value,TIME_DATE|TIME_SECONDS);
}

string DAYE_FormatSymbolHealth(const DAYE_SymbolDataHealth &health)
{
   return "symbol=" + health.broker_symbol +
          " canonical=" + health.canonical_symbol +
          " status=" + DAYE_DataStatusCodeToString(health.status) +
          " sync=" + (health.series_synchronized ? "true" : "false") +
          " available=" + IntegerToString(health.bars_available) +
          " copied=" + IntegerToString(health.copied_bars) +
          " accepted=" + IntegerToString(health.accepted_bars) +
          " invalid=" + IntegerToString(health.invalid_bar_count) +
          " duplicate=" + IntegerToString(health.duplicate_timestamp_count) +
          " non_monotonic=" + IntegerToString(health.non_monotonic_count) +
          " first_utc=" + DAYE_DataFormatDateTime(health.first_event_time_utc) +
          " last_utc=" + DAYE_DataFormatDateTime(health.last_event_time_utc) +
          " age_s=" + IntegerToString(health.latest_closed_bar_age_seconds) +
          " reason=" + health.reason_code;
}

string DAYE_FormatDataSyncSummary(const DAYE_DataSyncSummary &summary)
{
   return "EXP0018 P02 status=" + DAYE_DataStatusCodeToString(summary.status) +
          " ready=" + (summary.is_ready ? "true" : "false") +
          " complete=" + (summary.is_complete ? "true" : "false") +
          " replay_safe=" + (summary.is_replay_safe ? "true" : "false") +
          " symbols=" + summary.broker_symbol_a + "/" + summary.broker_symbol_b +
          " tf=" + EnumToString(summary.timeframe) +
          " copied=" + IntegerToString(summary.copied_a) + "/" + IntegerToString(summary.copied_b) +
          " aligned=" + IntegerToString(summary.aligned_count) +
          " unmatched=" + IntegerToString(summary.unmatched_a) + "/" + IntegerToString(summary.unmatched_b) +
          " latest_utc=" + DAYE_DataFormatDateTime(summary.last_common_event_time_utc) +
          " reason=" + summary.reason_code;
}

string DAYE_FormatDataSyncEvent(const DAYE_DataSyncEvent &event)
{
   return "EXP0018 P02 event=" + DAYE_DataEventTypeToString(event.event_type) +
          " id=" + event.event_id +
          " event_utc=" + DAYE_DataFormatDateTime(event.event_time_utc) +
          " available_utc=" + DAYE_DataFormatDateTime(event.availability_time_utc) +
          " processing_utc=" + DAYE_DataFormatDateTime(event.processing_time_utc) +
          " from=" + DAYE_DataStatusCodeToString(event.from_status) +
          " to=" + DAYE_DataStatusCodeToString(event.to_status) +
          " reason=" + event.reason_code;
}

#endif
