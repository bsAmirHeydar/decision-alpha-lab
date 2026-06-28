#ifndef __FP_VALIDATION_RULES_MQH__
#define __FP_VALIDATION_RULES_MQH__
#property strict

#include "FP_ValidationTypes.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 13 Validation Rules
// ============================================================================

string FP_ValidationBool(const bool v)
{
   return (v ? "true" : "false");
}

string FP_ValidationInt(const int v)
{
   return IntegerToString(v);
}

string FP_ValidationSafeName(const string raw)
{
   return FP_ExportSafeName(raw);
}

string FP_ValidationFileName(const FP_ValidationConfig &cfg)
{
   string id = FP_ValidationSafeName(cfg.case_id);
   if(id == "") id = "manual";
   if(cfg.overwrite_latest) return "latest_validation.csv";
   return id + "_validation.csv";
}

string FP_ValidationJoinPath(const string folder, const string file_name)
{
   return FP_ExportJoinPath(folder, file_name);
}

bool FP_ValidationEventIdVisible(const FP_FlagEvent &events[], const int event_id)
{
   if(event_id < 0) return false;
   for(int i=0; i<ArraySize(events); i++)
   {
      if(events[i].event_id == event_id)
         return events[i].visible_main;
   }
   return false;
}

int FP_ValidationCountLockedF3(const FP_FlagEvent &events[])
{
   int n = 0;
   for(int i=0; i<ArraySize(events); i++)
   {
      if(events[i].level == FP_LEVEL_F3 && (events[i].f3_locked || events[i].status == FP_STATUS_LOCKED))
         n++;
   }
   return n;
}

void FP_ValidationCollectActuals(const int bars,
                                 const int scale_count,
                                 const FP_FlagEvent &events[],
                                 const FP_HookBranch &hooks[],
                                 const FP_DetectResult &result,
                                 FP_ValidationReport &report)
{
   report.actual_bars = bars;
   report.actual_scales = scale_count;
   report.actual_raw_nodes = result.raw_nodes_total;
   report.actual_canonical_nodes = result.nodes_total;
   report.actual_hooks = ArraySize(hooks);
   report.actual_nd = result.nd_total;
   report.actual_events = ArraySize(events);
   report.actual_visible_events = 0;
   report.actual_hidden_events = 0;
   report.actual_f1 = 0;
   report.actual_f2 = 0;
   report.actual_f3 = 0;
   report.actual_locked_f3 = 0;
   report.visible_with_hidden_reason = 0;
   report.hidden_without_reason = 0;
   report.visible_child_without_visible_parent = 0;
   report.visible_duplicate_canonical_id = 0;

   for(int i=0; i<ArraySize(events); i++)
   {
      if(events[i].visible_main) report.actual_visible_events++;
      else report.actual_hidden_events++;

      if(events[i].level == FP_LEVEL_F1) report.actual_f1++;
      if(events[i].level == FP_LEVEL_F2) report.actual_f2++;
      if(events[i].level == FP_LEVEL_F3) report.actual_f3++;
      if(events[i].level == FP_LEVEL_F3 && (events[i].f3_locked || events[i].status == FP_STATUS_LOCKED)) report.actual_locked_f3++;

      if(events[i].visible_main && events[i].hidden_reason != "") report.visible_with_hidden_reason++;
      if(!events[i].visible_main && events[i].hidden_reason == "") report.hidden_without_reason++;
      if(events[i].visible_main && events[i].level != FP_LEVEL_F1 && events[i].parent_event_id >= 0 && !FP_ValidationEventIdVisible(events, events[i].parent_event_id))
         report.visible_child_without_visible_parent++;
   }

   for(int a=0; a<ArraySize(events); a++)
   {
      if(!events[a].visible_main || events[a].canonical_id == "") continue;
      for(int b=a+1; b<ArraySize(events); b++)
      {
         if(!events[b].visible_main || events[b].canonical_id == "") continue;
         if(events[a].canonical_id == events[b].canonical_id)
            report.visible_duplicate_canonical_id++;
      }
   }

   report.canonical_failures = result.canonical_invariant_failures_total +
                               result.canonical_visible_duplicate_after_total +
                               result.canonical_parent_missing_after_total;
   report.render_errors = result.render_object_errors_total + result.render_duplicate_names_total;
   report.export_errors = result.export_file_errors_total;
}

string FP_ValidationRangeText(const int min_expected, const int max_expected)
{
   if(min_expected < 0 && max_expected < 0) return "unbounded";
   if(min_expected >= 0 && max_expected >= 0) return "[" + IntegerToString(min_expected) + "," + IntegerToString(max_expected) + "]";
   if(min_expected >= 0) return ">=" + IntegerToString(min_expected);
   return "<=" + IntegerToString(max_expected);
}

bool FP_ValidationRangePass(const int actual, const int min_expected, const int max_expected)
{
   if(min_expected >= 0 && actual < min_expected) return false;
   if(max_expected >= 0 && actual > max_expected) return false;
   return true;
}

#endif // __FP_VALIDATION_RULES_MQH__
