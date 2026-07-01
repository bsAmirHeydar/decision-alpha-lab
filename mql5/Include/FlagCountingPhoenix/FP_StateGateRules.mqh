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


string FP_L19TransitionFamily(const bool has_previous,
                              const FP_Level19StateGateSnapshot &previous,
                              const FP_Level19StateGateSnapshot &current)
{
   if(!has_previous)
      return "TRANSITION_BASELINE_FIRST_ROW";

   int f3_delta = current.f3_total - previous.f3_total;
   int f2_delta = current.f2_total - previous.f2_total;
   int f1_delta = current.f1_total - previous.f1_total;
   int nd_delta = current.nd_total - previous.nd_total;
   int hooks_delta = current.hooks_total - previous.hooks_total;
   int events_delta = current.events_total - previous.events_total;
   int visible_delta = current.visible_events_total - previous.visible_events_total;

   if(current.render_ok != previous.render_ok)
      return "TRANSITION_RENDER_HEALTH_CHANGE";
   if(current.validation_ok != previous.validation_ok)
      return "TRANSITION_VALIDATION_HEALTH_CHANGE";

   if(f3_delta > 0)
      return "TRANSITION_F3_EXPANSION";
   if(f2_delta > 0)
      return "TRANSITION_F2_EXPANSION";
   if(f1_delta > 0)
      return "TRANSITION_F1_EXPANSION";
   if(f3_delta < 0 || f2_delta < 0 || f1_delta < 0)
      return "TRANSITION_F_COUNT_CONTRACTION";

   if(nd_delta != 0)
      return "TRANSITION_ND_COUNT_CHANGE";
   if(hooks_delta != 0)
      return "TRANSITION_HOOK_COUNT_CHANGE";
   if(visible_delta != 0)
      return "TRANSITION_VISIBILITY_CHANGE";
   if(events_delta != 0)
      return "TRANSITION_EVENT_COUNT_CHANGE";

   if(current.latest_visible_event_id != previous.latest_visible_event_id)
      return "TRANSITION_LATEST_VISIBLE_EVENT_CHANGED";
   if(current.latest_visible_hook_id != previous.latest_visible_hook_id)
      return "TRANSITION_LATEST_VISIBLE_HOOK_CHANGED";
   if(current.state_key != previous.state_key)
      return "TRANSITION_STATE_KEY_CHANGED";

   return "TRANSITION_NO_CHANGE";
}

string FP_L19TransitionSeverity(const bool has_previous,
                                const FP_Level19StateGateSnapshot &previous,
                                const FP_Level19StateGateSnapshot &current)
{
   if(!has_previous)
      return "TRANSITION_SEVERITY_BASELINE";

   string family = FP_L19TransitionFamily(has_previous, previous, current);

   if(family == "TRANSITION_RENDER_HEALTH_CHANGE" ||
      family == "TRANSITION_VALIDATION_HEALTH_CHANGE")
      return "TRANSITION_SEVERITY_HEALTH";

   if(family == "TRANSITION_F3_EXPANSION" ||
      family == "TRANSITION_F2_EXPANSION")
      return "TRANSITION_SEVERITY_MAJOR";

   if(family == "TRANSITION_F1_EXPANSION" ||
      family == "TRANSITION_F_COUNT_CONTRACTION" ||
      family == "TRANSITION_ND_COUNT_CHANGE")
      return "TRANSITION_SEVERITY_STRUCTURAL";

   if(family == "TRANSITION_HOOK_COUNT_CHANGE" ||
      family == "TRANSITION_VISIBILITY_CHANGE" ||
      family == "TRANSITION_EVENT_COUNT_CHANGE" ||
      family == "TRANSITION_LATEST_VISIBLE_EVENT_CHANGED" ||
      family == "TRANSITION_LATEST_VISIBLE_HOOK_CHANGED" ||
      family == "TRANSITION_STATE_KEY_CHANGED")
      return "TRANSITION_SEVERITY_MINOR";

   return "TRANSITION_SEVERITY_NONE";
}

string FP_L19TransitionBiasHint(const bool has_previous,
                                const FP_Level19StateGateSnapshot &previous,
                                const FP_Level19StateGateSnapshot &current)
{
   if(!has_previous)
      return "BIAS_HINT_BASELINE_NO_PRIOR_STATE";

   if(current.latest_visible_event_direction > 0)
      return "BIAS_HINT_LATEST_VISIBLE_EVENT_BULLISH";
   if(current.latest_visible_event_direction < 0)
      return "BIAS_HINT_LATEST_VISIBLE_EVENT_BEARISH";
   if(current.latest_visible_hook_direction > 0)
      return "BIAS_HINT_LATEST_VISIBLE_HOOK_BULLISH";
   if(current.latest_visible_hook_direction < 0)
      return "BIAS_HINT_LATEST_VISIBLE_HOOK_BEARISH";

   return "BIAS_HINT_NEUTRAL_OR_UNKNOWN";
}

string FP_L19TransitionActionHint(const string family,
                                  const string severity)
{
   if(severity == "TRANSITION_SEVERITY_HEALTH")
      return "ACTION_HINT_REVIEW_REPORTS_ONLY_NO_EXECUTION";
   if(severity == "TRANSITION_SEVERITY_MAJOR")
      return "ACTION_HINT_MAJOR_STRUCTURAL_TRANSITION_OBSERVE_ONLY";
   if(severity == "TRANSITION_SEVERITY_STRUCTURAL")
      return "ACTION_HINT_STRUCTURAL_TRANSITION_OBSERVE_ONLY";
   if(severity == "TRANSITION_SEVERITY_MINOR")
      return "ACTION_HINT_MINOR_STATE_UPDATE_OBSERVE_ONLY";
   if(family == "TRANSITION_NO_CHANGE")
      return "ACTION_HINT_NO_CHANGE";
   return "ACTION_HINT_BASELINE_OR_UNKNOWN_NO_EXECUTION";
}

