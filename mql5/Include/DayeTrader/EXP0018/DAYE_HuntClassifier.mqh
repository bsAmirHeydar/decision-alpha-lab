#ifndef __EXP0018_DAYE_HUNT_CLASSIFIER_MQH__
#define __EXP0018_DAYE_HUNT_CLASSIFIER_MQH__

#include <DayeTrader/EXP0018/DAYE_HuntTypes.mqh>

bool DAYE_ValidateHuntConfig(const DAYE_HuntConfig &config,string &reason)
{
   reason = "";
   if(config.schema_version != DAYE_HUNT_SCHEMA_VERSION)
   {
      reason = "hunt_schema_version_mismatch";
      return false;
   }
   if(!config.enable_high_side && !config.enable_low_side)
   {
      reason = "both_hunt_sides_disabled";
      return false;
   }
   if(!config.equality_counts_as_hunt)
   {
      reason = "equality_must_count_as_hunt_by_doctrine";
      return false;
   }
   if(config.minimum_ready_observations < 1)
   {
      reason = "minimum_ready_observations_must_be_positive";
      return false;
   }
   if(config.maximum_observations_to_publish < config.minimum_ready_observations)
   {
      reason = "maximum_observations_below_minimum_ready";
      return false;
   }
   return true;
}

string DAYE_BuildHuntObservationId(const string opportunity_id,const DAYE_HuntSide side)
{
   return "EXP0018|P05|" + opportunity_id + "|" + DAYE_HuntSideToString(side);
}

bool DAYE_IsPositiveValidPrice(const double value)
{
   return (value > 0.0 && value != EMPTY_VALUE);
}

void DAYE_InitializeSymbolHuntFact(const DAYE_SymbolPeriodSnapshot &current,
                                   const DAYE_SymbolPeriodSnapshot &reference,
                                   const DAYE_HuntSide side,
                                   DAYE_SymbolHuntFact &fact)
{
   ZeroMemory(fact);
   fact.schema_version = DAYE_HUNT_SCHEMA_VERSION;
   fact.status = DAYE_HUNT_STATUS_SOURCE_UNAVAILABLE;
   fact.reason_code = "not_evaluated";
   fact.state = DAYE_SYMBOL_HUNT_UNKNOWN;
   fact.broker_symbol = current.broker_symbol;
   fact.canonical_symbol = current.canonical_symbol;
   fact.side = side;
   fact.reference_snapshot_id = reference.snapshot_id;
   fact.current_snapshot_id = current.snapshot_id;
   fact.reference_completeness = reference.completeness;
   fact.current_completeness = current.completeness;
   fact.event_time_utc = current.last_source_bar_utc;
   fact.availability_time_utc = current.availability_time_utc;
}

