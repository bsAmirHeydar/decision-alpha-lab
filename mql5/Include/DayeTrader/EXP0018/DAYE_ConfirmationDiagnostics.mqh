#ifndef __EXP0018_DAYE_CONFIRMATION_DIAGNOSTICS_MQH__
#define __EXP0018_DAYE_CONFIRMATION_DIAGNOSTICS_MQH__

#include <DayeTrader/EXP0018/DAYE_ConfirmationEvents.mqh>

string DAYE_FormatConfirmationCandidate(const DAYE_ConfirmationCandidate &item)
{
   return "P06 candidate id=" + item.candidate_id +
          " relationship=" + item.relationship_id +
          " side=" + DAYE_HuntSideToString(item.side) +
          " initial=" + DAYE_HuntPairStateToString(item.initial_pair_state) +
          " last=" + DAYE_HuntPairStateToString(item.last_pair_state) +
          " hunter=" + item.hunter_canonical_symbol +
          " protected=" + item.protected_canonical_symbol +
          " target_close=" + TimeToString(item.target_host_close_utc,TIME_DATE|TIME_SECONDS) +
          " updates=" + IntegerToString(item.update_count) +
          " reason=" + item.reason_code;
}

string DAYE_FormatConfirmationResult(const DAYE_ConfirmationResult &item)
{
   return "P06 result id=" + item.result_id +
          " outcome=" + DAYE_ConfirmationOutcomeToString(item.outcome) +
          " relationship=" + item.relationship_id +
          " side=" + DAYE_HuntSideToString(item.side) +
          " hunter=" + item.hunter_canonical_symbol +
          " protected=" + item.protected_canonical_symbol +
          " host_close=" + TimeToString(item.host_bar_close_utc,TIME_DATE|TIME_SECONDS) +
          " ref=" + DoubleToString(item.hunter_reference_price,8) +
          " endpoint=" + DoubleToString(item.confirmation_endpoint_price,8) +
          " reason=" + item.reason_code;
}

string DAYE_FormatConfirmationSummary(const DAYE_ConfirmationStoreSummary &summary)
{
   return "EXP0018 P06 status=" + DAYE_ConfirmationStatusToString(summary.status) +
          " ready=" + IntegerToString(summary.is_ready ? 1 : 0) +
          " baselined=" + IntegerToString(summary.source_baselined ? 1 : 0) +
          " checkpoint=" + IntegerToString(summary.checkpoint_restored ? 1 : 0) +
          " pending=" + IntegerToString(summary.pending_candidate_count) +
          " results=" + IntegerToString(summary.result_count) +
          " confirmed=" + IntegerToString(summary.confirmed_count) +
          " double=" + IntegerToString(summary.invalidated_double_hunt_count) +
          " no_signal=" + IntegerToString(summary.no_signal_count) +
          " unavailable=" + IntegerToString(summary.unavailable_count) +
          " missed=" + IntegerToString(summary.missed_close_count) +
          " latest=" + summary.latest_result_id +
          " reason=" + summary.reason_code;
}

string DAYE_FormatConfirmationEvent(const DAYE_ConfirmationEvent &event)
{
   return "EXP0018 P06 event=" + DAYE_ConfirmationEventTypeToString(event.event_type) +
          " id=" + event.event_id +
          " candidate=" + event.candidate_id +
          " result=" + event.result_id +
          " relationship=" + event.relationship_id +
          " side=" + DAYE_HuntSideToString(event.side) +
          " outcome=" + DAYE_ConfirmationOutcomeToString(event.outcome) +
          " reason=" + event.reason_code;
}

#endif
