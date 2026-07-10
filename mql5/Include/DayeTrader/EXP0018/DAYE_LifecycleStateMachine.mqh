#ifndef __EXP0018_DAYE_LIFECYCLE_STATE_MACHINE_MQH__
#define __EXP0018_DAYE_LIFECYCLE_STATE_MACHINE_MQH__

#include <DayeTrader/EXP0018/DAYE_LifecycleStore.mqh>

bool DAYE_IsValidConfirmedResult(const DAYE_ConfirmationResult &result,string &reason)
{
   reason="";
   if(!result.is_final || !result.is_confirmed || result.outcome!=DAYE_CONFIRM_OUTCOME_CONFIRMED)
   {
      reason="result_is_not_an_immutable_confirmation";
      return false;
   }
   if(result.result_id=="" || result.reference_period_instance_id=="" || result.opportunity_id=="")
   {
      reason="confirmed_result_identity_missing";
      return false;
   }
   if(result.side!=DAYE_HUNT_SIDE_HIGH && result.side!=DAYE_HUNT_SIDE_LOW)
   {
      reason="confirmed_result_side_invalid";
      return false;
   }
   if(result.hunter_canonical_symbol=="" || result.protected_canonical_symbol=="" ||
      result.hunter_canonical_symbol==result.protected_canonical_symbol)
   {
      reason="confirmed_result_roles_invalid";
      return false;
   }
   if(result.hunter_reference_price<=0.0 || result.protected_reference_price<=0.0)
   {
      reason="confirmed_result_reference_prices_invalid";
      return false;
   }
   return true;
}

void DAYE_AssignReferencePrices(const DAYE_LifecycleConfig &config,
                                const DAYE_ConfirmationResult &result,
                                DAYE_ReferenceLifecycleRecord &record)
{
   string a=config.confirmation_config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_a;
   string b=config.confirmation_config.hunt_config.relationship_config.period_config.data_config.canonical_symbol_b;
   record.canonical_symbol_a=a;
   record.canonical_symbol_b=b;
   record.broker_symbol_a=config.confirmation_config.hunt_config.relationship_config.period_config.data_config.broker_symbol_a;
   record.broker_symbol_b=config.confirmation_config.hunt_config.relationship_config.period_config.data_config.broker_symbol_b;
   if(result.hunter_canonical_symbol==a)
   {
      record.reference_price_a=result.hunter_reference_price;
      record.reference_price_b=result.protected_reference_price;
   }
   else
   {
      record.reference_price_a=result.protected_reference_price;
      record.reference_price_b=result.hunter_reference_price;
   }
}

bool DAYE_InitializeReferenceRecord(const DAYE_LifecycleConfig &config,
                                    const DAYE_ConfirmationResult &result,
                                    DAYE_ReferenceLifecycleRecord &record,
                                    string &reason)
{
   ZeroMemory(record);
   if(!DAYE_IsValidConfirmedResult(result,reason)) return false;
   record.schema_version=DAYE_LIFECYCLE_SCHEMA_VERSION;
   record.status=DAYE_LIFECYCLE_STATUS_READY;
   record.state=DAYE_REF_STATE_PROTECTED_SURVIVES;
   record.reason_code="first_confirmed_use_activated_reference";
   record.is_replay_safe=result.is_replay_safe;
   record.is_retired=false;
   record.is_immutable=false;
   record.reference_period_instance_id=result.reference_period_instance_id;
   record.side=result.side;
   DAYE_AssignReferencePrices(config,result,record);
   record.reference_id=DAYE_BuildReferenceLifecycleId(record.reference_period_instance_id,record.side,record.canonical_symbol_a,record.canonical_symbol_b);
   record.first_hunter_canonical_symbol=result.hunter_canonical_symbol;
   record.protected_canonical_symbol=result.protected_canonical_symbol;
   record.first_confirmation_result_id=result.result_id;
   record.latest_confirmation_result_id=result.result_id;
   record.latest_pair_state=result.close_pair_state;
   record.activation_event_time_utc=result.event_time_utc;
   record.activation_availability_time_utc=result.availability_time_utc;
   record.latest_use_event_time_utc=result.event_time_utc;
   record.latest_observation_availability_time_utc=result.availability_time_utc;
   record.accepted_use_count=0;
   record.duplicate_use_count=0;
   record.rejected_use_count=0;
   return true;
}

