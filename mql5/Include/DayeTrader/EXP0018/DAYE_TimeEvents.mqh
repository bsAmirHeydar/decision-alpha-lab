#ifndef __EXP0018_DAYE_TIME_EVENTS_MQH__
#define __EXP0018_DAYE_TIME_EVENTS_MQH__

#include <DayeTrader/EXP0018/DAYE_Calendar.mqh>

void DAYE_AppendTimeEvent(DAYE_TimeEvent &events[],const DAYE_TimeEventType event_type,const datetime event_time_utc,const datetime availability_time_utc,const datetime processing_time_utc,const string trading_day_key,const DAYE_PeriodId from_period,const DAYE_PeriodId to_period,const string reason_code)
{
   int index = ArraySize(events);
   ArrayResize(events,index + 1);
   events[index].schema_version = DAYE_TIME_SCHEMA_VERSION;
   events[index].event_type = event_type;
   events[index].event_time_utc = event_time_utc;
   events[index].availability_time_utc = availability_time_utc;
   events[index].processing_time_utc = processing_time_utc;
   events[index].trading_day_key = trading_day_key;
   events[index].from_period_id = from_period;
   events[index].to_period_id = to_period;
   events[index].reason_code = reason_code;
   events[index].event_id = "EXP0018|P01|" + DAYE_TimeEventTypeToString(event_type) + "|" + IntegerToString((long)event_time_utc) + "|" + DAYE_PeriodIdToString(to_period);
}

int DAYE_DetectTimeTransitions(const bool has_previous,const DAYE_TimeSnapshot &previous,const DAYE_TimeSnapshot &current,const datetime processing_time_utc,DAYE_TimeEvent &events[])
{
   ArrayResize(events,0);
   if(!current.is_valid)
      return 0;

   if(!has_previous || !previous.is_valid)
   {
      DAYE_AppendTimeEvent(events,DAYE_TIME_EVENT_KERNEL_INITIALIZED,current.utc_time,current.utc_time,processing_time_utc,current.trading_day_key,DAYE_PERIOD_NONE,current.session_id,"first_valid_snapshot");
      return ArraySize(events);
   }

   if(previous.new_york_utc_offset_minutes != current.new_york_utc_offset_minutes)
      DAYE_AppendTimeEvent(events,DAYE_TIME_EVENT_DST_OFFSET_CHANGED,current.utc_time,current.utc_time,processing_time_utc,current.trading_day_key,DAYE_PERIOD_NONE,DAYE_PERIOD_NONE,"new_york_utc_offset_changed");

   if(previous.trading_day_key != current.trading_day_key)
      DAYE_AppendTimeEvent(events,DAYE_TIME_EVENT_TRADING_DAY_OPENED,current.trading_day_window.start_utc,current.utc_time,processing_time_utc,current.trading_day_key,DAYE_PERIOD_D,DAYE_PERIOD_D,"trading_day_key_changed");

   if(previous.in_declared_session_gap != current.in_declared_session_gap)
   {
      if(current.in_declared_session_gap)
         DAYE_AppendTimeEvent(events,DAYE_TIME_EVENT_GAP_ENTERED,current.session_window.start_utc,current.utc_time,processing_time_utc,current.trading_day_key,previous.session_id,DAYE_PERIOD_GAP,"entered_17_18_gap");
      else
         DAYE_AppendTimeEvent(events,DAYE_TIME_EVENT_GAP_EXITED,current.session_window.start_utc,current.utc_time,processing_time_utc,current.trading_day_key,DAYE_PERIOD_GAP,current.session_id,"left_17_18_gap");
   }

   if(previous.session_id != current.session_id)
      DAYE_AppendTimeEvent(events,DAYE_TIME_EVENT_SESSION_CHANGED,current.session_window.start_utc,current.utc_time,processing_time_utc,current.trading_day_key,previous.session_id,current.session_id,"session_identity_changed");

   if(previous.subcycle_id != current.subcycle_id)
   {
      datetime event_time = current.utc_time;
      if(current.subcycle_window.status == DAYE_STATUS_OK)
         event_time = current.subcycle_window.start_utc;
      DAYE_AppendTimeEvent(events,DAYE_TIME_EVENT_SUBCYCLE_CHANGED,event_time,current.utc_time,processing_time_utc,current.trading_day_key,previous.subcycle_id,current.subcycle_id,"subcycle_identity_changed");
   }

   return ArraySize(events);
}

#endif
