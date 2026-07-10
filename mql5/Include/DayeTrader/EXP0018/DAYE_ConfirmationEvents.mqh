#ifndef __EXP0018_DAYE_CONFIRMATION_EVENTS_MQH__
#define __EXP0018_DAYE_CONFIRMATION_EVENTS_MQH__

#include <DayeTrader/EXP0018/DAYE_ConfirmationCheckpoint.mqh>

string DAYE_BuildConfirmationEventId(const DAYE_ConfirmationEventType event_type,
                                     const datetime event_time_utc,
                                     const string candidate_id,
                                     const string result_id)
{
   return "EXP0018|P06|EVENT|" + DAYE_ConfirmationEventTypeToString(event_type) + "|" +
          IntegerToString((long)event_time_utc) + "|" + candidate_id + "|" + result_id;
}

void DAYE_AppendConfirmationEvent(DAYE_ConfirmationEvent &events[],
                                  const DAYE_ConfirmationEventType event_type,
                                  const string candidate_id,
                                  const string result_id,
                                  const string observation_id,
                                  const string relationship_id,
                                  const DAYE_HuntSide side,
                                  const DAYE_HuntPairState from_pair,
                                  const DAYE_HuntPairState to_pair,
                                  const DAYE_ConfirmationOutcome outcome,
                                  const datetime event_time_utc,
                                  const datetime availability_time_utc,
                                  const datetime processing_time_utc,
                                  const string reason_code)
{
   int index=ArraySize(events);
   ArrayResize(events,index+1);
   ZeroMemory(events[index]);
   events[index].schema_version=DAYE_CONFIRMATION_SCHEMA_VERSION;
   events[index].event_type=event_type;
   events[index].candidate_id=candidate_id;
   events[index].result_id=result_id;
   events[index].observation_id=observation_id;
   events[index].relationship_id=relationship_id;
   events[index].side=side;
   events[index].from_pair_state=from_pair;
   events[index].to_pair_state=to_pair;
   events[index].outcome=outcome;
   events[index].event_time_utc=event_time_utc;
   events[index].availability_time_utc=availability_time_utc;
   events[index].processing_time_utc=processing_time_utc;
   events[index].reason_code=reason_code;
   events[index].event_id=DAYE_BuildConfirmationEventId(event_type,event_time_utc,candidate_id,result_id);
}

DAYE_ConfirmationEventType DAYE_EventTypeForOutcome(const DAYE_ConfirmationOutcome outcome)
{
   switch(outcome)
   {
      case DAYE_CONFIRM_OUTCOME_CONFIRMED: return DAYE_CONFIRM_EVENT_CONFIRMED;
      case DAYE_CONFIRM_OUTCOME_INVALIDATED_DOUBLE_HUNT: return DAYE_CONFIRM_EVENT_INVALIDATED_DOUBLE_HUNT;
      case DAYE_CONFIRM_OUTCOME_NO_SIGNAL_AT_CLOSE: return DAYE_CONFIRM_EVENT_NO_SIGNAL_AT_CLOSE;
      case DAYE_CONFIRM_OUTCOME_INVALIDATED_ROLE_CHANGED: return DAYE_CONFIRM_EVENT_ROLE_CHANGED;
      case DAYE_CONFIRM_OUTCOME_MISSED_CLOSE_REPLAY_REQUIRED: return DAYE_CONFIRM_EVENT_HOST_CLOSE_MISSED;
      default: return DAYE_CONFIRM_EVENT_UNAVAILABLE_AT_CLOSE;
   }
}

#endif