string FP_L19TransitionKey(const bool has_previous,
                           const FP_Level19StateGateSnapshot &previous,
                           const FP_Level19StateGateSnapshot &current)
{
   string family = FP_L19TransitionFamily(has_previous, previous, current);
   string severity = FP_L19TransitionSeverity(has_previous, previous, current);

   string key = current.symbol;
   key += "|TF=" + current.period_label;
   key += "|BAR=" + FP_L19Time(current.last_bar_time);
   key += "|FAMILY=" + family;
   key += "|SEVERITY=" + severity;
   key += "|EV_D=" + IntegerToString(has_previous ? current.events_total - previous.events_total : 0);
   key += "|HK_D=" + IntegerToString(has_previous ? current.hooks_total - previous.hooks_total : 0);
   key += "|F1_D=" + IntegerToString(has_previous ? current.f1_total - previous.f1_total : 0);
   key += "|F2_D=" + IntegerToString(has_previous ? current.f2_total - previous.f2_total : 0);
   key += "|F3_D=" + IntegerToString(has_previous ? current.f3_total - previous.f3_total : 0);
   key += "|EXEC=NO";
   return key;
}


string FP_L19RegimeLabel(const bool has_previous,
                         const FP_Level19StateGateSnapshot &previous,
                         const FP_Level19StateGateSnapshot &current)
{
   string family = FP_L19TransitionFamily(has_previous, previous, current);

   if(family == "TRANSITION_RENDER_HEALTH_CHANGE" ||
      family == "TRANSITION_VALIDATION_HEALTH_CHANGE")
      return "REGIME_HEALTH_REVIEW";

   if(family == "TRANSITION_F3_EXPANSION")
      return "REGIME_F3_STRUCTURAL_EXPANSION";
   if(family == "TRANSITION_F2_EXPANSION")
      return "REGIME_F2_STRUCTURAL_EXPANSION";
   if(family == "TRANSITION_F1_EXPANSION")
      return "REGIME_F1_STRUCTURAL_EXPANSION";
   if(family == "TRANSITION_F_COUNT_CONTRACTION")
      return "REGIME_F_COUNT_CONTRACTION";
   if(family == "TRANSITION_ND_COUNT_CHANGE")
      return "REGIME_ND_REBUILD";
   if(family == "TRANSITION_HOOK_COUNT_CHANGE")
      return "REGIME_HOOK_REBUILD";
   if(family == "TRANSITION_VISIBILITY_CHANGE")
      return "REGIME_VISIBILITY_RESHUFFLE";
   if(family == "TRANSITION_NO_CHANGE")
      return "REGIME_STABLE_NO_CHANGE";

   return "REGIME_OBSERVE_ONLY_UNCLASSIFIED";
}

string FP_L19RegimeQualityHint(const string regime_label,
                               const string severity,
                               const int stability_streak)
{
   if(regime_label == "REGIME_HEALTH_REVIEW")
      return "REGIME_QUALITY_HEALTH_BLOCKED";
   if(stability_streak >= 5 && severity != "TRANSITION_SEVERITY_HEALTH")
      return "REGIME_QUALITY_STABLE_OBSERVATION";
   if(severity == "TRANSITION_SEVERITY_MAJOR")
      return "REGIME_QUALITY_MAJOR_TRANSITION_OBSERVATION";
   if(severity == "TRANSITION_SEVERITY_STRUCTURAL")
      return "REGIME_QUALITY_STRUCTURAL_OBSERVATION";
   if(severity == "TRANSITION_SEVERITY_MINOR")
      return "REGIME_QUALITY_MINOR_OBSERVATION";
   return "REGIME_QUALITY_NEUTRAL_OBSERVATION";
}

string FP_L19CompletionStatus(const FP_Level19StateGateSnapshot &current)
{
   if(!current.timebase_ok)
      return "LEVEL19_COMPLETE_BLOCKED_TIMEBASE";
   if(current.render_attempted && !current.render_ok)
      return "LEVEL19_COMPLETE_RENDER_HEALTH_REVIEW";
   if(current.validation_attempted && !current.validation_ok)
      return "LEVEL19_COMPLETE_VALIDATION_HEALTH_REVIEW";
   if(current.events_total <= 0 && current.hooks_total <= 0)
      return "LEVEL19_COMPLETE_EMPTY_STATE_OBSERVED";
   return "LEVEL19_COMPLETE_READY_FOR_LEVEL20_ENTRY_BRIDGE";
}

string FP_L19CompletionNextStep(const string completion_status)
{
   if(completion_status == "LEVEL19_COMPLETE_READY_FOR_LEVEL20_ENTRY_BRIDGE")
      return "NEXT_LEVEL_20_ENTRY_BRIDGE_XY_ANCHOR_JOIN";
   if(completion_status == "LEVEL19_COMPLETE_BLOCKED_TIMEBASE")
      return "FIX_TIMEBASE_BEFORE_LEVEL20";
   if(completion_status == "LEVEL19_COMPLETE_RENDER_HEALTH_REVIEW")
      return "REVIEW_RENDER_REPORT_BEFORE_LEVEL20";
   if(completion_status == "LEVEL19_COMPLETE_VALIDATION_HEALTH_REVIEW")
      return "REVIEW_VALIDATION_REPORT_BEFORE_LEVEL20";
   return "KEEP_OBSERVING_UNTIL_STATE_AVAILABLE";
}

#endif // __FP_STATE_GATE_RULES_MQH__