bool DAYE_ClassifySymbolHunt(const DAYE_SymbolPeriodSnapshot &current,
                             const DAYE_SymbolPeriodSnapshot &reference,
                             const DAYE_HuntSide side,
                             const DAYE_HuntConfig &config,
                             DAYE_SymbolHuntFact &fact)
{
   DAYE_InitializeSymbolHuntFact(current,reference,side,fact);

   if(reference.completeness != DAYE_PERIOD_COMPLETENESS_COMPLETE)
   {
      fact.status = DAYE_HUNT_STATUS_SOURCE_UNAVAILABLE;
      fact.reason_code = "reference_symbol_period_not_complete";
      fact.state = DAYE_SYMBOL_HUNT_UNAVAILABLE;
      return false;
   }
   if(current.completeness != DAYE_PERIOD_COMPLETENESS_OPEN &&
      current.completeness != DAYE_PERIOD_COMPLETENESS_COMPLETE)
   {
      fact.status = DAYE_HUNT_STATUS_SOURCE_UNAVAILABLE;
      fact.reason_code = "current_symbol_period_not_open_or_complete";
      fact.state = DAYE_SYMBOL_HUNT_UNAVAILABLE;
      return false;
   }

   if(side == DAYE_HUNT_SIDE_HIGH)
   {
      fact.reference_price = reference.high;
      fact.current_extreme = current.high;
      fact.signed_penetration = fact.current_extreme - fact.reference_price;
   }
   else if(side == DAYE_HUNT_SIDE_LOW)
   {
      fact.reference_price = reference.low;
      fact.current_extreme = current.low;
      fact.signed_penetration = fact.reference_price - fact.current_extreme;
   }
   else
   {
      fact.status = DAYE_HUNT_STATUS_INVALID_CONFIG;
      fact.reason_code = "unknown_hunt_side";
      fact.state = DAYE_SYMBOL_HUNT_UNAVAILABLE;
      return false;
   }

   if(config.require_positive_prices && !DAYE_IsPositiveValidPrice(fact.reference_price))
   {
      fact.status = DAYE_HUNT_STATUS_INVALID_REFERENCE_PRICE;
      fact.reason_code = "reference_price_not_positive";
      fact.state = DAYE_SYMBOL_HUNT_UNAVAILABLE;
      return false;
   }
   if(config.require_positive_prices && !DAYE_IsPositiveValidPrice(fact.current_extreme))
   {
      fact.status = DAYE_HUNT_STATUS_INVALID_CURRENT_EXTREME;
      fact.reason_code = "current_extreme_not_positive";
      fact.state = DAYE_SYMBOL_HUNT_UNAVAILABLE;
      return false;
   }

   fact.is_available = true;
   fact.touched_by_equality = (fact.current_extreme == fact.reference_price);
   fact.touched_beyond = false;
   if(side == DAYE_HUNT_SIDE_HIGH)
      fact.touched_beyond = (fact.current_extreme > fact.reference_price);
   else
      fact.touched_beyond = (fact.current_extreme < fact.reference_price);

   fact.is_hunted = (fact.signed_penetration >= 0.0);
   fact.state = fact.is_hunted ? DAYE_SYMBOL_HUNT_HUNTED : DAYE_SYMBOL_HUNT_NOT_HUNTED;
   fact.status = DAYE_HUNT_STATUS_READY;
   fact.reason_code = fact.is_hunted ? (fact.touched_by_equality ? "touch_by_exact_equality" : "touch_beyond_reference") : "reference_not_touched_as_of_snapshot";
   return true;
}

void DAYE_InitializeHuntObservation(const DAYE_RelationshipResolution &resolution,
                                    const DAYE_HuntSide side,
                                    const datetime processing_time_utc,
                                    DAYE_HuntObservation &observation)
{
   ZeroMemory(observation);
   observation.schema_version = DAYE_HUNT_SCHEMA_VERSION;
   observation.status = DAYE_HUNT_STATUS_RELATIONSHIP_NOT_READY;
   observation.reason_code = "not_evaluated";
   observation.is_replay_safe = resolution.is_replay_safe;
   observation.opportunity_id = resolution.opportunity_id;
   observation.relationship_id = resolution.relationship_id;
   observation.source_alias = resolution.source_alias;
   observation.relationship_family = resolution.family;
   observation.is_major = resolution.is_major;
   observation.chart_label = resolution.chart_label;
   observation.side = side;
   observation.pair_state = DAYE_HUNT_PAIR_UNKNOWN;
   observation.current_period_instance_id = resolution.current_period_instance_id;
   observation.current_period_code = resolution.current_period_code;
   observation.current_trading_day_key = resolution.current_trading_day_key;
   observation.reference_period_instance_id = resolution.reference_period_instance_id;
   observation.reference_period_code = resolution.reference_period_code;
   observation.reference_trading_day_key = resolution.reference_trading_day_key;
   observation.event_time_utc = resolution.event_time_utc;
   observation.availability_time_utc = resolution.availability_time_utc;
   observation.processing_time_utc = processing_time_utc;
   observation.current_period_is_open = (resolution.current_period.completeness == DAYE_PERIOD_COMPLETENESS_OPEN);
   observation.observation_id = DAYE_BuildHuntObservationId(resolution.opportunity_id,side);
}

