#ifndef __EXP0018_DAYE_HUNT_DIAGNOSTICS_MQH__
#define __EXP0018_DAYE_HUNT_DIAGNOSTICS_MQH__

#include <DayeTrader/EXP0018/DAYE_HuntEvents.mqh>

string DAYE_FormatSymbolHuntFact(const DAYE_SymbolHuntFact &fact)
{
   return fact.canonical_symbol + "=" + DAYE_SymbolHuntStateToString(fact.state) +
          " ref=" + DoubleToString(fact.reference_price,8) +
          " current=" + DoubleToString(fact.current_extreme,8) +
          " penetration=" + DoubleToString(fact.signed_penetration,8) +
          " equality=" + IntegerToString(fact.touched_by_equality ? 1 : 0) +
          " reason=" + fact.reason_code;
}

string DAYE_FormatHuntObservation(const DAYE_HuntObservation &item)
{
   return "P05 observation status=" + DAYE_HuntObservationStatusToString(item.status) +
          " relationship=" + item.relationship_id +
          " side=" + DAYE_HuntSideToString(item.side) +
          " pair=" + DAYE_HuntPairStateToString(item.pair_state) +
          " hunter=" + item.hunter_canonical_symbol +
          " protected=" + item.protected_canonical_symbol +
          " current=" + item.current_period_code + ":" + item.current_period_instance_id +
          " reference=" + item.reference_period_code + ":" + item.reference_period_instance_id +
          " A[" + DAYE_FormatSymbolHuntFact(item.symbol_a) + "]" +
          " B[" + DAYE_FormatSymbolHuntFact(item.symbol_b) + "]" +
          " reason=" + item.reason_code;
}

string DAYE_FormatHuntSummary(const DAYE_HuntStoreSummary &summary)
{
   return "EXP0018 P05 status=" + DAYE_HuntObservationStatusToString(summary.status) +
          " ready=" + IntegerToString(summary.is_ready ? 1 : 0) +
          " complete=" + IntegerToString(summary.is_complete ? 1 : 0) +
          " source_resolutions=" + IntegerToString(summary.source_resolution_count) +
          " observations=" + IntegerToString(summary.observation_count) +
          " ready_observations=" + IntegerToString(summary.ready_observation_count) +
          " one_sided=" + IntegerToString(summary.one_sided_count) +
          " double=" + IntegerToString(summary.double_hunt_count) +
          " none=" + IntegerToString(summary.no_hunt_count) +
          " equality=" + IntegerToString(summary.equality_hunt_count) +
          " latest=" + summary.latest_observation_id +
          " reason=" + summary.reason_code;
}

string DAYE_FormatHuntEvent(const DAYE_HuntEvent &event)
{
   return "EXP0018 P05 event=" + DAYE_HuntEventTypeToString(event.event_type) +
          " id=" + event.event_id +
          " observation=" + event.observation_id +
          " relationship=" + event.relationship_id +
          " side=" + DAYE_HuntSideToString(event.side) +
          " from=" + DAYE_HuntPairStateToString(event.from_pair_state) +
          " to=" + DAYE_HuntPairStateToString(event.to_pair_state) +
          " reason=" + event.reason_code;
}

#endif
