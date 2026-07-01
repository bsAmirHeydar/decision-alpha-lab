#ifndef __FP_STATE_GATE_RULES_MQH__
#define __FP_STATE_GATE_RULES_MQH__
#property strict

#include "FP_StateGateTypes.mqh"

string FP_L19Bool(const bool v)
{
   return (v ? "true" : "false");
}

string FP_L19Time(const datetime t)
{
   if(t <= 0)
      return "";
   return TimeToString(t, TIME_DATE|TIME_SECONDS);
}

string FP_L19SafeCsv(string v)
{
   StringReplace(v, "\"", "\"\"");
   return "\"" + v + "\"";
}

string FP_L19TfLabel(const ENUM_TIMEFRAMES tf)
{
   return EnumToString(tf);
}

string FP_L19StateStatus(const FP_Level19StateGateSnapshot &s)
{
   if(!s.timebase_ok)
      return "LEVEL19_TIMEBASE_NOT_OK_READ_ONLY";
   if(s.render_attempted && !s.render_ok)
      return "LEVEL19_RENDER_REPORTED_NOT_OK_READ_ONLY";
   if(s.validation_attempted && !s.validation_ok)
      return "LEVEL19_VALIDATION_REPORTED_NOT_OK_READ_ONLY";
   return "LEVEL19_STATE_GATE_READY_READ_ONLY";
}

string FP_L19StateKey(const FP_Level19StateGateSnapshot &s)
{
   string k = s.symbol;
   k += "|TF=" + s.period_label;
   k += "|BARS=" + IntegerToString(s.bars);
   k += "|EVENTS=" + IntegerToString(s.events_total);
   k += "|HOOKS=" + IntegerToString(s.hooks_total);
   k += "|F1=" + IntegerToString(s.f1_total);
   k += "|F2=" + IntegerToString(s.f2_total);
   k += "|F3=" + IntegerToString(s.f3_total);
   k += "|ND=" + IntegerToString(s.nd_total);
   k += "|CONTRACT=READ_ONLY_NO_TOUCH";
   return k;
}

void FP_L19BuildSnapshot(const string symbol,
                         const ENUM_TIMEFRAMES period,
                         const MqlRates &rates[],
                         const int bars,
                         const int scale_count,
                         const FP_FlagEvent &events[],
                         const FP_HookBranch &hooks[],
                         const FP_DetectResult &result,
                         const FP_TimebaseReport &timebase_report,
                         const FP_ExportReport &export_report,
                         const FP_RenderReport &render_report,
                         const FP_ValidationReport &validation_report,
                         FP_Level19StateGateSnapshot &s)
{
   FP_ResetLevel19StateGateSnapshot(s);

   s.generated_at = TimeCurrent();
   s.symbol = symbol;
   s.period = period;
   s.period_label = FP_L19TfLabel(period);
   s.bars = bars;
   s.scale_count = scale_count;

   s.timebase_ok = timebase_report.ok;
   s.timebase_status = timebase_report.status;
   s.timebase_reason = timebase_report.reason;
   s.first_bar_time = timebase_report.first_time;
   s.last_bar_time = timebase_report.last_time;

   s.raw_nodes_total = result.raw_nodes_total;
   s.nodes_total = result.nodes_total;
   s.confirmed_nodes_total = result.confirmed_nodes_total;
   s.pending_nodes_total = result.pending_nodes_total;
   s.hooks_total = result.hooks_total;
   s.events_total = result.events_total;
   s.visible_events_total = result.visible_events_total;
   s.hidden_events_total = result.hidden_events_total;
   s.f1_total = result.f1_total;
   s.f2_total = result.f2_total;
   s.f3_total = result.f3_total;
   s.nd_total = result.nd_total;

   s.input_events = ArraySize(events);
   s.input_hooks = ArraySize(hooks);

   for(int h=0; h<ArraySize(hooks); h++)
   {
      if(hooks[h].visible_main)
      {
         s.visible_hooks_seen++;
         s.latest_visible_hook_id = hooks[h].visual_id;
         s.latest_visible_hook_L = hooks[h].scale_L;
         s.latest_visible_hook_direction = hooks[h].direction;
         s.latest_visible_hook_status = hooks[h].status;
         s.latest_visible_hook_is_nd = hooks[h].is_nd;
         s.latest_visible_hook_node_count = hooks[h].node_count;
      }
   }

   for(int e=0; e<ArraySize(events); e++)
   {
      if(events[e].visible_main)
      {
         s.latest_visible_event_id = events[e].canonical_id;
         if(StringLen(s.latest_visible_event_id) <= 0)
            s.latest_visible_event_id = events[e].visual_id;
         s.latest_visible_event_level = events[e].level;
         s.latest_visible_event_L = events[e].scale_L;
         s.latest_visible_event_direction = events[e].direction;
         s.latest_visible_event_status = events[e].status;
      }
   }

   s.export_attempted = export_report.attempted;
   s.export_ok = export_report.ok;
   s.export_files_written = export_report.files_written;
   s.export_file_errors = export_report.file_errors;

   s.render_attempted = render_report.attempted;
   s.render_ok = render_report.ok;
   s.render_objects_created = render_report.objects_created;
   s.render_object_errors = render_report.object_create_failures;
   s.render_objects_deleted = render_report.objects_deleted_by_prefix;
   s.render_reason = render_report.reason;

   s.validation_attempted = validation_report.attempted;
   s.validation_ok = validation_report.ok;
   s.validation_failed = validation_report.checks_failed;
   s.validation_warned = validation_report.checks_warned;

   s.state_status = FP_L19StateStatus(s);
   s.state_key = FP_L19StateKey(s);
   s.no_touch_contract = "READ_ONLY_DIAGNOSTIC_ONLY_DOES_NOT_CALL_RENDERER_DOES_NOT_DELETE_RENDER_OBJECTS";
}