void DAYE_DerivePairState(DAYE_HuntObservation &observation)
{
   if(!observation.symbol_a.is_available || !observation.symbol_b.is_available)
   {
      observation.pair_state = DAYE_HUNT_PAIR_UNAVAILABLE;
      observation.status = DAYE_HUNT_STATUS_SOURCE_UNAVAILABLE;
      observation.reason_code = "one_or_both_symbol_hunt_facts_unavailable";
      observation.is_publishable = false;
      return;
   }

   bool a = observation.symbol_a.is_hunted;
   bool b = observation.symbol_b.is_hunted;
   if(a && b)
      observation.pair_state = DAYE_HUNT_PAIR_BOTH;
   else if(a)
      observation.pair_state = DAYE_HUNT_PAIR_A_ONLY;
   else if(b)
      observation.pair_state = DAYE_HUNT_PAIR_B_ONLY;
   else
      observation.pair_state = DAYE_HUNT_PAIR_NONE;

   observation.is_no_hunt = (observation.pair_state == DAYE_HUNT_PAIR_NONE);
   observation.is_one_sided = (observation.pair_state == DAYE_HUNT_PAIR_A_ONLY || observation.pair_state == DAYE_HUNT_PAIR_B_ONLY);
   observation.is_double_hunt = (observation.pair_state == DAYE_HUNT_PAIR_BOTH);

   if(observation.pair_state == DAYE_HUNT_PAIR_A_ONLY)
   {
      observation.hunter_broker_symbol = observation.symbol_a.broker_symbol;
      observation.hunter_canonical_symbol = observation.symbol_a.canonical_symbol;
      observation.protected_broker_symbol = observation.symbol_b.broker_symbol;
      observation.protected_canonical_symbol = observation.symbol_b.canonical_symbol;
   }
   else if(observation.pair_state == DAYE_HUNT_PAIR_B_ONLY)
   {
      observation.hunter_broker_symbol = observation.symbol_b.broker_symbol;
      observation.hunter_canonical_symbol = observation.symbol_b.canonical_symbol;
      observation.protected_broker_symbol = observation.symbol_a.broker_symbol;
      observation.protected_canonical_symbol = observation.symbol_a.canonical_symbol;
   }

   observation.status = DAYE_HUNT_STATUS_READY;
   observation.reason_code = "touch_only_hunt_state_classified";
   observation.is_publishable = true;
}

bool DAYE_BuildHuntObservation(const DAYE_RelationshipResolution &resolution,
                               const DAYE_HuntSide side,
                               const DAYE_HuntConfig &config,
                               const datetime processing_time_utc,
                               DAYE_HuntObservation &observation)
{
   DAYE_InitializeHuntObservation(resolution,side,processing_time_utc,observation);

   if(resolution.status != DAYE_REL_RESOLUTION_READY || !resolution.is_publishable)
   {
      observation.status = DAYE_HUNT_STATUS_RELATIONSHIP_NOT_READY;
      observation.reason_code = "relationship_resolution_status_" + DAYE_RelationshipResolutionStatusToString(resolution.status);
      observation.pair_state = DAYE_HUNT_PAIR_UNAVAILABLE;
      observation.is_publishable = false;
      return false;
   }

   DAYE_ClassifySymbolHunt(resolution.current_period.symbol_a,resolution.reference_period.symbol_a,side,config,observation.symbol_a);
   DAYE_ClassifySymbolHunt(resolution.current_period.symbol_b,resolution.reference_period.symbol_b,side,config,observation.symbol_b);

   if(observation.symbol_a.event_time_utc > observation.event_time_utc)
      observation.event_time_utc = observation.symbol_a.event_time_utc;
   if(observation.symbol_b.event_time_utc > observation.event_time_utc)
      observation.event_time_utc = observation.symbol_b.event_time_utc;
   if(observation.symbol_a.availability_time_utc > observation.availability_time_utc)
      observation.availability_time_utc = observation.symbol_a.availability_time_utc;
   if(observation.symbol_b.availability_time_utc > observation.availability_time_utc)
      observation.availability_time_utc = observation.symbol_b.availability_time_utc;

   DAYE_DerivePairState(observation);
   return observation.status == DAYE_HUNT_STATUS_READY;
}

bool DAYE_HuntObservationIdExists(const DAYE_HuntObservation &items[],const string observation_id)
{
   for(int i=0;i<ArraySize(items);i++)
      if(items[i].observation_id == observation_id)
         return true;
   return false;
}

bool DAYE_AppendHuntObservation(DAYE_HuntObservation &items[],
                                const DAYE_HuntObservation &observation,
                                const int maximum_items)
{
   if(maximum_items > 0 && ArraySize(items) >= maximum_items)
      return false;
   int index = ArraySize(items);
   ArrayResize(items,index + 1);
   items[index] = observation;
   return true;
}

