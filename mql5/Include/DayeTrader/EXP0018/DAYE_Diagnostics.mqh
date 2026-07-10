#ifndef __EXP0018_DAYE_DIAGNOSTICS_MQH__
#define __EXP0018_DAYE_DIAGNOSTICS_MQH__

#include <DayeTrader/EXP0018/DAYE_Calendar.mqh>

string DAYE_FormatDateTime(const datetime value)
{
   if(value <= 0)
      return "NA";
   return TimeToString(value,TIME_DATE|TIME_SECONDS);
}

string DAYE_FormatWindow(const DAYE_PeriodWindow &window)
{
   if(window.status != DAYE_STATUS_OK)
      return window.code + "[" + DAYE_StatusCodeToString(window.status) + ":" + window.reason_code + "]";
   return window.code + "[NY " + DAYE_FormatDateTime(window.start_ny) + " -> " + DAYE_FormatDateTime(window.end_ny) +
          " | UTC " + DAYE_FormatDateTime(window.start_utc) + " -> " + DAYE_FormatDateTime(window.end_utc) +
          " | elapsed=" + IntegerToString(window.elapsed_minutes_utc) + "m]";
}

string DAYE_FormatSnapshot(const DAYE_TimeSnapshot &snapshot)
{
   if(!snapshot.is_valid)
      return "EXP0018 P01 status=" + DAYE_StatusCodeToString(snapshot.status) + " reason=" + snapshot.reason_code;

   return "EXP0018 P01"
          + " | Broker=" + DAYE_FormatDateTime(snapshot.broker_time)
          + " | UTC=" + DAYE_FormatDateTime(snapshot.utc_time)
          + " | NY=" + DAYE_FormatDateTime(snapshot.new_york_time)
          + " | NYOffset=" + IntegerToString(snapshot.new_york_utc_offset_minutes)
          + " | DST=" + (snapshot.is_new_york_dst ? "1" : "0")
          + " | Fold=" + IntegerToString(snapshot.new_york_fold)
          + " | Day=" + snapshot.trading_day_key
          + " | Session=" + DAYE_PeriodIdToString(snapshot.session_id)
          + " | Subcycle=" + DAYE_PeriodIdToString(snapshot.subcycle_id)
          + " | Gap=" + (snapshot.in_declared_session_gap ? "1" : "0")
          + " | ReplaySafe=" + (snapshot.is_replay_safe ? "1" : "0");
}

void DAYE_PrintPeriodRegistry(const DAYE_PeriodDefinition &items[])
{
   Print("EXP0018 P01 canonical period registry count=",ArraySize(items));
   for(int i=0;i<ArraySize(items);i++)
   {
      Print("  ",items[i].code,
            " family=",DAYE_PeriodFamilyToString(items[i].family),
            " start_second=",items[i].start_second,
            " end_second=",items[i].end_second,
            " nominal_minutes=",items[i].nominal_duration_minutes,
            " ready=",(items[i].implementation_ready ? "true" : "false"),
            " blocker=",items[i].blocker);
   }
}

void DAYE_PrintTimeEvent(const DAYE_TimeEvent &event)
{
   Print("EXP0018 P01 event id=",event.event_id,
         " type=",DAYE_TimeEventTypeToString(event.event_type),
         " event_utc=",DAYE_FormatDateTime(event.event_time_utc),
         " available_utc=",DAYE_FormatDateTime(event.availability_time_utc),
         " day=",event.trading_day_key,
         " from=",DAYE_PeriodIdToString(event.from_period_id),
         " to=",DAYE_PeriodIdToString(event.to_period_id),
         " reason=",event.reason_code);
}

#endif
