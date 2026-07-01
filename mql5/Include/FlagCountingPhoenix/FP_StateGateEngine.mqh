#ifndef __FP_STATE_GATE_ENGINE_MQH__
#define __FP_STATE_GATE_ENGINE_MQH__
#property strict

#include "FP_StateGateExport.mqh"

datetime g_fp_level19_last_ledger_bar_time = 0;
datetime g_fp_level19_last_delta_bar_time = 0;
datetime g_fp_level19_last_transition_bar_time = 0;
bool g_fp_level19_delta_initialized = false;
FP_Level19StateGateSnapshot g_fp_level19_previous_delta_snapshot;

int g_fp_level19_transition_total_rows = 0;
int g_fp_level19_transition_baseline_rows = 0;
int g_fp_level19_transition_no_change_rows = 0;
int g_fp_level19_transition_health_rows = 0;
int g_fp_level19_transition_major_rows = 0;
int g_fp_level19_transition_structural_rows = 0;
int g_fp_level19_transition_minor_rows = 0;
int g_fp_level19_transition_f1_rows = 0;
int g_fp_level19_transition_f2_rows = 0;
int g_fp_level19_transition_f3_rows = 0;
int g_fp_level19_transition_f_contraction_rows = 0;
int g_fp_level19_transition_nd_rows = 0;
int g_fp_level19_transition_hook_rows = 0;
int g_fp_level19_transition_visibility_rows = 0;
int g_fp_level19_transition_event_count_rows = 0;
int g_fp_level19_transition_latest_event_rows = 0;
int g_fp_level19_transition_latest_hook_rows = 0;
int g_fp_level19_transition_state_key_rows = 0;
string g_fp_level19_previous_transition_family = "NO_PREVIOUS_TRANSITION";
int g_fp_level19_transition_family_streak = 0;

// ============================================================================
// FlagCounting Phoenix - Level 19 Clean Isolated State Gate Engine
// ----------------------------------------------------------------------------
// Read-only diagnostic layer. It does not call FP_Draw*, FP_DeleteObjectsByPrefix,
// order functions, or any structural mutation.
// ============================================================================

bool FP_L19ShouldWriteClosedBarLedger(const FP_Level19StateGateSnapshot &snapshot,
                                      FP_Level19StateGateReport &report)
{
   if(snapshot.last_bar_time <= 0)
      return false;

   if(g_fp_level19_last_ledger_bar_time == snapshot.last_bar_time)
   {
      report.ledger_skipped_duplicate_bar = true;
      return false;
   }

   g_fp_level19_last_ledger_bar_time = snapshot.last_bar_time;
   return true;
}


bool FP_L19ShouldWriteStateDeltaLedger(const FP_Level19StateGateSnapshot &snapshot,
                                     FP_Level19StateGateReport &report)
{
   if(snapshot.last_bar_time <= 0)
      return false;

   if(g_fp_level19_last_delta_bar_time == snapshot.last_bar_time)
   {
      report.state_delta_skipped_duplicate_bar = true;
      return false;
   }

   g_fp_level19_last_delta_bar_time = snapshot.last_bar_time;
   return true;
}


bool FP_L19ShouldWriteTransitionEventLedger(const FP_Level19StateGateSnapshot &snapshot,
                                           FP_Level19StateGateReport &report)
{
   if(snapshot.last_bar_time <= 0)
      return false;

   if(g_fp_level19_last_transition_bar_time == snapshot.last_bar_time)
   {
      report.transition_event_skipped_duplicate_bar = true;
      return false;
   }

   g_fp_level19_last_transition_bar_time = snapshot.last_bar_time;
   return true;
}


