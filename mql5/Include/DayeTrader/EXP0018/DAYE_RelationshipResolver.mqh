#ifndef __EXP0018_DAYE_RELATIONSHIP_RESOLVER_MQH__
#define __EXP0018_DAYE_RELATIONSHIP_RESOLVER_MQH__

#include <DayeTrader/EXP0018/DAYE_RelationshipRegistry.mqh>

string DAYE_BuildRelationshipOpportunityId(const string relationship_id,
                                           const string current_period_instance_id,
                                           const string reference_period_instance_id)
{
   return "EXP0018|P04|" + relationship_id + "|" + current_period_instance_id + "|" + reference_period_instance_id;
}

bool DAYE_FindPairedPeriodById(const DAYE_PairedPeriodSnapshot &items[],
                               const string paired_period_id,
                               DAYE_PairedPeriodSnapshot &item)
{
   if(paired_period_id == "")
      return false;
   for(int i=0;i<ArraySize(items);i++)
   {
      if(items[i].paired_period_id == paired_period_id)
      {
         item = items[i];
         return true;
      }
   }
   ZeroMemory(item);
   return false;
}

bool DAYE_IsCurrentPeriodEligible(const DAYE_PairedPeriodSnapshot &current,
                                  const DAYE_RelationshipConfig &config,
                                  string &reason)
{
   reason = "";
   if(current.completeness == DAYE_PERIOD_COMPLETENESS_COMPLETE)
      return true;
   if(current.completeness == DAYE_PERIOD_COMPLETENESS_OPEN && config.allow_open_current_periods)
      return true;
   if(current.completeness == DAYE_PERIOD_COMPLETENESS_PARTIAL && config.allow_partial_current_periods)
      return true;

   reason = "current_period_completeness_not_allowed_" + DAYE_PeriodCompletenessToString(current.completeness);
   return false;
}

bool DAYE_IsReferencePeriodEligible(const DAYE_PairedPeriodSnapshot &reference,
                                    const DAYE_RelationshipConfig &config,
                                    string &reason)
{
   reason = "";
   if(config.require_complete_reference_periods)
   {
      if(reference.completeness != DAYE_PERIOD_COMPLETENESS_COMPLETE)
      {
         reason = "reference_period_must_be_complete_actual_" + DAYE_PeriodCompletenessToString(reference.completeness);
         return false;
      }
      return true;
   }

   if(reference.completeness == DAYE_PERIOD_COMPLETENESS_COMPLETE ||
      reference.completeness == DAYE_PERIOD_COMPLETENESS_PARTIAL)
      return true;

   reason = "reference_period_not_eligible_" + DAYE_PeriodCompletenessToString(reference.completeness);
   return false;
}

string DAYE_SelectReferencePairedPeriodId(const DAYE_RelationshipDefinition &definition,
                                          const DAYE_PairedPeriodSnapshot &current)
{
   if(definition.selector == DAYE_REL_SELECTOR_PREVIOUS_SAME_CODE)
      return current.previous_same_code_paired_period_id;
   if(definition.selector == DAYE_REL_SELECTOR_PREVIOUS_CHRONOLOGICAL)
      return current.previous_chronological_paired_period_id;
   return "";
}

bool DAYE_OpportunityIdExists(const DAYE_RelationshipResolution &items[],const string opportunity_id)
{
   for(int i=0;i<ArraySize(items);i++)
      if(items[i].opportunity_id == opportunity_id)
         return true;
   return false;
}

void DAYE_InitializeResolution(const DAYE_RelationshipDefinition &definition,
                               const DAYE_PairedPeriodSnapshot &current,
                               const datetime processing_time_utc,
                               DAYE_RelationshipResolution &resolution)
{
   ZeroMemory(resolution);
   resolution.schema_version = DAYE_RELATIONSHIP_SCHEMA_VERSION;
   resolution.status = DAYE_REL_RESOLUTION_UNKNOWN;
   resolution.reason_code = "not_evaluated";
   resolution.is_publishable = false;
   resolution.is_replay_safe = current.is_replay_safe;
   resolution.relationship_id = definition.relationship_id;
   resolution.source_alias = definition.source_alias;
   resolution.family = definition.family;
   resolution.selector = definition.selector;
   resolution.is_major = definition.is_major;
   resolution.chart_label = definition.chart_label;
   resolution.current_paired_period_id = current.paired_period_id;
   resolution.current_period_instance_id = current.period_instance_id;
   resolution.current_period_code = current.period_code;
   resolution.current_trading_day_key = current.trading_day_key;
   resolution.event_time_utc = current.window.start_utc;
   resolution.availability_time_utc = current.availability_time_utc;
   resolution.processing_time_utc = processing_time_utc;
   resolution.current_period = current;
}

void DAYE_AppendResolution(DAYE_RelationshipResolution &items[],const DAYE_RelationshipResolution &resolution,const int maximum_count)
{
   if(maximum_count > 0 && ArraySize(items) >= maximum_count)
      return;
   int index = ArraySize(items);
   ArrayResize(items,index + 1);
   items[index] = resolution;
}

