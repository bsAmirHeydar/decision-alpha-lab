#ifndef __FP_VALIDATION_ENGINE_MQH__
#define __FP_VALIDATION_ENGINE_MQH__
#property strict

#include "FP_ValidationAudit.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 13 Validation Engine
// ============================================================================

bool FP_ValidationWriteLine(const int handle, const string line)
{
   if(handle == INVALID_HANDLE) return false;
   FileWriteString(handle, line + "\r\n");
   return true;
}

bool FP_ValidationWriteCsv(const FP_ValidationConfig &cfg,
                           const string &rows[],
                           FP_ValidationReport &report)
{
   if(!cfg.write_csv) return true;
   FP_ExportEnsureFolder(cfg.folder);
   string path = FP_ValidationJoinPath(cfg.folder, FP_ValidationFileName(cfg));
   int handle = FileOpen(path, FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = report.reason + ";validation_open_failed_" + path;
      return false;
   }
   FP_ValidationWriteLine(handle, FP_ValidationHeader());
   for(int i=0; i<ArraySize(rows); i++)
      FP_ValidationWriteLine(handle, rows[i]);
   FileClose(handle);
   report.validation_file = path;
   report.files_written++;
   return true;
}

void FP_ValidationApplyReportToResult(const FP_ValidationReport &vr, FP_DetectResult &r)
{
   r.validation_attempted_total += (vr.attempted ? 1 : 0);
   r.validation_ok_total += (vr.ok ? 1 : 0);
   r.validation_checks_total += vr.checks_total;
   r.validation_pass_total += vr.checks_passed;
   r.validation_fail_total += vr.checks_failed;
   r.validation_warn_total += vr.checks_warned;
   r.validation_skipped_total += vr.checks_skipped;
   r.validation_file_errors_total += vr.file_errors;
}

