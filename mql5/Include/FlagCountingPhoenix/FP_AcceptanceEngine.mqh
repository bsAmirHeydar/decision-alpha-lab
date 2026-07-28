#ifndef __FP_ACCEPTANCE_ENGINE_MQH__
#define __FP_ACCEPTANCE_ENGINE_MQH__
#property strict

#include "FP_ExportEngine.mqh"
#include "FP_AcceptanceAudit.mqh"
#include <AlphaLab/UC04/AL_UC04CorePrimitives.mqh>

// ============================================================================
// Phoenix Level 16 - Acceptance Matrix Engine
// ============================================================================

bool FP_AcceptanceWriteLine(const int handle, const string line)
{
   return AL_UC04WriteLine(handle, line);
}

bool FP_AcceptanceWriteCsv(const FP_AcceptanceConfig &cfg,
                           const string &rows[],
                           FP_AcceptanceReport &report)
{
   if(!cfg.write_csv) return true;
   FP_ExportEnsureFolder(cfg.folder);
   string path = cfg.folder + "/" + FP_AcceptanceFileName(cfg);
   int handle = FileOpen(path, FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = report.reason + ";acceptance_open_failed_" + path;
      return false;
   }
   FP_AcceptanceWriteLine(handle, FP_AcceptanceHeader());
   for(int i=0; i<ArraySize(rows); i++)
      FP_AcceptanceWriteLine(handle, rows[i]);
   FileClose(handle);
   report.report_file = path;
   report.files_written++;
   return true;
}

void FP_AcceptanceFinalizeReport(const FP_AcceptanceConfig &cfg,
                                 const string &rows[],
                                 FP_AcceptanceReport &report)
{
   report.ok = (report.checks_failed == 0 && report.file_errors == 0);
   if(report.reason == "") report.reason = (report.ok ? "ok" : "acceptance_matrix_failed");
   FP_AcceptanceWriteCsv(cfg, rows, report);
   report.ok = (report.checks_failed == 0 && report.file_errors == 0);
   if(!report.ok && report.reason == "ok") report.reason = "acceptance_matrix_failed";
}

bool FP_RunAcceptanceWithReport(const string symbol,
                                const ENUM_TIMEFRAMES period,
                                const FP_AcceptanceConfig &cfg,
                                const FP_TimebaseReport &timebase_report,
                                const FP_DetectResult &result,
                                const FP_ExportReport &export_report,
                                const FP_RenderReport &render_report,
                                const FP_ValidationReport &validation_report,
                                const FP_ReleaseReport &release_report,
                                const FP_InterfaceReport &interface_pre_report,
                                const FP_InterfaceReport &interface_post_report,
                                FP_AcceptanceReport &report,
                                string &rows[])
{
   FP_ResetAcceptanceReport(report);
   ArrayResize(rows, 0);
   report.attempted = cfg.enabled;
   report.mode_name = FP_AcceptanceModeName(cfg.mode);
   report.case_id = cfg.case_id;
   report.folder = cfg.folder;
   report.run_id = FP_AcceptanceRunId(symbol, period, cfg);
   if(!cfg.enabled)
   {
      report.reason = "acceptance_disabled";
      return false;
   }

   FP_AcceptanceAddOrderChecks(report, rows, cfg);
   FP_AcceptanceAddRuntimeChecks(report, rows, cfg, timebase_report, result, export_report, render_report, validation_report, release_report, interface_pre_report, interface_post_report);
   FP_AcceptanceAddMatrixChecks(report, rows, cfg, result);

   FP_AcceptanceFinalizeReport(cfg, rows, report);
   return report.ok;
}

void FP_AcceptanceApplyReportToResult(const FP_AcceptanceReport &ar, FP_DetectResult &r)
{
   r.acceptance_attempted_total += (ar.attempted ? 1 : 0);
   r.acceptance_ok_total += (ar.ok ? 1 : 0);
   r.acceptance_checks_total += ar.checks_total;
   r.acceptance_pass_total += ar.checks_passed;
   r.acceptance_fail_total += ar.checks_failed;
   r.acceptance_warn_total += ar.checks_warned;
   r.acceptance_skipped_total += ar.checks_skipped;
   r.acceptance_file_errors_total += ar.file_errors;
   r.acceptance_hard_gates_total += ar.hard_gates_total;
   r.acceptance_hard_gate_fail_total += ar.hard_gates_failed;
   r.acceptance_order_errors_total += ar.order_errors;
   r.acceptance_dependency_errors_total += ar.dependency_errors;
   r.acceptance_matrix_errors_total += ar.matrix_errors;
   r.acceptance_invariant_errors_total += ar.invariant_errors;
}

#endif // __FP_ACCEPTANCE_ENGINE_MQH__