void FP_L19UpdateCompleteObservationStats(const string family,
                                           const string severity)
{
   g_fp_level19_transition_total_rows++;

   if(family == "TRANSITION_BASELINE_FIRST_ROW")
      g_fp_level19_transition_baseline_rows++;
   else if(family == "TRANSITION_NO_CHANGE")
      g_fp_level19_transition_no_change_rows++;
   else if(family == "TRANSITION_F1_EXPANSION")
      g_fp_level19_transition_f1_rows++;
   else if(family == "TRANSITION_F2_EXPANSION")
      g_fp_level19_transition_f2_rows++;
   else if(family == "TRANSITION_F3_EXPANSION")
      g_fp_level19_transition_f3_rows++;
   else if(family == "TRANSITION_F_COUNT_CONTRACTION")
      g_fp_level19_transition_f_contraction_rows++;
   else if(family == "TRANSITION_ND_COUNT_CHANGE")
      g_fp_level19_transition_nd_rows++;
   else if(family == "TRANSITION_HOOK_COUNT_CHANGE")
      g_fp_level19_transition_hook_rows++;
   else if(family == "TRANSITION_VISIBILITY_CHANGE")
      g_fp_level19_transition_visibility_rows++;
   else if(family == "TRANSITION_EVENT_COUNT_CHANGE")
      g_fp_level19_transition_event_count_rows++;
   else if(family == "TRANSITION_LATEST_VISIBLE_EVENT_CHANGED")
      g_fp_level19_transition_latest_event_rows++;
   else if(family == "TRANSITION_LATEST_VISIBLE_HOOK_CHANGED")
      g_fp_level19_transition_latest_hook_rows++;
   else if(family == "TRANSITION_STATE_KEY_CHANGED")
      g_fp_level19_transition_state_key_rows++;

   if(severity == "TRANSITION_SEVERITY_HEALTH")
      g_fp_level19_transition_health_rows++;
   else if(severity == "TRANSITION_SEVERITY_MAJOR")
      g_fp_level19_transition_major_rows++;
   else if(severity == "TRANSITION_SEVERITY_STRUCTURAL")
      g_fp_level19_transition_structural_rows++;
   else if(severity == "TRANSITION_SEVERITY_MINOR")
      g_fp_level19_transition_minor_rows++;

   if(family == g_fp_level19_previous_transition_family)
      g_fp_level19_transition_family_streak++;
   else
   {
      g_fp_level19_previous_transition_family = family;
      g_fp_level19_transition_family_streak = 1;
   }
}

string FP_L19DominantFamily()
{
   string best = "TRANSITION_NO_DOMINANT";
   int best_count = -1;

   if(g_fp_level19_transition_f3_rows > best_count) { best = "TRANSITION_F3_EXPANSION"; best_count = g_fp_level19_transition_f3_rows; }
   if(g_fp_level19_transition_f2_rows > best_count) { best = "TRANSITION_F2_EXPANSION"; best_count = g_fp_level19_transition_f2_rows; }
   if(g_fp_level19_transition_f1_rows > best_count) { best = "TRANSITION_F1_EXPANSION"; best_count = g_fp_level19_transition_f1_rows; }
   if(g_fp_level19_transition_f_contraction_rows > best_count) { best = "TRANSITION_F_COUNT_CONTRACTION"; best_count = g_fp_level19_transition_f_contraction_rows; }
   if(g_fp_level19_transition_nd_rows > best_count) { best = "TRANSITION_ND_COUNT_CHANGE"; best_count = g_fp_level19_transition_nd_rows; }
   if(g_fp_level19_transition_hook_rows > best_count) { best = "TRANSITION_HOOK_COUNT_CHANGE"; best_count = g_fp_level19_transition_hook_rows; }
   if(g_fp_level19_transition_visibility_rows > best_count) { best = "TRANSITION_VISIBILITY_CHANGE"; best_count = g_fp_level19_transition_visibility_rows; }
   if(g_fp_level19_transition_event_count_rows > best_count) { best = "TRANSITION_EVENT_COUNT_CHANGE"; best_count = g_fp_level19_transition_event_count_rows; }
   if(g_fp_level19_transition_no_change_rows > best_count) { best = "TRANSITION_NO_CHANGE"; best_count = g_fp_level19_transition_no_change_rows; }
   if(g_fp_level19_transition_baseline_rows > best_count) { best = "TRANSITION_BASELINE_FIRST_ROW"; best_count = g_fp_level19_transition_baseline_rows; }

   return best;
}

