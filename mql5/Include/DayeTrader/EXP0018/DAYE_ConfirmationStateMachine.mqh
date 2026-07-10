#ifndef __EXP0018_DAYE_CONFIRMATION_STATE_MACHINE_MQH__
#define __EXP0018_DAYE_CONFIRMATION_STATE_MACHINE_MQH__

#include <DayeTrader/EXP0018/DAYE_HostCloseClock.mqh>

bool DAYE_ValidateConfirmationConfig(const DAYE_ConfirmationConfig &config,string &reason)
{
   reason="";
   if(config.schema_version != DAYE_CONFIRMATION_SCHEMA_VERSION)
   {
      reason="confirmation_schema_version_mismatch";
      return false;
   }
   if(config.maximum_pending_candidates < 1)
   {
      reason="maximum_pending_candidates_must_be_positive";
      return false;
   }
   if(config.maximum_results_to_publish < 1)
   {
      reason="maximum_results_to_publish_must_be_positive";
      return false;
   }
   if(config.maximum_finalized_ids_to_remember < config.maximum_results_to_publish)
   {
      reason="finalized_id_memory_must_cover_result_capacity";
      return false;
   }
   ENUM_TIMEFRAMES resolved=DAYE_ResolveHostTimeframe(config.host_timeframe);
   int host_seconds=PeriodSeconds(resolved);
   int base_seconds=PeriodSeconds(config.hunt_config.relationship_config.period_config.data_config.base_timeframe);
   if(host_seconds <= 0 || base_seconds <= 0)
   {
      reason="host_or_base_timeframe_has_no_fixed_seconds";
      return false;
   }
   if(host_seconds < base_seconds || (host_seconds % base_seconds) != 0)
   {
      reason="host_timeframe_must_be_an_integer_multiple_of_base_timeframe";
      return false;
   }
   if(config.checkpoint_prefix == "")
   {
      reason="checkpoint_prefix_empty";
      return false;
   }
   return true;
}

string DAYE_BuildConfirmationCandidateId(const string observation_id)
{
   return "EXP0018|P06|CANDIDATE|" + observation_id;
}

string DAYE_BuildConfirmationResultId(const string observation_id,const datetime host_close_utc)
{
   return "EXP0018|P06|RESULT|" + observation_id + "|" + IntegerToString((long)host_close_utc);
}

bool DAYE_ObservationMatchesCandidateRole(const DAYE_HuntObservation &observation,const DAYE_ConfirmationCandidate &candidate)
{
   return observation.hunter_canonical_symbol == candidate.hunter_canonical_symbol &&
          observation.protected_canonical_symbol == candidate.protected_canonical_symbol &&
          observation.pair_state == candidate.initial_pair_state;
}

bool DAYE_ResolveCandidateTarget(const DAYE_HuntObservation &observation,
                                 const DAYE_HostClockSnapshot &clock,
                                 const bool closed_advanced,
                                 const datetime previous_closed_close_utc,
                                 DAYE_HostBarPair &target,
                                 string &reason)
{
   reason="";
   ZeroMemory(target);
   if(!clock.is_ready)
   {
      reason="host_clock_not_ready";
      return false;
   }

   if(closed_advanced && observation.availability_time_utc > previous_closed_close_utc &&
      observation.availability_time_utc <= clock.latest_closed_bar.close_time_utc)
   {
      target=clock.latest_closed_bar;
      reason="transition_belongs_to_newly_closed_host_bar";
      return true;
   }

   if(observation.availability_time_utc > clock.latest_closed_bar.close_time_utc &&
      observation.availability_time_utc <= clock.current_open_bar.close_time_utc)
   {
      target=clock.current_open_bar;
      reason="transition_belongs_to_current_open_host_bar";
      return true;
   }

   reason="transition_not_inside_live_host_horizon_replay_required";
   return false;
}