string FP_L19DeltaDirection(const int delta)
{
   if(delta > 0)
      return "UP";
   if(delta < 0)
      return "DOWN";
   return "FLAT";
}

string FP_L19BoolChange(const bool before_value, const bool after_value)
{
   if(before_value == after_value)
      return "UNCHANGED";
   if(after_value)
      return "FALSE_TO_TRUE";
   return "TRUE_TO_FALSE";
}

string FP_L19StringChange(const string before_value, const string after_value)
{
   if(before_value == after_value)
      return "UNCHANGED";
   if(StringLen(before_value) <= 0 && StringLen(after_value) > 0)
      return "EMPTY_TO_VALUE";
   if(StringLen(before_value) > 0 && StringLen(after_value) <= 0)
      return "VALUE_TO_EMPTY";
   return "CHANGED";
}

int FP_L19AbsInt(const int value)
{
   if(value < 0)
      return -value;
   return value;
}

string FP_L19DeltaStatus(const bool has_previous,
                         const FP_Level19StateGateSnapshot &previous,
                         const FP_Level19StateGateSnapshot &current)
{
   if(!has_previous)
      return "STATE_DELTA_BASELINE_FIRST_ROW";

   int movement = 0;
   movement += FP_L19AbsInt(current.events_total - previous.events_total);
   movement += FP_L19AbsInt(current.hooks_total - previous.hooks_total);
   movement += FP_L19AbsInt(current.f1_total - previous.f1_total);
   movement += FP_L19AbsInt(current.f2_total - previous.f2_total);
   movement += FP_L19AbsInt(current.f3_total - previous.f3_total);
   movement += FP_L19AbsInt(current.nd_total - previous.nd_total);
   movement += FP_L19AbsInt(current.visible_events_total - previous.visible_events_total);

   if(current.state_key != previous.state_key)
      movement++;
   if(current.latest_visible_event_id != previous.latest_visible_event_id)
      movement++;
   if(current.latest_visible_hook_id != previous.latest_visible_hook_id)
      movement++;
   if(current.render_ok != previous.render_ok)
      movement++;
   if(current.validation_ok != previous.validation_ok)
      movement++;

   if(movement <= 0)
      return "STATE_DELTA_NO_CHANGE";
   if(movement <= 2)
      return "STATE_DELTA_MINOR_CHANGE";
   if(movement <= 6)
      return "STATE_DELTA_STRUCTURAL_CHANGE";
   return "STATE_DELTA_MAJOR_CHANGE";
}

string FP_L19DeltaKey(const bool has_previous,
                      const FP_Level19StateGateSnapshot &previous,
                      const FP_Level19StateGateSnapshot &current)
{
   string key = current.symbol;
   key += "|TF=" + current.period_label;
   key += "|BAR=" + FP_L19Time(current.last_bar_time);
   key += "|PREV=" + (has_previous ? FP_L19Time(previous.last_bar_time) : "NO_PREVIOUS");
   key += "|EV_D=" + IntegerToString(has_previous ? current.events_total - previous.events_total : 0);
   key += "|HK_D=" + IntegerToString(has_previous ? current.hooks_total - previous.hooks_total : 0);
   key += "|F1_D=" + IntegerToString(has_previous ? current.f1_total - previous.f1_total : 0);
   key += "|F2_D=" + IntegerToString(has_previous ? current.f2_total - previous.f2_total : 0);
   key += "|F3_D=" + IntegerToString(has_previous ? current.f3_total - previous.f3_total : 0);
   key += "|NO_TOUCH=true";
   return key;
}

#endif // __FP_STATE_GATE_RULES_MQH__
