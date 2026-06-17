#ifndef __DAL_VALIDATION_JOURNAL_MQH__
#define __DAL_VALIDATION_JOURNAL_MQH__

#include <DecisionAlphaLab/M0001/DAL_M0001Types.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001AuditState.mqh>
#include <DecisionAlphaLab/StructuralNodes/LRule/DAL_LRuleTypes.mqh>

int DAL_OpenJournalWrite(const string file_name)
{
   return FileOpen(file_name, FILE_WRITE | FILE_CSV | FILE_ANSI, ',');
}

void DAL_WriteM0001NodeJournal(
   const string file_name,
   const DALLRuleNode &nodes[],
   const int nodes_count
)
{
   int h = DAL_OpenJournalWrite(file_name);
   if(h == INVALID_HANDLE)
      return;

   FileWrite(h, "id", "type", "node_time", "active_from_time", "index", "active_index", "price");
   for(int i = 0; i < nodes_count; i++)
   {
      FileWrite(
         h,
         nodes[i].id,
         DAL_NodeTypeToString(nodes[i].type),
         TimeToString(nodes[i].time, TIME_DATE | TIME_MINUTES),
         TimeToString(nodes[i].active_from_time, TIME_DATE | TIME_MINUTES),
         nodes[i].index,
         nodes[i].active_from_index,
         DoubleToString(nodes[i].price, _Digits)
      );
   }

   FileClose(h);
}


void DAL_WriteM0001NodeAuditStateJournal(
   const string file_name,
   const DALM0001NodeAuditState &states[],
   const int states_count
)
{
   int h = DAL_OpenJournalWrite(file_name);
   if(h == INVALID_HANDLE)
      return;

   FileWrite(
      h,
      "id",
      "node_id",
      "type",
      "node_time",
      "active_from_time",
      "tracking_cycle_start_time",
      "current_time",
      "node_price",
      "expansion_extreme",
      "territory_lower",
      "territory_upper",
      "touch_started",
      "first_touch_time",
      "touch_confirmed",
      "touch_confirmed_time",
      "hunted",
      "hunt_time",
      "consumed",
      "consumed_time",
      "consume_reason",
      "invalidated",
      "revisited_live",
      "fresh_live",
      "confirmed_touch_count",
      "next_revisit_id",
      "bars_since_last_touch_confirmed"
   );

   for(int i = 0; i < states_count; i++)
   {
      FileWrite(
         h,
         states[i].id,
         states[i].node_id,
         DAL_NodeTypeToString(states[i].node_type),
         TimeToString(states[i].node_time, TIME_DATE | TIME_MINUTES),
         TimeToString(states[i].active_from_time, TIME_DATE | TIME_MINUTES),
         TimeToString(states[i].tracking_cycle_start_time, TIME_DATE | TIME_MINUTES),
         TimeToString(states[i].current_time, TIME_DATE | TIME_MINUTES),
         DoubleToString(states[i].node_price, _Digits),
         DoubleToString(states[i].expansion_extreme, _Digits),
         DoubleToString(states[i].territory_lower, _Digits),
         DoubleToString(states[i].territory_upper, _Digits),
         DAL_BoolToString(states[i].touch_started),
         states[i].first_touch_time > 0 ? TimeToString(states[i].first_touch_time, TIME_DATE | TIME_MINUTES) : "",
         DAL_BoolToString(states[i].touch_confirmed),
         states[i].touch_confirmed_time > 0 ? TimeToString(states[i].touch_confirmed_time, TIME_DATE | TIME_MINUTES) : "",
         DAL_BoolToString(states[i].hunted),
         states[i].hunt_time > 0 ? TimeToString(states[i].hunt_time, TIME_DATE | TIME_MINUTES) : "",
         DAL_BoolToString(states[i].consumed),
         states[i].consumed_time > 0 ? TimeToString(states[i].consumed_time, TIME_DATE | TIME_MINUTES) : "",
         DAL_M0001ConsumeReasonToString(states[i].consume_reason),
         DAL_BoolToString(states[i].invalidated),
         DAL_BoolToString(states[i].revisited_live),
         DAL_BoolToString(states[i].fresh_live),
         states[i].confirmed_touch_count,
         states[i].next_revisit_id,
         states[i].bars_since_last_touch_confirmed
      );
   }

   FileClose(h);
}

void DAL_WriteM0001EventJournal(
   const string file_name,
   const DALM0001Event &events[],
   const int events_count
)
{
   int h = DAL_OpenJournalWrite(file_name);
   if(h == INVALID_HANDLE)
      return;

   FileWrite(h, "id", "node_id", "revisit_id", "type", "entry_time", "exit_time", "event_length", "rtv_sample_length", "rtv_inside_end_index", "rtv_before_start_index", "touch_confirmed_time", "consumed_time", "consume_reason", "rtv", "rtv_ready", "touch_confirmed", "hunted", "mean_before", "mean_inside");
   for(int i = 0; i < events_count; i++)
   {
      FileWrite(
         h,
         events[i].id,
         events[i].node_id,
         events[i].revisit_id,
         DAL_NodeTypeToString(events[i].node_type),
         TimeToString(events[i].entry_time, TIME_DATE | TIME_MINUTES),
         TimeToString(events[i].exit_time, TIME_DATE | TIME_MINUTES),
         events[i].event_length,
         events[i].rtv_sample_length,
         events[i].rtv_inside_end_index,
         events[i].rtv_before_start_index,
         events[i].touch_confirmed_time > 0 ? TimeToString(events[i].touch_confirmed_time, TIME_DATE | TIME_MINUTES) : "",
         events[i].consumed_time > 0 ? TimeToString(events[i].consumed_time, TIME_DATE | TIME_MINUTES) : "",
         DAL_M0001ConsumeReasonToString(events[i].consume_reason),
         DoubleToString(events[i].rtv, 6),
         DAL_BoolToString(events[i].rtv_ready),
         DAL_BoolToString(events[i].touch_confirmed),
         DAL_BoolToString(events[i].hunted),
         DoubleToString(events[i].mean_before, 6),
         DoubleToString(events[i].mean_inside, 6)
      );
   }

   FileClose(h);
}

#endif