bool DAYE_InitializeConfirmationCandidate(const DAYE_HuntObservation &observation,
                                          const DAYE_HostBarPair &target,
                                          DAYE_ConfirmationCandidate &candidate,
                                          string &reason)
{
   reason="";
   ZeroMemory(candidate);
   if(observation.status != DAYE_HUNT_STATUS_READY || !observation.is_publishable || !observation.is_one_sided)
   {
      reason="source_observation_not_ready_one_sided";
      return false;
   }
   if(!target.is_ready)
   {
      reason="target_host_bar_not_ready";
      return false;
   }

   candidate.schema_version=DAYE_CONFIRMATION_SCHEMA_VERSION;
   candidate.state=DAYE_CONFIRM_CANDIDATE_PENDING;
   candidate.status=DAYE_CONFIRM_STATUS_READY;
   candidate.reason_code="live_one_sided_transition_opened_candidate";
   candidate.is_replay_safe=observation.is_replay_safe && target.is_replay_safe;
   candidate.candidate_id=DAYE_BuildConfirmationCandidateId(observation.observation_id);
   candidate.observation_id=observation.observation_id;
   candidate.opportunity_id=observation.opportunity_id;
   candidate.relationship_id=observation.relationship_id;
   candidate.source_alias=observation.source_alias;
   candidate.is_major=observation.is_major;
   candidate.chart_label=observation.chart_label;
   candidate.side=observation.side;
   candidate.initial_pair_state=observation.pair_state;
   candidate.last_pair_state=observation.pair_state;
   candidate.hunter_broker_symbol=observation.hunter_broker_symbol;
   candidate.hunter_canonical_symbol=observation.hunter_canonical_symbol;
   candidate.protected_broker_symbol=observation.protected_broker_symbol;
   candidate.protected_canonical_symbol=observation.protected_canonical_symbol;
   candidate.current_period_instance_id=observation.current_period_instance_id;
   candidate.reference_period_instance_id=observation.reference_period_instance_id;
   if(observation.pair_state == DAYE_HUNT_PAIR_A_ONLY)
   {
      candidate.hunter_reference_price=observation.symbol_a.reference_price;
      candidate.protected_reference_price=observation.symbol_b.reference_price;
   }
   else
   {
      candidate.hunter_reference_price=observation.symbol_b.reference_price;
      candidate.protected_reference_price=observation.symbol_a.reference_price;
   }
   candidate.first_seen_event_time_utc=observation.event_time_utc;
   candidate.first_seen_availability_time_utc=observation.availability_time_utc;
   candidate.last_seen_availability_time_utc=observation.availability_time_utc;
   candidate.target_host_open_utc=target.open_time_utc;
   candidate.target_host_close_utc=target.close_time_utc;
   candidate.target_host_bar_id=target.host_bar_id;
   candidate.update_count=1;
   return true;
}

bool DAYE_UpdateConfirmationCandidate(const DAYE_HuntObservation &observation,
                                      DAYE_ConfirmationCandidate &candidate,
                                      bool &changed)
{
   changed=false;
   if(observation.observation_id != candidate.observation_id) return false;
   if(observation.availability_time_utc < candidate.last_seen_availability_time_utc) return true;
   if(observation.availability_time_utc > candidate.target_host_close_utc) return true;

   if(candidate.last_pair_state != observation.pair_state ||
      candidate.last_seen_availability_time_utc != observation.availability_time_utc)
      changed=true;
   candidate.last_pair_state=observation.pair_state;
   candidate.last_seen_availability_time_utc=observation.availability_time_utc;
   candidate.is_replay_safe=candidate.is_replay_safe && observation.is_replay_safe;
   candidate.update_count++;
   candidate.reason_code="candidate_updated_with_source_state_at_or_before_target_close";
   return true;
}

void DAYE_InitializeConfirmationResult(const DAYE_ConfirmationCandidate &candidate,
                                       const DAYE_HostBarPair &closed_bar,
                                       const datetime processing_time_utc,
                                       DAYE_ConfirmationResult &result)
{
   ZeroMemory(result);
   result.schema_version=DAYE_CONFIRMATION_SCHEMA_VERSION;
   result.status=DAYE_CONFIRM_STATUS_READY;
   result.outcome=DAYE_CONFIRM_OUTCOME_UNKNOWN;
   result.is_final=true;
   result.is_immutable=true;
   result.is_replay_safe=candidate.is_replay_safe && closed_bar.is_replay_safe;
   result.result_id=DAYE_BuildConfirmationResultId(candidate.observation_id,candidate.target_host_close_utc);
   result.candidate_id=candidate.candidate_id;
   result.observation_id=candidate.observation_id;
   result.opportunity_id=candidate.opportunity_id;
   result.relationship_id=candidate.relationship_id;
   result.source_alias=candidate.source_alias;
   result.is_major=candidate.is_major;
   result.chart_label=candidate.chart_label;
   result.side=candidate.side;
   result.initial_pair_state=candidate.initial_pair_state;
   result.close_pair_state=candidate.last_pair_state;
   result.hunter_broker_symbol=candidate.hunter_broker_symbol;
   result.hunter_canonical_symbol=candidate.hunter_canonical_symbol;
   result.protected_broker_symbol=candidate.protected_broker_symbol;
   result.protected_canonical_symbol=candidate.protected_canonical_symbol;
   result.current_period_instance_id=candidate.current_period_instance_id;
   result.reference_period_instance_id=candidate.reference_period_instance_id;
   result.hunter_reference_price=candidate.hunter_reference_price;
   result.protected_reference_price=candidate.protected_reference_price;
   result.candidate_first_seen_utc=candidate.first_seen_availability_time_utc;
   result.host_bar_open_utc=candidate.target_host_open_utc;
   result.host_bar_close_utc=candidate.target_host_close_utc;
   result.host_bar_id=candidate.target_host_bar_id;
   result.event_time_utc=candidate.target_host_close_utc;
   result.availability_time_utc=candidate.last_seen_availability_time_utc;
   if(result.availability_time_utc < candidate.target_host_close_utc)
      result.availability_time_utc=candidate.target_host_close_utc;
   result.processing_time_utc=processing_time_utc;
}

