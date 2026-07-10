#ifndef __EXP0018_DAYE_RENDER_EVENTS_MQH__
#define __EXP0018_DAYE_RENDER_EVENTS_MQH__

#include <DayeTrader/EXP0018/DAYE_RenderStore.mqh>

void DAYE_AppendRenderEvent(DAYE_RenderEvent &events[],const DAYE_RenderEventType type,
                            const DAYE_RenderProjection &projection,const DAYE_RenderProjectionStatus from_status,
                            const datetime processing_time_utc,const string reason_code)
{
   int n=ArraySize(events); ArrayResize(events,n+1);
   ZeroMemory(events[n]);
   events[n].schema_version=DAYE_RENDER_SCHEMA_VERSION;
   events[n].event_type=type;
   events[n].projection_id=projection.projection_id;
   events[n].use_id=projection.use_id;
   events[n].object_name=projection.line_object_name;
   events[n].target_chart_id=projection.target_chart_id;
   events[n].from_status=from_status;
   events[n].to_status=projection.status;
   events[n].event_time_utc=projection.event_time_utc;
   events[n].availability_time_utc=projection.availability_time_utc;
   events[n].processing_time_utc=processing_time_utc;
   events[n].reason_code=reason_code;
   events[n].event_id=DAYE_BuildRenderEventId(type,projection.projection_id,processing_time_utc);
}

DAYE_RenderEventType DAYE_RenderEventTypeForStatus(const DAYE_RenderProjectionStatus status,const bool manual_delete_repaired)
{
   if(manual_delete_repaired) return DAYE_RENDER_EVENT_MANUAL_DELETE_REPAIRED;
   if(status==DAYE_RENDER_STATUS_CREATED) return DAYE_RENDER_EVENT_LINE_CREATED;
   if(status==DAYE_RENDER_STATUS_VERIFIED) return DAYE_RENDER_EVENT_LINE_VERIFIED;
   if(status==DAYE_RENDER_STATUS_REPAIRED) return DAYE_RENDER_EVENT_LINE_REPAIRED;
   if(status==DAYE_RENDER_STATUS_WAITING_FOR_HUNTER_CHART) return DAYE_RENDER_EVENT_WAITING_FOR_HUNTER_CHART;
   if(status==DAYE_RENDER_STATUS_SOURCE_PERIOD_NOT_FOUND) return DAYE_RENDER_EVENT_SOURCE_PERIOD_MISSING;
   if(status==DAYE_RENDER_STATUS_SOURCE_EXTREME_UNAVAILABLE) return DAYE_RENDER_EVENT_SOURCE_EXTREME_MISSING;
   if(status==DAYE_RENDER_STATUS_OBJECT_CREATE_FAILED || status==DAYE_RENDER_STATUS_OBJECT_UPDATE_FAILED)
      return DAYE_RENDER_EVENT_OBJECT_API_FAILED;
   return DAYE_RENDER_EVENT_NONE;
}

#endif
