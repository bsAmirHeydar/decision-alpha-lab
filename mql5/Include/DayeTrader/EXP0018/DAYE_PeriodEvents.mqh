
#ifndef __EXP0018_DAYE_PERIOD_EVENTS_MQH__
#define __EXP0018_DAYE_PERIOD_EVENTS_MQH__

#include <DayeTrader/EXP0018/DAYE_PeriodStore.mqh>

string DAYE_BuildPeriodAggregateEventId(const DAYE_PeriodAggregateEventType type,
                                        const datetime event_time_utc,
                                        const string period_instance_id)
{
   return "EXP0018|P03|EVENT|" + DAYE_PeriodAggregateEventTypeToString(type) + "|" + IntegerToString((long)event_time_utc) + "|" + period_instance_id;
}

void DAYE_AppendPeriodAggregateEvent(DAYE_PeriodAggregateEvent &events[],
                                     const DAYE_PeriodAggregateEventType type,
                                     const datetime event_time_utc,
                                     const datetime availability_time_utc,
                                     const datetime processing_time_utc,
                                     const DAYE_PeriodAggregateStatusCode from_status,
                                     const DAYE_PeriodAggregateStatusCode to_status,
                                     const string period_instance_id,
                                     const string reason_code)
{
   int index = ArraySize(events);
   ArrayResize(events,index + 1);
   ZeroMemory(events[index]);
   events[index].schema_version = DAYE_PERIOD_AGG_SCHEMA_VERSION;
   events[index].event_type = type;
   events[index].event_time_utc = event_time_utc;
   events[index].availability_time_utc = availability_time_utc;
   events[index].processing_time_utc = processing_time_utc;
   events[index].from_status = from_status;
   events[index].to_status = to_status;
   events[index].period_instance_id = period_instance_id;
   events[index].reason_code = reason_code;
   events[index].event_id = DAYE_BuildPeriodAggregateEventId(type,event_time_utc,period_instance_id);
}

void DAYE_DetectPeriodAggregateEvents(const bool has_previous,
                                      const DAYE_PeriodStoreSummary &previous,
                                      const DAYE_PeriodStoreSummary &current,
                                      DAYE_PeriodAggregateEvent &events[])
{
   ArrayResize(events,0);
   if(!has_previous)
   {
      DAYE_AppendPeriodAggregateEvent(events,
                                      DAYE_PERIOD_EVENT_ENGINE_INITIALIZED,
                                      current.source_last_event_time_utc,
                                      current.availability_time_utc,
                                      current.processing_time_utc,
                                      current.status,
                                      current.status,
                                      current.latest_paired_period_id,
                                      "first_period_store_evaluation");
      if(current.is_ready)
         DAYE_AppendPeriodAggregateEvent(events,DAYE_PERIOD_EVENT_STORE_READY,current.source_last_event_time_utc,current.availability_time_utc,current.processing_time_utc,current.status,current.status,current.latest_paired_period_id,current.reason_code);
      else
         DAYE_AppendPeriodAggregateEvent(events,DAYE_PERIOD_EVENT_DATA_UNAVAILABLE,current.source_last_event_time_utc,current.availability_time_utc,current.processing_time_utc,current.status,current.status,current.latest_paired_period_id,current.reason_code);
      return;
   }

   if(previous.status != current.status)
      DAYE_AppendPeriodAggregateEvent(events,DAYE_PERIOD_EVENT_STATUS_CHANGED,current.source_last_event_time_utc,current.availability_time_utc,current.processing_time_utc,previous.status,current.status,current.latest_paired_period_id,current.reason_code);

   if(!previous.is_ready && current.is_ready)
      DAYE_AppendPeriodAggregateEvent(events,DAYE_PERIOD_EVENT_STORE_READY,current.source_last_event_time_utc,current.availability_time_utc,current.processing_time_utc,previous.status,current.status,current.latest_paired_period_id,current.reason_code);
   else if(previous.is_ready && !current.is_ready)
      DAYE_AppendPeriodAggregateEvent(events,DAYE_PERIOD_EVENT_DATA_UNAVAILABLE,current.source_last_event_time_utc,current.availability_time_utc,current.processing_time_utc,previous.status,current.status,current.latest_paired_period_id,current.reason_code);
   else if(previous.status == DAYE_PERIOD_STATUS_OK && current.status == DAYE_PERIOD_STATUS_PARTIAL_SOURCE_ALIGNMENT)
      DAYE_AppendPeriodAggregateEvent(events,DAYE_PERIOD_EVENT_STORE_DEGRADED,current.source_last_event_time_utc,current.availability_time_utc,current.processing_time_utc,previous.status,current.status,current.latest_paired_period_id,current.reason_code);

   if(current.latest_complete_paired_period_id != "" && current.latest_complete_paired_period_id != previous.latest_complete_paired_period_id)
      DAYE_AppendPeriodAggregateEvent(events,
                                      DAYE_PERIOD_EVENT_LATEST_COMPLETE_PERIOD_ADVANCED,
                                      current.latest_complete_period_end_utc,
                                      current.availability_time_utc,
                                      current.processing_time_utc,
                                      previous.status,
                                      current.status,
                                      current.latest_complete_paired_period_id,
                                      "new_latest_complete_period");
}

#endif
