#ifndef __EXP0018_DAYE_RELATIONSHIP_EVENTS_MQH__
#define __EXP0018_DAYE_RELATIONSHIP_EVENTS_MQH__

#include <DayeTrader/EXP0018/DAYE_RelationshipStore.mqh>

string DAYE_BuildRelationshipEventId(const DAYE_RelationshipEventType event_type,
                                     const datetime event_time_utc,
                                     const string opportunity_id,
                                     const string relationship_id)
{
   return "EXP0018|P04|EVENT|" + DAYE_RelationshipEventTypeToString(event_type) + "|" + IntegerToString((long)event_time_utc) + "|" + opportunity_id + "|" + relationship_id;
}

void DAYE_AppendRelationshipEvent(DAYE_RelationshipEvent &events[],
                                  const DAYE_RelationshipEventType event_type,
                                  const datetime event_time_utc,
                                  const datetime availability_time_utc,
                                  const datetime processing_time_utc,
                                  const DAYE_RelationshipResolutionStatus from_status,
                                  const DAYE_RelationshipResolutionStatus to_status,
                                  const string opportunity_id,
                                  const string relationship_id,
                                  const string reason_code)
{
   int index = ArraySize(events);
   ArrayResize(events,index + 1);
   ZeroMemory(events[index]);
   events[index].schema_version = DAYE_RELATIONSHIP_SCHEMA_VERSION;
   events[index].event_type = event_type;
   events[index].event_time_utc = event_time_utc;
   events[index].availability_time_utc = availability_time_utc;
   events[index].processing_time_utc = processing_time_utc;
   events[index].from_status = from_status;
   events[index].to_status = to_status;
   events[index].opportunity_id = opportunity_id;
   events[index].relationship_id = relationship_id;
   events[index].reason_code = reason_code;
   events[index].event_id = DAYE_BuildRelationshipEventId(event_type,event_time_utc,opportunity_id,relationship_id);
}

void DAYE_DetectRelationshipEvents(const bool has_previous,
                                   const DAYE_RelationshipStoreSummary &previous,
                                   const DAYE_RelationshipStoreSummary &current,
                                   DAYE_RelationshipEvent &events[])
{
   ArrayResize(events,0);
   if(!has_previous)
   {
      DAYE_AppendRelationshipEvent(events,DAYE_REL_EVENT_ENGINE_INITIALIZED,current.event_time_utc,current.availability_time_utc,current.processing_time_utc,DAYE_REL_RESOLUTION_UNKNOWN,current.status,current.latest_ready_opportunity_id,current.latest_relationship_id,"relationship_engine_initialized");
      if(current.is_ready)
         DAYE_AppendRelationshipEvent(events,DAYE_REL_EVENT_STORE_READY,current.event_time_utc,current.availability_time_utc,current.processing_time_utc,DAYE_REL_RESOLUTION_UNKNOWN,current.status,current.latest_ready_opportunity_id,current.latest_relationship_id,current.reason_code);
      return;
   }

   if(previous.status != current.status)
      DAYE_AppendRelationshipEvent(events,DAYE_REL_EVENT_STATUS_CHANGED,current.event_time_utc,current.availability_time_utc,current.processing_time_utc,previous.status,current.status,current.latest_ready_opportunity_id,current.latest_relationship_id,current.reason_code);

   if(!previous.is_ready && current.is_ready)
      DAYE_AppendRelationshipEvent(events,DAYE_REL_EVENT_STORE_READY,current.event_time_utc,current.availability_time_utc,current.processing_time_utc,previous.status,current.status,current.latest_ready_opportunity_id,current.latest_relationship_id,current.reason_code);
   else if(previous.is_ready && !current.is_ready)
      DAYE_AppendRelationshipEvent(events,DAYE_REL_EVENT_SOURCE_UNAVAILABLE,current.event_time_utc,current.availability_time_utc,current.processing_time_utc,previous.status,current.status,current.latest_ready_opportunity_id,current.latest_relationship_id,current.reason_code);
   else if(current.is_ready && !current.is_complete && previous.is_complete)
      DAYE_AppendRelationshipEvent(events,DAYE_REL_EVENT_STORE_DEGRADED,current.event_time_utc,current.availability_time_utc,current.processing_time_utc,previous.status,current.status,current.latest_ready_opportunity_id,current.latest_relationship_id,current.reason_code);

   if(current.latest_ready_opportunity_id != "" && current.latest_ready_opportunity_id != previous.latest_ready_opportunity_id)
      DAYE_AppendRelationshipEvent(events,DAYE_REL_EVENT_LATEST_READY_OPPORTUNITY_ADVANCED,current.event_time_utc,current.availability_time_utc,current.processing_time_utc,previous.status,current.status,current.latest_ready_opportunity_id,current.latest_relationship_id,"latest_ready_opportunity_changed");
}

#endif
