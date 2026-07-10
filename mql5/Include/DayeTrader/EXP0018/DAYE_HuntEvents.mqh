#ifndef __EXP0018_DAYE_HUNT_EVENTS_MQH__
#define __EXP0018_DAYE_HUNT_EVENTS_MQH__

#include <DayeTrader/EXP0018/DAYE_HuntStore.mqh>

string DAYE_BuildHuntEventId(const DAYE_HuntEventType event_type,
                             const datetime event_time_utc,
                             const string observation_id,
                             const DAYE_HuntPairState pair_state)
{
   return "EXP0018|P05|EVENT|" + DAYE_HuntEventTypeToString(event_type) + "|" + IntegerToString((long)event_time_utc) + "|" + observation_id + "|" + DAYE_HuntPairStateToString(pair_state);
}

void DAYE_AppendHuntEvent(DAYE_HuntEvent &events[],
                          const DAYE_HuntEventType event_type,
                          const DAYE_HuntObservation &observation,
                          const DAYE_HuntObservationStatus from_status,
                          const DAYE_HuntObservationStatus to_status,
                          const DAYE_HuntPairState from_pair_state,
                          const DAYE_HuntPairState to_pair_state,
                          const string reason_code)
{
   int index = ArraySize(events);
   ArrayResize(events,index + 1);
   ZeroMemory(events[index]);
   events[index].schema_version = DAYE_HUNT_SCHEMA_VERSION;
   events[index].event_type = event_type;
   events[index].event_time_utc = observation.event_time_utc;
   events[index].availability_time_utc = observation.availability_time_utc;
   events[index].processing_time_utc = observation.processing_time_utc;
   events[index].from_status = from_status;
   events[index].to_status = to_status;
   events[index].from_pair_state = from_pair_state;
   events[index].to_pair_state = to_pair_state;
   events[index].observation_id = observation.observation_id;
   events[index].opportunity_id = observation.opportunity_id;
   events[index].relationship_id = observation.relationship_id;
   events[index].side = observation.side;
   events[index].reason_code = reason_code;
   events[index].event_id = DAYE_BuildHuntEventId(event_type,observation.event_time_utc,observation.observation_id,to_pair_state);
}

void DAYE_AppendHuntSummaryEvent(DAYE_HuntEvent &events[],
                                 const DAYE_HuntEventType event_type,
                                 const DAYE_HuntStoreSummary &current,
                                 const DAYE_HuntObservationStatus from_status,
                                 const DAYE_HuntObservationStatus to_status,
                                 const string reason_code)
{
   DAYE_HuntObservation synthetic;
   ZeroMemory(synthetic);
   synthetic.schema_version = DAYE_HUNT_SCHEMA_VERSION;
   synthetic.observation_id = current.latest_observation_id;
   synthetic.relationship_id = current.latest_relationship_id;
   synthetic.current_period_instance_id = current.latest_current_period_instance_id;
   synthetic.event_time_utc = current.event_time_utc;
   synthetic.availability_time_utc = current.availability_time_utc;
   synthetic.processing_time_utc = current.processing_time_utc;
   synthetic.pair_state = DAYE_HUNT_PAIR_UNKNOWN;
   DAYE_AppendHuntEvent(events,event_type,synthetic,from_status,to_status,DAYE_HUNT_PAIR_UNKNOWN,DAYE_HUNT_PAIR_UNKNOWN,reason_code);
}

bool DAYE_FindObservationInArray(const DAYE_HuntObservation &items[],const string observation_id,DAYE_HuntObservation &item)
{
   for(int i=0;i<ArraySize(items);i++)
   {
      if(items[i].observation_id == observation_id)
      {
         item = items[i];
         return true;
      }
   }
   return false;
}

void DAYE_DetectHuntEvents(const bool has_previous_summary,
                           const DAYE_HuntStoreSummary &previous_summary,
                           const DAYE_HuntStoreSummary &current_summary,
                           const DAYE_HuntObservation &previous_items[],
                           const DAYE_HuntObservation &current_items[],
                           DAYE_HuntEvent &events[])
{
   ArrayResize(events,0);

   if(!has_previous_summary)
   {
      DAYE_AppendHuntSummaryEvent(events,DAYE_HUNT_EVENT_ENGINE_INITIALIZED,current_summary,DAYE_HUNT_STATUS_UNKNOWN,current_summary.status,"hunt_engine_initialized");
      if(current_summary.is_ready)
         DAYE_AppendHuntSummaryEvent(events,DAYE_HUNT_EVENT_STORE_READY,current_summary,DAYE_HUNT_STATUS_UNKNOWN,current_summary.status,current_summary.reason_code);
   }
   else
   {
      if(previous_summary.status != current_summary.status)
         DAYE_AppendHuntSummaryEvent(events,DAYE_HUNT_EVENT_STATUS_CHANGED,current_summary,previous_summary.status,current_summary.status,current_summary.reason_code);
      if(!previous_summary.is_ready && current_summary.is_ready)
         DAYE_AppendHuntSummaryEvent(events,DAYE_HUNT_EVENT_STORE_READY,current_summary,previous_summary.status,current_summary.status,current_summary.reason_code);
      else if(previous_summary.is_ready && !current_summary.is_ready)
         DAYE_AppendHuntSummaryEvent(events,DAYE_HUNT_EVENT_SOURCE_UNAVAILABLE,current_summary,previous_summary.status,current_summary.status,current_summary.reason_code);
      else if(previous_summary.is_complete && !current_summary.is_complete && current_summary.is_ready)
         DAYE_AppendHuntSummaryEvent(events,DAYE_HUNT_EVENT_STORE_DEGRADED,current_summary,previous_summary.status,current_summary.status,current_summary.reason_code);
      if(current_summary.latest_observation_id != "" && current_summary.latest_observation_id != previous_summary.latest_observation_id)
         DAYE_AppendHuntSummaryEvent(events,DAYE_HUNT_EVENT_LATEST_OBSERVATION_ADVANCED,current_summary,previous_summary.status,current_summary.status,"latest_hunt_observation_changed");
   }

   for(int i=0;i<ArraySize(current_items);i++)
   {
      DAYE_HuntObservation prior;
      if(!DAYE_FindObservationInArray(previous_items,current_items[i].observation_id,prior))
         continue;
      if(prior.status == current_items[i].status && prior.pair_state == current_items[i].pair_state)
         continue;

      DAYE_AppendHuntEvent(events,DAYE_HUNT_EVENT_OBSERVATION_STATE_CHANGED,current_items[i],prior.status,current_items[i].status,prior.pair_state,current_items[i].pair_state,"hunt_observation_state_changed");
      if(!prior.is_one_sided && current_items[i].is_one_sided)
         DAYE_AppendHuntEvent(events,DAYE_HUNT_EVENT_ONE_SIDED_HUNT_APPEARED,current_items[i],prior.status,current_items[i].status,prior.pair_state,current_items[i].pair_state,"one_sided_touch_state_appeared");
      if(!prior.is_double_hunt && current_items[i].is_double_hunt)
         DAYE_AppendHuntEvent(events,DAYE_HUNT_EVENT_DOUBLE_HUNT_APPEARED,current_items[i],prior.status,current_items[i].status,prior.pair_state,current_items[i].pair_state,"double_touch_state_appeared");
   }
}

#endif