string FP_L19DominantSeverity()
{
   string best = "TRANSITION_SEVERITY_NONE";
   int best_count = -1;

   if(g_fp_level19_transition_health_rows > best_count) { best = "TRANSITION_SEVERITY_HEALTH"; best_count = g_fp_level19_transition_health_rows; }
   if(g_fp_level19_transition_major_rows > best_count) { best = "TRANSITION_SEVERITY_MAJOR"; best_count = g_fp_level19_transition_major_rows; }
   if(g_fp_level19_transition_structural_rows > best_count) { best = "TRANSITION_SEVERITY_STRUCTURAL"; best_count = g_fp_level19_transition_structural_rows; }
   if(g_fp_level19_transition_minor_rows > best_count) { best = "TRANSITION_SEVERITY_MINOR"; best_count = g_fp_level19_transition_minor_rows; }

   return best;
}


void FP_RunLevel19StateGate(const string symbol,
                            const ENUM_TIMEFRAMES period,
                            const MqlRates &rates[],
                            const int bars,
                            const int &scales[],
                            const int scale_count,
                            const FP_FlagEvent &events[],
                            const FP_HookBranch &hooks[],
                            const FP_DetectResult &result,
                            const FP_TimebaseReport &timebase_report,
                            const FP_ExportReport &export_report,
                            const FP_RenderReport &render_report,
                            const FP_ValidationReport &validation_report,
                            const FP_Level19StateGateConfig &cfg,
                            FP_Level19StateGateReport &report)
{
   FP_ResetLevel19StateGateReport(report);
   report.attempted = cfg.enabled;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "LEVEL19_DISABLED";
      report.reason = "InpLevel19StateGateEnabled_false";
      return;
   }

   FP_Level19StateGateSnapshot snapshot;
   FP_L19BuildSnapshot(symbol, period, rates, bars, scale_count, events, hooks, result,
                       timebase_report, export_report, render_report, validation_report, snapshot);

   bool export_ok = FP_L19ExportSnapshot(cfg, snapshot, report);

   bool ledger_ok = true;
   if(cfg.export_closed_bar_ledger_csv && FP_L19ShouldWriteClosedBarLedger(snapshot, report))
      ledger_ok = FP_L19AppendClosedBarLedger(cfg, snapshot, report);

   bool delta_ok = true;
   bool transition_ok = true;
   bool has_previous_snapshot = g_fp_level19_delta_initialized;
   FP_Level19StateGateSnapshot previous_snapshot = g_fp_level19_previous_delta_snapshot;

   if(cfg.export_state_delta_csv && FP_L19ShouldWriteStateDeltaLedger(snapshot, report))
   {
      delta_ok = FP_L19AppendStateDeltaLedger(cfg, has_previous_snapshot,
                                             previous_snapshot,
                                             snapshot, report);
   }

   string transition_family = FP_L19TransitionFamily(has_previous_snapshot, previous_snapshot, snapshot);
   string transition_severity = FP_L19TransitionSeverity(has_previous_snapshot, previous_snapshot, snapshot);
   string bias_hint = FP_L19TransitionBiasHint(has_previous_snapshot, previous_snapshot, snapshot);
   string action_hint = FP_L19TransitionActionHint(transition_family, transition_severity);
   string previous_family = g_fp_level19_previous_transition_family;

   if(cfg.export_transition_event_csv && FP_L19ShouldWriteTransitionEventLedger(snapshot, report))
   {
      transition_ok = FP_L19AppendTransitionEventLedger(cfg, has_previous_snapshot,
                                                       previous_snapshot,
                                                       snapshot, report);
   }

   bool summary_ok = true;
   bool stability_ok = true;
   bool regime_ok = true;
   bool completion_ok = true;

   if(delta_ok && transition_ok)
   {
      FP_L19UpdateCompleteObservationStats(transition_family, transition_severity);

      summary_ok = FP_L19WriteTransitionSummary(cfg, snapshot,
                                                g_fp_level19_transition_total_rows,
                                                g_fp_level19_transition_baseline_rows,
                                                g_fp_level19_transition_no_change_rows,
                                                g_fp_level19_transition_health_rows,
                                                g_fp_level19_transition_major_rows,
                                                g_fp_level19_transition_structural_rows,
                                                g_fp_level19_transition_minor_rows,
                                                g_fp_level19_transition_f1_rows,
                                                g_fp_level19_transition_f2_rows,
                                                g_fp_level19_transition_f3_rows,
                                                g_fp_level19_transition_f_contraction_rows,
                                                g_fp_level19_transition_nd_rows,
                                                g_fp_level19_transition_hook_rows,
                                                g_fp_level19_transition_visibility_rows,
                                                g_fp_level19_transition_event_count_rows,
                                                g_fp_level19_transition_latest_event_rows,
                                                g_fp_level19_transition_latest_hook_rows,
                                                g_fp_level19_transition_state_key_rows,
                                                FP_L19DominantFamily(),
                                                FP_L19DominantSeverity(),
                                                report);

      stability_ok = FP_L19AppendTransitionStability(cfg, snapshot, transition_family,
                                                     transition_severity, previous_family,
                                                     g_fp_level19_transition_family_streak,
                                                     bias_hint, action_hint, report);

      string regime_label = FP_L19RegimeLabel(has_previous_snapshot, previous_snapshot, snapshot);
      string regime_quality = FP_L19RegimeQualityHint(regime_label, transition_severity,
                                                      g_fp_level19_transition_family_streak);
      string completion_status = FP_L19CompletionStatus(snapshot);
      string next_step = FP_L19CompletionNextStep(completion_status);

      regime_ok = FP_L19AppendRegimeLabel(cfg, snapshot, regime_label, regime_quality,
                                          transition_family, transition_severity,
                                          g_fp_level19_transition_family_streak,
                                          bias_hint, action_hint, completion_status,
                                          next_step, report);

      completion_ok = FP_L19WriteCompletion(cfg, snapshot, completion_status, next_step, report);

      g_fp_level19_previous_delta_snapshot = snapshot;
      g_fp_level19_delta_initialized = true;
   }

   FP_L19PanelDraw(cfg, snapshot, report);

   report.ok = (export_ok && ledger_ok && delta_ok && transition_ok && summary_ok && stability_ok && regime_ok && completion_ok && report.file_errors == 0 && report.panel_object_errors == 0);
   report.status = snapshot.state_status;
   report.reason = snapshot.no_touch_contract;
}

