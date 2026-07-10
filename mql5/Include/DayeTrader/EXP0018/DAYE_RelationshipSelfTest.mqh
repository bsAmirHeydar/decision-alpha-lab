#ifndef __EXP0018_DAYE_RELATIONSHIP_SELF_TEST_MQH__
#define __EXP0018_DAYE_RELATIONSHIP_SELF_TEST_MQH__

#include <DayeTrader/EXP0018/DAYE_RelationshipAudit.mqh>

void DAYE_TestSetPeriod(DAYE_PairedPeriodSnapshot &item,
                        const DAYE_PeriodId period_id,
                        const string period_code,
                        const string instance_id,
                        const string paired_id,
                        const DAYE_PeriodCompleteness completeness,
                        const string previous_chronological_id,
                        const string previous_same_code_id,
                        const datetime start_utc,
                        const datetime end_utc)
{
   ZeroMemory(item);
   item.schema_version = DAYE_PERIOD_AGG_SCHEMA_VERSION;
   item.status = DAYE_PERIOD_STATUS_OK;
   item.reason_code = "self_test";
   item.completeness = completeness;
   item.is_publishable = true;
   item.is_replay_safe = true;
   item.paired_period_id = paired_id;
   item.period_instance_id = instance_id;
   item.period_id = period_id;
   item.period_code = period_code;
   item.trading_day_key = "2026-01-01";
   item.window.start_utc = start_utc;
   item.window.end_utc = end_utc;
   item.event_time_utc = start_utc;
   item.availability_time_utc = end_utc;
   item.processing_time_utc = end_utc;
   item.previous_chronological_paired_period_id = previous_chronological_id;
   item.previous_same_code_paired_period_id = previous_same_code_id;
}

bool DAYE_RunEmbeddedRelationshipSelfTests(void)
{
   DAYE_RelationshipDefinition registry[];
   DAYE_BuildCanonicalRelationshipRegistry(registry);
   string reason = "";
   if(!DAYE_ValidateCanonicalRelationshipRegistry(registry,reason))
   {
      Print("EXP0018 P04 self-test registry failed reason=",reason);
      return false;
   }

   int major_count = 0;
   int minor_count = 0;
   int blocked_count = 0;
   for(int i=0;i<ArraySize(registry);i++)
   {
      if(registry[i].is_major) major_count++; else minor_count++;
      if(!registry[i].implementation_ready) blocked_count++;
   }
   if(major_count != 6 || minor_count != 16 || blocked_count != 2)
   {
      Print("EXP0018 P04 self-test count failed major=",major_count," minor=",minor_count," blocked=",blocked_count);
      return false;
   }

   DAYE_PairedPeriodSnapshot periods[];
   ArrayResize(periods,5);
   DAYE_TestSetPeriod(periods[0],DAYE_PERIOD_P,"P","P_PREV","PAIR_P_PREV",DAYE_PERIOD_COMPLETENESS_COMPLETE,"","",1000,2000);
   DAYE_TestSetPeriod(periods[1],DAYE_PERIOD_A,"A","A_CURR","PAIR_A_CURR",DAYE_PERIOD_COMPLETENESS_OPEN,"PAIR_P_PREV","",2000,3000);
   DAYE_TestSetPeriod(periods[2],DAYE_PERIOD_D,"D","D_PREV","PAIR_D_PREV",DAYE_PERIOD_COMPLETENESS_COMPLETE,"","",0,1000);
   DAYE_TestSetPeriod(periods[3],DAYE_PERIOD_D,"D","D_CURR","PAIR_D_CURR",DAYE_PERIOD_COMPLETENESS_OPEN,"","PAIR_D_PREV",1000,3000);
   DAYE_TestSetPeriod(periods[4],DAYE_PERIOD_N,"N","N_CURR","PAIR_N_CURR",DAYE_PERIOD_COMPLETENESS_PARTIAL,"","",2000,3000);

   DAYE_RelationshipConfig config;
   ZeroMemory(config);
   config.schema_version = DAYE_RELATIONSHIP_SCHEMA_VERSION;
   config.enable_major_relationships = true;
   config.enable_minor_relationships = true;
   config.allow_open_current_periods = true;
   config.allow_partial_current_periods = false;
   config.require_complete_reference_periods = true;
   config.publish_unavailable_resolutions = true;
   config.publish_blocked_registry_records = true;
   config.minimum_ready_resolutions = 2;
   config.maximum_resolutions_to_publish = 100;

   DAYE_RelationshipResolution resolutions[];
   DAYE_RelationshipStoreSummary summary;
   DAYE_ResolveRelationshipOpportunities(periods,registry,config,4000,resolutions,summary);
   if(!summary.is_ready || summary.ready_resolution_count != 2)
   {
      Print("EXP0018 P04 self-test resolver failed ready=",summary.is_ready," ready_count=",summary.ready_resolution_count," reason=",summary.reason_code);
      return false;
   }

   bool found_pa = false;
   bool found_dd = false;
   for(int i=0;i<ArraySize(resolutions);i++)
   {
      if(resolutions[i].relationship_id == "DAYE_A_CURR_VS_P_PREV" && resolutions[i].status == DAYE_REL_RESOLUTION_READY)
         found_pa = true;
      if(resolutions[i].relationship_id == "DAYE_D_CURR_VS_D_PREV" && resolutions[i].status == DAYE_REL_RESOLUTION_READY)
         found_dd = true;
   }
   if(!found_pa || !found_dd)
   {
      Print("EXP0018 P04 self-test expected PA/DD resolution missing.");
      return false;
   }

   string id_a = DAYE_BuildRelationshipOpportunityId("DAYE_A_CURR_VS_P_PREV","A_CURR","P_PREV");
   string id_b = DAYE_BuildRelationshipOpportunityId("DAYE_A_CURR_VS_P_PREV","A_CURR","P_PREV");
   if(id_a != id_b || id_a == "")
   {
      Print("EXP0018 P04 self-test deterministic opportunity id failed.");
      return false;
   }

   Print("EXP0018 P04 embedded relationship self-tests PASS.");
   return true;
}

#endif