bool FP_RunValidationWithReport(const string symbol,
                                const ENUM_TIMEFRAMES period,
                                const int bars,
                                const int scale_count,
                                const FP_ValidationConfig &cfg,
                                const FP_FlagEvent &events[],
                                const FP_HookBranch &hooks[],
                                const FP_DetectResult &result,
                                FP_ValidationReport &report,
                                string &rows[])
{
   FP_ResetValidationReport(report);
   ArrayResize(rows, 0);
   report.attempted = cfg.enabled;
   report.case_id = cfg.case_id;
   report.suite_tag = cfg.suite_tag;

   if(!cfg.enabled)
   {
      report.reason = "disabled";
      return false;
   }

   FP_ValidationCollectActuals(bars, scale_count, events, hooks, result, report);
   report.reason = "ok";

   FP_ValidationAddCheck(report, cfg, rows, "RANGE_BARS", "bars", "error", report.actual_bars, cfg.expected_min_bars, cfg.expected_max_bars, "bars_in_range", "bars_out_of_range");
   FP_ValidationAddCheck(report, cfg, rows, "RANGE_SCALES", "scales", "error", report.actual_scales, cfg.expected_min_scales, cfg.expected_max_scales, "scales_in_range", "scales_out_of_range");
   FP_ValidationAddCheck(report, cfg, rows, "RANGE_RAW_NODES", "raw_nodes", "error", report.actual_raw_nodes, cfg.expected_min_raw_nodes, cfg.expected_max_raw_nodes, "raw_nodes_in_range", "raw_nodes_out_of_range");
   FP_ValidationAddCheck(report, cfg, rows, "RANGE_CANONICAL_NODES", "canonical_nodes", "error", report.actual_canonical_nodes, cfg.expected_min_canonical_nodes, cfg.expected_max_canonical_nodes, "canonical_nodes_in_range", "canonical_nodes_out_of_range");
   FP_ValidationAddCheck(report, cfg, rows, "RANGE_HOOKS", "hooks", "error", report.actual_hooks, cfg.expected_min_hooks, cfg.expected_max_hooks, "hooks_in_range", "hooks_out_of_range");
   FP_ValidationAddCheck(report, cfg, rows, "RANGE_ND", "nd", "error", report.actual_nd, cfg.expected_min_nd, cfg.expected_max_nd, "nd_in_range", "nd_out_of_range");
   FP_ValidationAddCheck(report, cfg, rows, "RANGE_EVENTS", "events", "error", report.actual_events, cfg.expected_min_events, cfg.expected_max_events, "events_in_range", "events_out_of_range");
   FP_ValidationAddCheck(report, cfg, rows, "RANGE_VISIBLE_EVENTS", "visible_events", "error", report.actual_visible_events, cfg.expected_min_visible_events, cfg.expected_max_visible_events, "visible_events_in_range", "visible_events_out_of_range");
   FP_ValidationAddCheck(report, cfg, rows, "RANGE_HIDDEN_EVENTS", "hidden_events", "error", report.actual_hidden_events, cfg.expected_min_hidden_events, cfg.expected_max_hidden_events, "hidden_events_in_range", "hidden_events_out_of_range");
   FP_ValidationAddCheck(report, cfg, rows, "RANGE_F1", "f1", "error", report.actual_f1, cfg.expected_min_f1, cfg.expected_max_f1, "f1_in_range", "f1_out_of_range");
   FP_ValidationAddCheck(report, cfg, rows, "RANGE_F2", "f2", "error", report.actual_f2, cfg.expected_min_f2, cfg.expected_max_f2, "f2_in_range", "f2_out_of_range");
   FP_ValidationAddCheck(report, cfg, rows, "RANGE_F3", "f3", "error", report.actual_f3, cfg.expected_min_f3, cfg.expected_max_f3, "f3_in_range", "f3_out_of_range");
   FP_ValidationAddCheck(report, cfg, rows, "RANGE_LOCKED_F3", "locked_f3", "error", report.actual_locked_f3, cfg.expected_min_locked_f3, cfg.expected_max_locked_f3, "locked_f3_in_range", "locked_f3_out_of_range");

   FP_ValidationAddBoolCheck(report, cfg, rows, "INV_EVENT_COUNT", "visible_plus_hidden_equals_events", "error", (report.actual_visible_events + report.actual_hidden_events == report.actual_events), "event_partition_ok", "event_partition_mismatch");
   FP_ValidationAddBoolCheck(report, cfg, rows, "INV_HIDDEN_REASON", "hidden_events_have_reason", "error", (report.hidden_without_reason == 0), "hidden_reasons_complete", "hidden_event_without_reason");
   FP_ValidationAddBoolCheck(report, cfg, rows, "INV_VISIBLE_REASON", "visible_events_have_no_hidden_reason", "error", (report.visible_with_hidden_reason == 0), "visible_hidden_reason_clean", "visible_event_has_hidden_reason");
   FP_ValidationAddBoolCheck(report, cfg, rows, "INV_VISIBLE_PARENT", "visible_child_has_visible_parent", "error", (report.visible_child_without_visible_parent == 0), "visible_parent_chain_ok", "visible_child_parent_missing_or_hidden");
   FP_ValidationAddBoolCheck(report, cfg, rows, "INV_VISIBLE_CANONICAL_DUP", "visible_canonical_id_unique", "error", (report.visible_duplicate_canonical_id == 0), "visible_canonical_ids_unique", "visible_canonical_id_duplicate");

   if(cfg.require_no_canonical_failures)
      FP_ValidationAddBoolCheck(report, cfg, rows, "REQ_CANONICAL_CLEAN", "no_canonical_failures", "error", (report.canonical_failures == 0), "canonical_clean", "canonical_failures_present");
   if(cfg.require_render_ok)
      FP_ValidationAddBoolCheck(report, cfg, rows, "REQ_RENDER_OK", "renderer_ok", "error", (result.render_ok_total > 0 && report.render_errors == 0), "renderer_ok", "renderer_not_ok_or_errors");
   if(cfg.require_no_render_errors)
      FP_ValidationAddBoolCheck(report, cfg, rows, "REQ_RENDER_ERRORS", "no_render_errors", "error", (report.render_errors == 0), "render_errors_zero", "render_errors_present");
   if(cfg.require_export_ok)
      FP_ValidationAddBoolCheck(report, cfg, rows, "REQ_EXPORT_OK", "export_ok", "error", (result.export_ok_total > 0 && report.export_errors == 0), "export_ok", "export_not_ok_or_errors");
   if(cfg.require_no_export_errors)
      FP_ValidationAddBoolCheck(report, cfg, rows, "REQ_EXPORT_ERRORS", "no_export_errors", "error", (report.export_errors == 0), "export_errors_zero", "export_errors_present");

   if(cfg.strict)
      report.ok = (report.checks_failed == 0 && report.file_errors == 0);
   else
      report.ok = (report.file_errors == 0);

   if(!report.ok && report.reason == "ok") report.reason = "validation_failed";
   FP_ValidationWriteCsv(cfg, rows, report);
   if(report.file_errors > 0 && report.reason == "ok") report.reason = "validation_file_errors";
   if(cfg.strict) report.ok = (report.checks_failed == 0 && report.file_errors == 0);
   return report.ok;
}

#endif // __FP_VALIDATION_ENGINE_MQH__
