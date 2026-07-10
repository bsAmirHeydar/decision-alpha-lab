#ifndef __EXP0018_DAYE_SESSION_BOX_EVENTS_MQH__
#define __EXP0018_DAYE_SESSION_BOX_EVENTS_MQH__

#include <DayeTrader/EXP0018/DAYE_SessionBoxStore.mqh>

DAYE_SessionBoxEventType DAYE_SessionBoxEventTypeForStatus(const DAYE_SessionBoxProjectionStatus status)
{
   if(status==DAYE_SESSION_BOX_STATUS_CREATED) return DAYE_SESSION_BOX_EVENT_BOX_CREATED;
   if(status==DAYE_SESSION_BOX_STATUS_UPDATED_OPEN) return DAYE_SESSION_BOX_EVENT_OPEN_BOX_UPDATED;
   if(status==DAYE_SESSION_BOX_STATUS_VERIFIED_CLOSED) return DAYE_SESSION_BOX_EVENT_CLOSED_BOX_VERIFIED;
   if(status==DAYE_SESSION_BOX_STATUS_REPAIRED) return DAYE_SESSION_BOX_EVENT_BOX_REPAIRED;
   if(status==DAYE_SESSION_BOX_STATUS_WAITING_FOR_SYMBOL_CHART) return DAYE_SESSION_BOX_EVENT_WAITING_FOR_CHART;
   if(status==DAYE_SESSION_BOX_STATUS_OBJECT_CREATE_FAILED || status==DAYE_SESSION_BOX_STATUS_OBJECT_UPDATE_FAILED)
      return DAYE_SESSION_BOX_EVENT_OBJECT_API_FAILED;
   if(status==DAYE_SESSION_BOX_STATUS_ORPHAN_DELETED) return DAYE_SESSION_BOX_EVENT_ORPHAN_DELETED;
   return DAYE_SESSION_BOX_EVENT_NONE;
}

void DAYE_AppendSessionBoxEvent(DAYE_SessionBoxEvent &events[],
                                const DAYE_SessionBoxProjection &projection,
                                const DAYE_SessionBoxProjectionStatus from_status,
                                const datetime processing_time_utc)
{
   DAYE_SessionBoxEventType type=DAYE_SessionBoxEventTypeForStatus(projection.status);
   if(type==DAYE_SESSION_BOX_EVENT_NONE) return;
   int n=ArraySize(events); ArrayResize(events,n+1);
   ZeroMemory(events[n]);
   events[n].schema_version=DAYE_SESSION_BOX_SCHEMA_VERSION;
   events[n].event_type=type;
   events[n].projection_id=projection.projection_id;
   events[n].object_name=projection.object_name;
   events[n].period_instance_id=projection.period_instance_id;
   events[n].broker_symbol=projection.broker_symbol;
   events[n].session_code=projection.session_code;
   events[n].target_chart_id=projection.target_chart_id;
   events[n].from_status=from_status;
   events[n].to_status=projection.status;
   events[n].event_time_utc=projection.event_time_utc;
   events[n].availability_time_utc=projection.availability_time_utc;
   events[n].processing_time_utc=processing_time_utc;
   events[n].reason_code=projection.reason_code;
   events[n].event_id=DAYE_BuildSessionBoxEventId(type,projection.projection_id,projection.event_time_utc,projection.reason_code);
}

#endif
