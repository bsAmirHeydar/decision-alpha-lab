#ifndef __EXP0018_DAYE_RELATIONSHIP_DIAGNOSTICS_MQH__
#define __EXP0018_DAYE_RELATIONSHIP_DIAGNOSTICS_MQH__

#include <DayeTrader/EXP0018/DAYE_RelationshipEvents.mqh>

string DAYE_FormatRelationshipDefinition(const DAYE_RelationshipDefinition &item)
{
   return "P04 registry id=" + item.relationship_id +
          " alias=" + item.source_alias +
          " family=" + DAYE_RelationshipFamilyToString(item.family) +
          " current=" + item.current_period_code +
          " reference=" + item.reference_period_code +
          " selector=" + DAYE_RelationshipSelectorToString(item.selector) +
          " doctrine=" + DAYE_RelationshipDoctrineStatusToString(item.doctrine_status) +
          " blocker=" + item.blocker_decision_id;
}

string DAYE_FormatRelationshipResolution(const DAYE_RelationshipResolution &item)
{
   return "P04 resolution status=" + DAYE_RelationshipResolutionStatusToString(item.status) +
          " relationship=" + item.relationship_id +
          " alias=" + item.source_alias +
          " current=" + item.current_period_code + ":" + item.current_period_instance_id +
          " reference=" + item.reference_period_code + ":" + item.reference_period_instance_id +
          " publishable=" + IntegerToString(item.is_publishable ? 1 : 0) +
          " reason=" + item.reason_code;
}

string DAYE_FormatRelationshipSummary(const DAYE_RelationshipStoreSummary &summary)
{
   return "EXP0018 P04 status=" + DAYE_RelationshipResolutionStatusToString(summary.status) +
          " ready=" + IntegerToString(summary.is_ready ? 1 : 0) +
          " complete=" + IntegerToString(summary.is_complete ? 1 : 0) +
          " registry=" + IntegerToString(summary.registry_count) +
          " enabled=" + IntegerToString(summary.enabled_registry_count) +
          " blocked=" + IntegerToString(summary.blocked_registry_count) +
          " source_periods=" + IntegerToString(summary.source_period_count) +
          " resolutions=" + IntegerToString(summary.resolved_count) +
          " ready_resolutions=" + IntegerToString(summary.ready_resolution_count) +
          " unavailable=" + IntegerToString(summary.unavailable_resolution_count) +
          " latest=" + summary.latest_relationship_id +
          " reason=" + summary.reason_code;
}

string DAYE_FormatRelationshipEvent(const DAYE_RelationshipEvent &event)
{
   return "EXP0018 P04 event=" + DAYE_RelationshipEventTypeToString(event.event_type) +
          " id=" + event.event_id +
          " relationship=" + event.relationship_id +
          " opportunity=" + event.opportunity_id +
          " from=" + DAYE_RelationshipResolutionStatusToString(event.from_status) +
          " to=" + DAYE_RelationshipResolutionStatusToString(event.to_status) +
          " reason=" + event.reason_code;
}

#endif