void DAYE_ClassifyHuntObservations(const DAYE_RelationshipResolution &resolutions[],
                                   const DAYE_HuntConfig &config,
                                   const datetime processing_time_utc,
                                   DAYE_HuntObservation &observations[],
                                   DAYE_HuntStoreSummary &summary)
{
   ArrayResize(observations,0);
   ZeroMemory(summary);
   summary.schema_version = DAYE_HUNT_SCHEMA_VERSION;
   summary.status = DAYE_HUNT_STATUS_SOURCE_UNAVAILABLE;
   summary.reason_code = "not_evaluated";
   summary.is_complete = true;
   summary.is_replay_safe = true;
   summary.processing_time_utc = processing_time_utc;
   summary.source_resolution_count = ArraySize(resolutions);

   if(ArraySize(resolutions) < 1)
   {
      summary.reason_code = "relationship_resolution_store_empty";
      return;
   }

   for(int i=0;i<ArraySize(resolutions);i++)
   {
      DAYE_HuntSide sides[2];
      int side_count = 0;
      if(config.enable_high_side) sides[side_count++] = DAYE_HUNT_SIDE_HIGH;
      if(config.enable_low_side) sides[side_count++] = DAYE_HUNT_SIDE_LOW;

      for(int s=0;s<side_count;s++)
      {
         DAYE_HuntObservation observation;
         bool ready = DAYE_BuildHuntObservation(resolutions[i],sides[s],config,processing_time_utc,observation);
         if(!ready && !config.publish_unavailable_observations)
            continue;

         if(observation.observation_id != "" && DAYE_HuntObservationIdExists(observations,observation.observation_id))
         {
            summary.status = DAYE_HUNT_STATUS_DUPLICATE_OBSERVATION_ID;
            summary.reason_code = "duplicate_hunt_observation_identity";
            summary.is_complete = false;
            return;
         }
         if(!DAYE_AppendHuntObservation(observations,observation,config.maximum_observations_to_publish))
            break;

         summary.observation_count++;
         if(observation.side == DAYE_HUNT_SIDE_HIGH) summary.high_side_count++;
         if(observation.side == DAYE_HUNT_SIDE_LOW) summary.low_side_count++;
         if(!observation.is_replay_safe) summary.is_replay_safe = false;

         if(observation.status == DAYE_HUNT_STATUS_READY)
         {
            summary.ready_observation_count++;
            if(observation.pair_state == DAYE_HUNT_PAIR_NONE) summary.no_hunt_count++;
            else if(observation.pair_state == DAYE_HUNT_PAIR_A_ONLY) summary.a_only_count++;
            else if(observation.pair_state == DAYE_HUNT_PAIR_B_ONLY) summary.b_only_count++;
            else if(observation.pair_state == DAYE_HUNT_PAIR_BOTH) summary.double_hunt_count++;
            if(observation.is_one_sided) summary.one_sided_count++;
            if(observation.current_period_is_open) summary.open_current_count++;
            else summary.complete_current_count++;
            if(observation.symbol_a.touched_by_equality) summary.equality_hunt_count++;
            if(observation.symbol_b.touched_by_equality) summary.equality_hunt_count++;

            summary.latest_observation_id = observation.observation_id;
            if(observation.is_one_sided)
               summary.latest_one_sided_observation_id = observation.observation_id;
            summary.latest_relationship_id = observation.relationship_id;
            summary.latest_current_period_instance_id = observation.current_period_instance_id;
            summary.event_time_utc = observation.event_time_utc;
            if(observation.availability_time_utc > summary.availability_time_utc)
               summary.availability_time_utc = observation.availability_time_utc;
         }
         else
         {
            summary.unavailable_observation_count++;
            summary.is_complete = false;
         }
      }
   }

   summary.run_key = "EXP0018|P05|HUNT_V2|" + IntegerToString(summary.source_resolution_count) + "|" + summary.latest_observation_id;

   if(summary.ready_observation_count < config.minimum_ready_observations)
   {
      summary.status = DAYE_HUNT_STATUS_INSUFFICIENT_READY_OBSERVATIONS;
      summary.reason_code = "ready_hunt_observations_below_minimum";
      summary.is_ready = false;
      return;
   }

   summary.status = DAYE_HUNT_STATUS_READY;
   summary.reason_code = summary.is_complete ? "hunt_observation_store_ready" : "hunt_observation_store_ready_with_explicit_unavailable_records";
   summary.is_ready = true;
}

#endif
