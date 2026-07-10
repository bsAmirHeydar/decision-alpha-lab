
#ifndef __EXP0018_DAYE_DATA_EVENTS_MQH__
#define __EXP0018_DAYE_DATA_EVENTS_MQH__

#include <DayeTrader/EXP0018/DAYE_DataSynchronizer.mqh>

string DAYE_BuildDataEventId(const DAYE_DataEventType type,const datetime event_time_utc,const datetime latest_common_event_time_utc)
{
   return "EXP0018|P02|" + DAYE_DataEventTypeToString(type) + "|" +
          IntegerToString((long)event_time_utc) + "|" +
          IntegerToString((long)latest_common_event_time_utc);
}

void DAYE_AppendDataEvent(DAYE_DataSyncEvent &events[],
                          const DAYE_DataEventType type,
                          const datetime event_time_utc,
                          const datetime availability_time_utc,
                          const datetime processing_time_utc,
                          const DAYE_DataStatusCode from_status,
                          const DAYE_DataStatusCode to_status,
                          const datetime latest_common_event_time_utc,
                          const string reason_code)
{
   int index = ArraySize(events);
   ArrayResize(events,index + 1);
   DAYE_DataSyncEvent event;
   ZeroMemory(event);
   event.schema_version = DAYE_DATA_SCHEMA_VERSION;
   event.event_type = type;
   event.event_time_utc = event_time_utc;
   event.availability_time_utc = availability_time_utc;
   event.processing_time_utc = processing_time_utc;
   event.from_status = from_status;
   event.to_status = to_status;
   event.latest_common_event_time_utc = latest_common_event_time_utc;
   event.reason_code = reason_code;
   event.event_id = DAYE_BuildDataEventId(type,event_time_utc,latest_common_event_time_utc);
   events[index] = event;
}

void DAYE_DetectDataSyncEvents(const bool has_previous,
                               const DAYE_DataSyncSummary &previous,
                               const DAYE_DataSyncSummary &current,
                               DAYE_DataSyncEvent &events[])
{
   ArrayResize(events,0);
   if(!has_previous)
   {
      DAYE_AppendDataEvent(events,
                           DAYE_DATA_EVENT_ENGINE_INITIALIZED,
                           current.processing_time_utc,
                           current.availability_time_utc,
                           current.processing_time_utc,
                           current.status,
                           current.status,
                           current.last_common_event_time_utc,
                           "initial_data_sync_observation");
   }

   if(has_previous && previous.status != current.status)
   {
      DAYE_AppendDataEvent(events,
                           DAYE_DATA_EVENT_STATUS_CHANGED,
                           current.processing_time_utc,
                           current.availability_time_utc,
                           current.processing_time_utc,
                           previous.status,
                           current.status,
                           current.last_common_event_time_utc,
                           current.reason_code);
   }

   if(current.is_ready && (!has_previous || !previous.is_ready))
   {
      DAYE_AppendDataEvent(events,
                           current.is_complete ? DAYE_DATA_EVENT_ALIGNMENT_READY : DAYE_DATA_EVENT_ALIGNMENT_DEGRADED,
                           current.last_common_event_time_utc,
                           current.availability_time_utc,
                           current.processing_time_utc,
                           has_previous ? previous.status : current.status,
                           current.status,
                           current.last_common_event_time_utc,
                           current.reason_code);
   }
   else if(!current.is_ready && (!has_previous || previous.is_ready))
   {
      DAYE_AppendDataEvent(events,
                           DAYE_DATA_EVENT_DATA_UNAVAILABLE,
                           current.processing_time_utc,
                           current.availability_time_utc,
                           current.processing_time_utc,
                           has_previous ? previous.status : current.status,
                           current.status,
                           current.last_common_event_time_utc,
                           current.reason_code);
   }

   if(current.is_ready && current.last_common_event_time_utc > 0 &&
      (!has_previous || current.last_common_event_time_utc > previous.last_common_event_time_utc))
   {
      DAYE_AppendDataEvent(events,
                           DAYE_DATA_EVENT_LATEST_COMMON_BAR_ADVANCED,
                           current.last_common_event_time_utc,
                           current.availability_time_utc,
                           current.processing_time_utc,
                           has_previous ? previous.status : current.status,
                           current.status,
                           current.last_common_event_time_utc,
                           "new_exact_timestamp_pair_available");
   }
}

#endif