void FP_PrintLevel19StateGateReport(const string tag,
                                    const FP_Level19StateGateReport &report)
{
   string line = tag;
   line += " attempted=" + FP_L19Bool(report.attempted);
   line += " ok=" + FP_L19Bool(report.ok);
   line += " status=" + report.status;
   line += " reason=" + report.reason;
   line += " files_written=" + IntegerToString(report.files_written);
   line += " file_errors=" + IntegerToString(report.file_errors);
   line += " ledger_written=" + FP_L19Bool(report.ledger_written);
   line += " ledger_duplicate_skip=" + FP_L19Bool(report.ledger_skipped_duplicate_bar);
   line += " delta_written=" + FP_L19Bool(report.state_delta_written);
   line += " delta_duplicate_skip=" + FP_L19Bool(report.state_delta_skipped_duplicate_bar);
   line += " transition_written=" + FP_L19Bool(report.transition_event_written);
   line += " transition_duplicate_skip=" + FP_L19Bool(report.transition_event_skipped_duplicate_bar);
   line += " summary_written=" + FP_L19Bool(report.transition_summary_written);
   line += " stability_written=" + FP_L19Bool(report.transition_stability_written);
   line += " regime_written=" + FP_L19Bool(report.regime_label_written);
   line += " completion_written=" + FP_L19Bool(report.completion_written);
   line += " panel_created=" + IntegerToString(report.panel_objects_created);
   line += " panel_errors=" + IntegerToString(report.panel_object_errors);
   line += " panel_deleted=" + IntegerToString(report.panel_objects_deleted);
   Print(line);
}

#endif // __FP_STATE_GATE_ENGINE_MQH__
