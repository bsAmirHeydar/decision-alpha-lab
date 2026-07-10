#ifndef __EXP0018_DAYE_HUNT_SELF_TEST_MQH__
#define __EXP0018_DAYE_HUNT_SELF_TEST_MQH__

#include <DayeTrader/EXP0018/DAYE_HuntAudit.mqh>

void DAYE_BuildP05TestSymbolPeriod(const string broker_symbol,
                                   const string canonical_symbol,
                                   const double high,
                                   const double low,
                                   DAYE_SymbolPeriodSnapshot &item)
{
   ZeroMemory(item);
   item.schema_version = DAYE_PERIOD_AGG_SCHEMA_VERSION;
   item.status = DAYE_PERIOD_STATUS_OK;
   item.reason_code = "test";
   item.completeness = DAYE_PERIOD_COMPLETENESS_COMPLETE;
   item.is_publishable = true;
   item.is_replay_safe = true;
   item.snapshot_id = "TEST|" + canonical_symbol;
   item.broker_symbol = broker_symbol;
   item.canonical_symbol = canonical_symbol;
   item.high = high;
   item.low = low;
   item.open = (high + low) * 0.5;
   item.close = item.open;
   item.last_source_bar_utc = 1000;
   item.availability_time_utc = 1060;
}

void DAYE_BuildP05TestResolution(const double a_current_high,
                                 const double a_current_low,
                                 const double b_current_high,
                                 const double b_current_low,
                                 const double a_reference_high,
                                 const double a_reference_low,
                                 const double b_reference_high,
                                 const double b_reference_low,
                                 DAYE_RelationshipResolution &resolution)
{
   ZeroMemory(resolution);
   resolution.schema_version = DAYE_RELATIONSHIP_SCHEMA_VERSION;
   resolution.status = DAYE_REL_RESOLUTION_READY;
   resolution.reason_code = "test";
   resolution.is_publishable = true;
   resolution.is_replay_safe = true;
   resolution.opportunity_id = "TEST_OPPORTUNITY";
   resolution.relationship_id = "DAYE_N_CURRENT_VS_L_PREVIOUS";
   resolution.source_alias = "LN";
   resolution.current_period_instance_id = "CURRENT";
   resolution.current_period_code = "N";
   resolution.reference_period_instance_id = "REFERENCE";
   resolution.reference_period_code = "L";
   resolution.event_time_utc = 1000;
   resolution.availability_time_utc = 1060;
   resolution.current_period.completeness = DAYE_PERIOD_COMPLETENESS_COMPLETE;
   resolution.reference_period.completeness = DAYE_PERIOD_COMPLETENESS_COMPLETE;
   DAYE_BuildP05TestSymbolPeriod("SPXUSD","SPX",a_current_high,a_current_low,resolution.current_period.symbol_a);
   DAYE_BuildP05TestSymbolPeriod("NDXUSD","NDX",b_current_high,b_current_low,resolution.current_period.symbol_b);
   DAYE_BuildP05TestSymbolPeriod("SPXUSD","SPX",a_reference_high,a_reference_low,resolution.reference_period.symbol_a);
   DAYE_BuildP05TestSymbolPeriod("NDXUSD","NDX",b_reference_high,b_reference_low,resolution.reference_period.symbol_b);
}

bool DAYE_RunEmbeddedHuntSelfTests(void)
{
   DAYE_HuntConfig config;
   ZeroMemory(config);
   config.schema_version = DAYE_HUNT_SCHEMA_VERSION;
   config.enable_high_side = true;
   config.enable_low_side = true;
   config.equality_counts_as_hunt = true;
   config.publish_unavailable_observations = true;
   config.require_positive_prices = true;
   config.minimum_ready_observations = 1;
   config.maximum_observations_to_publish = 100;

   DAYE_RelationshipResolution resolution;
   DAYE_HuntObservation observation;

   DAYE_BuildP05TestResolution(101.0,95.0,199.0,190.0,100.0,90.0,200.0,180.0,resolution);
   if(!DAYE_BuildHuntObservation(resolution,DAYE_HUNT_SIDE_HIGH,config,1100,observation)) return false;
   if(observation.pair_state != DAYE_HUNT_PAIR_A_ONLY || !observation.is_one_sided || observation.hunter_canonical_symbol != "SPX") return false;

   DAYE_BuildP05TestResolution(100.0,95.0,199.0,190.0,100.0,90.0,200.0,180.0,resolution);
   if(!DAYE_BuildHuntObservation(resolution,DAYE_HUNT_SIDE_HIGH,config,1100,observation)) return false;
   if(observation.pair_state != DAYE_HUNT_PAIR_A_ONLY || !observation.symbol_a.touched_by_equality) return false;

   DAYE_BuildP05TestResolution(99.0,89.0,199.0,190.0,100.0,90.0,200.0,180.0,resolution);
   if(!DAYE_BuildHuntObservation(resolution,DAYE_HUNT_SIDE_LOW,config,1100,observation)) return false;
   if(observation.pair_state != DAYE_HUNT_PAIR_A_ONLY || !observation.symbol_a.is_hunted) return false;

   DAYE_BuildP05TestResolution(101.0,89.0,201.0,179.0,100.0,90.0,200.0,180.0,resolution);
   if(!DAYE_BuildHuntObservation(resolution,DAYE_HUNT_SIDE_HIGH,config,1100,observation)) return false;
   if(observation.pair_state != DAYE_HUNT_PAIR_BOTH || !observation.is_double_hunt) return false;
   if(!DAYE_BuildHuntObservation(resolution,DAYE_HUNT_SIDE_LOW,config,1100,observation)) return false;
   if(observation.pair_state != DAYE_HUNT_PAIR_BOTH || !observation.is_double_hunt) return false;

   string id1 = DAYE_BuildHuntObservationId("ABC",DAYE_HUNT_SIDE_HIGH);
   string id2 = DAYE_BuildHuntObservationId("ABC",DAYE_HUNT_SIDE_HIGH);
   if(id1 != id2 || id1 == "") return false;

   Print("EXP0018 P05 embedded hunt self-tests: PASS");
   return true;
}

#endif
