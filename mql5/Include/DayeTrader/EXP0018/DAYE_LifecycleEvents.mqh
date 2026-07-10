#ifndef __EXP0018_DAYE_LIFECYCLE_EVENTS_MQH__
#define __EXP0018_DAYE_LIFECYCLE_EVENTS_MQH__

#include <DayeTrader/EXP0018/DAYE_LifecycleStateMachine.mqh>

void DAYE_AppendLifecycleEvent(DAYE_LifecycleEvent &events[],
                               const DAYE_LifecycleEventType event_type,
                               const string reference_id,
                               const string use_id,
                               const string result_id,
                               const string observation_id,
                               const string relationship_id,
                               const DAYE_HuntSide side,
                               const DAYE_ReferenceLifecycleState from_state,
                               const DAYE_ReferenceLifecycleState to_state,
                               const DAYE_ReferenceUseStatus use_status,
                               const datetime event_time_utc,
                               const datetime availability_time_utc,
                               const datetime processing_time_utc,
                               const string reason_code)
{
   int n=ArraySize(events);
   ArrayResize(events,n+1);
   DAYE_LifecycleEvent e;
   ZeroMemory(e);
   e.schema_version=DAYE_LIFECYCLE_SCHEMA_VERSION;
   e.event_type=event_type;
   e.reference_id=reference_id;
   e.use_id=use_id;
   e.result_id=result_id;
   e.observation_id=observation_id;
   e.relationship_id=relationship_id;
   e.side=side;
   e.from_state=from_state;
   e.to_state=to_state;
   e.use_status=use_status;
   e.event_time_utc=event_time_utc;
   e.availability_time_utc=availability_time_utc;
   e.processing_time_utc=processing_time_utc;
   e.reason_code=reason_code;
   string evidence_id=result_id!="" ? result_id : observation_id;
   e.event_id=DAYE_BuildLifecycleEventId(event_type,reference_id,evidence_id,event_time_utc);
   events[n]=e;
}

#endif