bool DAYE_ValidateRelationshipConfig(const DAYE_RelationshipConfig &config,string &reason)
{
   reason = "";
   if(config.schema_version != DAYE_RELATIONSHIP_SCHEMA_VERSION)
   {
      reason = "relationship_config_schema_version_mismatch";
      return false;
   }
   if(config.minimum_ready_resolutions < 0)
   {
      reason = "minimum_ready_resolutions_must_be_non_negative";
      return false;
   }
   if(config.maximum_resolutions_to_publish < 1)
   {
      reason = "maximum_resolutions_to_publish_must_be_positive";
      return false;
   }
   return true;
}

void DAYE_ResolveRelationshipOpportunities(const DAYE_PairedPeriodSnapshot &periods[],
                                           const DAYE_RelationshipDefinition &registry[],
                                           const DAYE_RelationshipConfig &config,
                                           const datetime processing_time_utc,
                                           DAYE_RelationshipResolution &resolutions[],
                                           DAYE_RelationshipStoreSummary &summary)
{
   ArrayResize(resolutions,0);
   ZeroMemory(summary);
   summary.schema_version = DAYE_RELATIONSHIP_SCHEMA_VERSION;
   summary.status = DAYE_REL_RESOLUTION_SOURCE_UNAVAILABLE;
   summary.reason_code = "not_evaluated";
   summary.is_ready = false;
   summary.is_complete = true;
   summary.is_replay_safe = true;
   summary.processing_time_utc = processing_time_utc;
   summary.source_period_count = ArraySize(periods);

   string registry_reason = "";
   if(!DAYE_ValidateCanonicalRelationshipRegistry(registry,registry_reason))
   {
      summary.status = DAYE_REL_RESOLUTION_INVALID_REGISTRY;
      summary.reason_code = registry_reason;
      summary.is_complete = false;
      return;
   }

   summary.registry_count = ArraySize(registry);
   for(int r=0;r<ArraySize(registry);r++)
   {
      if(registry[r].is_major) summary.major_registry_count++;
      else summary.minor_registry_count++;
      if(registry[r].implementation_ready) summary.ready_registry_count++;
      else summary.blocked_registry_count++;
      if(DAYE_IsRelationshipEnabledByConfig(registry[r],config) && registry[r].implementation_ready)
         summary.enabled_registry_count++;
   }

   if(ArraySize(periods) < 1)
   {
      summary.status = DAYE_REL_RESOLUTION_SOURCE_UNAVAILABLE;
      summary.reason_code = "period_store_is_empty";
      summary.is_complete = false;
      return;
   }

   for(int p=0;p<ArraySize(periods);p++)
   {
      DAYE_PairedPeriodSnapshot current = periods[p];
      for(int r=0;r<ArraySize(registry);r++)
      {
         DAYE_RelationshipDefinition definition = registry[r];
         if(current.period_id != definition.current_period_id)
            continue;

         DAYE_RelationshipResolution resolution;
         DAYE_InitializeResolution(definition,current,processing_time_utc,resolution);

         if(!DAYE_IsRelationshipEnabledByConfig(definition,config))
         {
            resolution.status = DAYE_REL_RESOLUTION_DISABLED_BY_CONFIG;
            resolution.reason_code = "relationship_family_disabled_by_config";
            if(config.publish_unavailable_resolutions)
               DAYE_AppendResolution(resolutions,resolution,config.maximum_resolutions_to_publish);
            continue;
         }

         if(!definition.implementation_ready)
         {
            resolution.status = DAYE_REL_RESOLUTION_BLOCKED_BY_DOCTRINE;
            resolution.reason_code = "blocked_by_" + definition.blocker_decision_id;
            summary.blocked_resolution_count++;
            summary.is_complete = false;
            if(config.publish_blocked_registry_records && config.publish_unavailable_resolutions)
               DAYE_AppendResolution(resolutions,resolution,config.maximum_resolutions_to_publish);
            continue;
         }

         string current_reason = "";
         if(!DAYE_IsCurrentPeriodEligible(current,config,current_reason))
         {
            resolution.status = DAYE_REL_RESOLUTION_CURRENT_NOT_ELIGIBLE;
            resolution.reason_code = current_reason;
            summary.unavailable_resolution_count++;
            summary.is_complete = false;
            if(config.publish_unavailable_resolutions)
               DAYE_AppendResolution(resolutions,resolution,config.maximum_resolutions_to_publish);
            continue;
         }

         string reference_paired_id = DAYE_SelectReferencePairedPeriodId(definition,current);
         if(reference_paired_id == "")
         {
            resolution.status = DAYE_REL_RESOLUTION_REFERENCE_ID_MISSING;
            resolution.reason_code = "reference_link_is_empty";
            summary.unavailable_resolution_count++;
            summary.is_complete = false;
            if(config.publish_unavailable_resolutions)
               DAYE_AppendResolution(resolutions,resolution,config.maximum_resolutions_to_publish);
            continue;
         }

         DAYE_PairedPeriodSnapshot reference;
         if(!DAYE_FindPairedPeriodById(periods,reference_paired_id,reference))
         {
            resolution.status = DAYE_REL_RESOLUTION_REFERENCE_NOT_FOUND;
            resolution.reason_code = "reference_pair_not_found_in_exported_store";
            resolution.reference_paired_period_id = reference_paired_id;
            summary.unavailable_resolution_count++;
            summary.is_complete = false;
            if(config.publish_unavailable_resolutions)
               DAYE_AppendResolution(resolutions,resolution,config.maximum_resolutions_to_publish);
            continue;
         }

         resolution.reference_period = reference;
         resolution.reference_paired_period_id = reference.paired_period_id;
         resolution.reference_period_instance_id = reference.period_instance_id;
         resolution.reference_period_code = reference.period_code;
         resolution.reference_trading_day_key = reference.trading_day_key;
         if(reference.availability_time_utc > resolution.availability_time_utc)
            resolution.availability_time_utc = reference.availability_time_utc;
         if(!reference.is_replay_safe)
            resolution.is_replay_safe = false;

         if(reference.period_id != definition.reference_period_id || reference.period_code != definition.reference_period_code)
         {
            resolution.status = DAYE_REL_RESOLUTION_REFERENCE_CODE_MISMATCH;
            resolution.reason_code = "expected_" + definition.reference_period_code + "_actual_" + reference.period_code;
            summary.unavailable_resolution_count++;
            summary.is_complete = false;
            if(config.publish_unavailable_resolutions)
               DAYE_AppendResolution(resolutions,resolution,config.maximum_resolutions_to_publish);
            continue;
         }

         string reference_reason = "";
         if(!DAYE_IsReferencePeriodEligible(reference,config,reference_reason))
         {
            resolution.status = DAYE_REL_RESOLUTION_REFERENCE_NOT_COMPLETE;
            resolution.reason_code = reference_reason;
            summary.unavailable_resolution_count++;
            summary.is_complete = false;
            if(config.publish_unavailable_resolutions)
               DAYE_AppendResolution(resolutions,resolution,config.maximum_resolutions_to_publish);
            continue;
         }

         resolution.opportunity_id = DAYE_BuildRelationshipOpportunityId(definition.relationship_id,current.period_instance_id,reference.period_instance_id);
         if(DAYE_OpportunityIdExists(resolutions,resolution.opportunity_id))
         {
            resolution.status = DAYE_REL_RESOLUTION_DUPLICATE_OPPORTUNITY_ID;
            resolution.reason_code = "duplicate_opportunity_identity";
            summary.status = DAYE_REL_RESOLUTION_DUPLICATE_OPPORTUNITY_ID;
            summary.reason_code = resolution.reason_code;
            summary.is_complete = false;
            DAYE_AppendResolution(resolutions,resolution,config.maximum_resolutions_to_publish);
            return;
         }

         resolution.status = DAYE_REL_RESOLUTION_READY;
         resolution.reason_code = "relationship_context_resolved";
         resolution.is_publishable = true;
         DAYE_AppendResolution(resolutions,resolution,config.maximum_resolutions_to_publish);
         summary.ready_resolution_count++;
         if(current.completeness == DAYE_PERIOD_COMPLETENESS_OPEN)
            summary.open_current_resolution_count++;
         if(current.completeness == DAYE_PERIOD_COMPLETENESS_COMPLETE)
            summary.complete_current_resolution_count++;
         summary.latest_ready_opportunity_id = resolution.opportunity_id;
         summary.latest_opportunity_id = resolution.opportunity_id;
         summary.latest_relationship_id = resolution.relationship_id;
         summary.latest_current_period_instance_id = resolution.current_period_instance_id;
         summary.event_time_utc = resolution.event_time_utc;
         if(resolution.availability_time_utc > summary.availability_time_utc)
            summary.availability_time_utc = resolution.availability_time_utc;
         if(!resolution.is_replay_safe)
            summary.is_replay_safe = false;
      }
   }

   summary.resolved_count = ArraySize(resolutions);
   summary.run_key = "EXP0018|P04|REGISTRY_V2|" + IntegerToString(summary.source_period_count) + "|" + summary.latest_current_period_instance_id;

   if(summary.status == DAYE_REL_RESOLUTION_DUPLICATE_OPPORTUNITY_ID)
      return;
   if(summary.ready_resolution_count < config.minimum_ready_resolutions)
   {
      summary.status = DAYE_REL_RESOLUTION_SOURCE_UNAVAILABLE;
      summary.reason_code = "ready_relationship_resolutions_below_minimum";
      summary.is_ready = false;
      return;
   }

   summary.status = DAYE_REL_RESOLUTION_READY;
   summary.reason_code = summary.is_complete ? "relationship_store_ready" : "relationship_store_ready_with_explicit_unavailable_records";
   summary.is_ready = true;
}

#endif