void DAYE_BuildUseRecord(const DAYE_ConfirmationResult &result,
                         const string reference_id,
                         const DAYE_ReferenceUseStatus status,
                         const string reason_code,
                         const datetime processing_time_utc,
                         DAYE_ReferenceUseRecord &use)
{
   ZeroMemory(use);
   use.schema_version=DAYE_LIFECYCLE_SCHEMA_VERSION;
   use.status=status;
   use.reason_code=reason_code;
   use.is_accepted=(status==DAYE_USE_STATUS_ACCEPTED);
   use.is_historical_immutable=use.is_accepted;
   use.is_replay_safe=result.is_replay_safe;
   use.use_id=DAYE_BuildReferenceUseId(result);
   use.exact_opportunity_use_key=DAYE_BuildExactOpportunityUseKey(result);
   use.reference_id=reference_id;
   use.result_id=result.result_id;
   use.candidate_id=result.candidate_id;
   use.observation_id=result.observation_id;
   use.opportunity_id=result.opportunity_id;
   use.relationship_id=result.relationship_id;
   use.source_alias=result.source_alias;
   use.is_major=result.is_major;
   use.chart_label=result.chart_label;
   use.side=result.side;
   use.hunter_broker_symbol=result.hunter_broker_symbol;
   use.hunter_canonical_symbol=result.hunter_canonical_symbol;
   use.protected_broker_symbol=result.protected_broker_symbol;
   use.protected_canonical_symbol=result.protected_canonical_symbol;
   use.current_period_instance_id=result.current_period_instance_id;
   use.reference_period_instance_id=result.reference_period_instance_id;
   use.hunter_reference_price=result.hunter_reference_price;
   use.protected_reference_price=result.protected_reference_price;
   use.host_bar_open_utc=result.host_bar_open_utc;
   use.host_bar_close_utc=result.host_bar_close_utc;
   use.host_bar_id=result.host_bar_id;
   use.hunter_host_open=result.hunter_host_open;
   use.hunter_host_high=result.hunter_host_high;
   use.hunter_host_low=result.hunter_host_low;
   use.hunter_host_close=result.hunter_host_close;
   use.confirmation_endpoint_price=result.confirmation_endpoint_price;
   use.event_time_utc=result.event_time_utc;
   use.availability_time_utc=result.availability_time_utc;
   use.processing_time_utc=processing_time_utc;
}

bool DAYE_ObservationMatchesReference(const DAYE_HuntObservation &observation,
                                      const DAYE_ReferenceLifecycleRecord &record)
{
   return observation.reference_period_instance_id==record.reference_period_instance_id &&
          observation.side==record.side;
}

bool DAYE_ProtectedSymbolHunted(const DAYE_HuntObservation &observation,
                               const DAYE_ReferenceLifecycleRecord &record)
{
   if(record.protected_canonical_symbol==observation.symbol_a.canonical_symbol)
      return observation.symbol_a.is_available && observation.symbol_a.is_hunted;
   if(record.protected_canonical_symbol==observation.symbol_b.canonical_symbol)
      return observation.symbol_b.is_available && observation.symbol_b.is_hunted;
   return false;
}

bool DAYE_ApplyObservationToReference(const DAYE_LifecycleConfig &config,
                                      const DAYE_HuntObservation &observation,
                                      DAYE_ReferenceLifecycleRecord &record,
                                      DAYE_ReferenceLifecycleState &from_state,
                                      DAYE_LifecycleEventType &event_type,
                                      string &reason)
{
   from_state=record.state;
   event_type=DAYE_LIFECYCLE_EVENT_NONE;
   reason="";
   if(record.is_retired || DAYE_IsReferenceRetiredState(record.state)) return false;
   if(!DAYE_ObservationMatchesReference(observation,record)) return false;
   if(observation.status!=DAYE_HUNT_STATUS_READY || observation.pair_state==DAYE_HUNT_PAIR_UNAVAILABLE) return false;
   if(observation.availability_time_utc<=record.latest_observation_availability_time_utc) return false;

   record.latest_observation_availability_time_utc=observation.availability_time_utc;
   record.latest_observation_id=observation.observation_id;
   record.latest_pair_state=observation.pair_state;

   bool protected_hunted=DAYE_ProtectedSymbolHunted(observation,record);
   if(!protected_hunted)
   {
      event_type=DAYE_LIFECYCLE_EVENT_REFERENCE_SURVIVED;
      reason="protected_symbol_remains_unhunted";
      record.reason_code=reason;
      return true;
   }

   DAYE_ReferenceLifecycleState retirement_state=DAYE_REF_STATE_RETIRED_PROTECTED_TOUCH;
   DAYE_LifecycleEventType retirement_event=DAYE_LIFECYCLE_EVENT_REFERENCE_RETIRED_PROTECTED_TOUCH;
   string retirement_reason="protected_symbol_touched_its_own_reference";

   if(config.retire_on_double_hunt && observation.pair_state==DAYE_HUNT_PAIR_BOTH)
   {
      retirement_state=DAYE_REF_STATE_RETIRED_DOUBLE_HUNT;
      retirement_event=DAYE_LIFECYCLE_EVENT_REFERENCE_RETIRED_DOUBLE_HUNT;
      retirement_reason="protected_touch_observed_as_double_hunt";
   }
   else if(config.retire_on_role_switch && observation.is_one_sided &&
           observation.hunter_canonical_symbol==record.protected_canonical_symbol)
   {
      retirement_state=DAYE_REF_STATE_RETIRED_ROLE_SWITCH;
      retirement_event=DAYE_LIFECYCLE_EVENT_REFERENCE_RETIRED_ROLE_SWITCH;
      retirement_reason="previously_protected_symbol_became_hunter_on_same_reference";
   }
   else if(!config.retire_on_protected_touch)
   {
      event_type=DAYE_LIFECYCLE_EVENT_REFERENCE_SURVIVED;
      reason="protected_touch_retirement_disabled_by_config";
      return true;
   }

   record.state=retirement_state;
   record.status=DAYE_LIFECYCLE_STATUS_READY;
   record.reason_code=retirement_reason;
   record.is_retired=true;
   record.is_immutable=true;
   record.retirement_event_time_utc=observation.event_time_utc;
   record.retirement_availability_time_utc=observation.availability_time_utc;
   record.retirement_evidence_id=observation.observation_id;
   event_type=retirement_event;
   reason=retirement_reason;
   return true;
}

#endif