void DAYE_AttachHunterHostGeometry(const DAYE_ConfirmationCandidate &candidate,
                                   const DAYE_HostBarPair &closed_bar,
                                   DAYE_ConfirmationResult &result)
{
   DAYE_HostBarSnapshot hunter_bar;
   if(!DAYE_SelectHunterHostBar(closed_bar,candidate.hunter_canonical_symbol,hunter_bar))
      return;
   result.hunter_host_open=hunter_bar.open;
   result.hunter_host_high=hunter_bar.high;
   result.hunter_host_low=hunter_bar.low;
   result.hunter_host_close=hunter_bar.close;
   result.confirmation_endpoint_price=(candidate.side == DAYE_HUNT_SIDE_HIGH ? hunter_bar.high : hunter_bar.low);
}

bool DAYE_FinalizeCandidateAtClose(const DAYE_ConfirmationCandidate &candidate,
                                   const DAYE_HostBarPair &closed_bar,
                                   const datetime processing_time_utc,
                                   const bool close_was_missed,
                                   DAYE_ConfirmationResult &result)
{
   DAYE_InitializeConfirmationResult(candidate,closed_bar,processing_time_utc,result);

   if(close_was_missed || candidate.target_host_close_utc < closed_bar.close_time_utc)
   {
      result.outcome=DAYE_CONFIRM_OUTCOME_MISSED_CLOSE_REPLAY_REQUIRED;
      result.reason_code="candidate_target_close_was_not_processed_causally";
      return true;
   }
   if(candidate.target_host_close_utc != closed_bar.close_time_utc || candidate.target_host_bar_id != closed_bar.host_bar_id)
   {
      result.outcome=DAYE_CONFIRM_OUTCOME_UNAVAILABLE_AT_CLOSE;
      result.reason_code="closed_host_bar_identity_does_not_match_candidate_target";
      return true;
   }
   if(candidate.last_seen_availability_time_utc < candidate.target_host_close_utc)
   {
      result.outcome=DAYE_CONFIRM_OUTCOME_UNAVAILABLE_AT_CLOSE;
      result.reason_code="source_state_not_available_through_host_close";
      return true;
   }

   if(candidate.last_pair_state == DAYE_HUNT_PAIR_BOTH)
   {
      result.outcome=DAYE_CONFIRM_OUTCOME_INVALIDATED_DOUBLE_HUNT;
      result.reason_code="both_symbols_hunted_before_or_at_host_close";
      return true;
   }
   if(candidate.last_pair_state == DAYE_HUNT_PAIR_NONE)
   {
      result.outcome=DAYE_CONFIRM_OUTCOME_NO_SIGNAL_AT_CLOSE;
      result.reason_code="one_sided_state_not_present_at_host_close";
      return true;
   }
   if(candidate.last_pair_state == DAYE_HUNT_PAIR_UNAVAILABLE || candidate.last_pair_state == DAYE_HUNT_PAIR_UNKNOWN)
   {
      result.outcome=DAYE_CONFIRM_OUTCOME_UNAVAILABLE_AT_CLOSE;
      result.reason_code="pair_state_unavailable_at_host_close";
      return true;
   }
   if(candidate.last_pair_state != candidate.initial_pair_state)
   {
      result.outcome=DAYE_CONFIRM_OUTCOME_INVALIDATED_ROLE_CHANGED;
      result.reason_code="hunter_protected_role_changed_before_close";
      return true;
   }

   result.outcome=DAYE_CONFIRM_OUTCOME_CONFIRMED;
   result.is_confirmed=true;
   result.reason_code="one_sided_hunt_survived_through_first_host_close";
   DAYE_AttachHunterHostGeometry(candidate,closed_bar,result);
   if(result.confirmation_endpoint_price <= 0.0)
   {
      result.is_confirmed=false;
      result.outcome=DAYE_CONFIRM_OUTCOME_UNAVAILABLE_AT_CLOSE;
      result.reason_code="hunter_host_bar_geometry_unavailable";
   }
   return true;
}

#endif
