#ifndef __FP_STATIC_QA_ENGINE_MQH__
#define __FP_STATIC_QA_ENGINE_MQH__
#property strict

#include "FP_ExportEngine.mqh"
#include "FP_StaticQaAudit.mqh"
#include <AlphaLab/UC04/AL_UC04CorePrimitives.mqh>

// ============================================================================
// Phoenix Level 18 - Static QA / Compile Hardening Engine
// ============================================================================

bool FP_StaticQaWriteLine(const int handle, const string line)
{
   return AL_UC04WriteLine(handle, line);
}

bool FP_StaticQaWriteCsv(const FP_StaticQaConfig &cfg,
                         const string &rows[],
                         FP_StaticQaReport &report)
{
   if(!cfg.write_csv) return true;
   FP_ExportEnsureFolder(cfg.folder);
   string path = cfg.folder + "/" + FP_StaticQaFileName(cfg);
   int handle = FileOpen(path, FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = report.reason + ";static_qa_open_failed_" + path;
      return false;
   }
   FP_StaticQaWriteLine(handle, FP_StaticQaHeader());
   for(int i=0; i<ArraySize(rows); i++)
      FP_StaticQaWriteLine(handle, rows[i]);
   FileClose(handle);
   report.report_file = path;
   report.files_written++;
   return true;
}

void FP_StaticQaFinalizeReport(const FP_StaticQaConfig &cfg,
                               const string &rows[],
                               FP_StaticQaReport &report)
{
   bool no_blockers = (!cfg.require_zero_runtime_blockers || report.blockers <= 0);
   report.ok = (report.checks_failed == 0 && report.file_errors == 0 && no_blockers);
   if(report.reason == "") report.reason = (report.ok ? "ok" : "static_qa_failed");
   FP_StaticQaWriteCsv(cfg, rows, report);
   no_blockers = (!cfg.require_zero_runtime_blockers || report.blockers <= 0);
   report.ok = (report.checks_failed == 0 && report.file_errors == 0 && no_blockers);
   if(!report.ok && report.reason == "ok") report.reason = "static_qa_failed";
}

bool FP_RunStaticQaWithReport(const string symbol,
                              const ENUM_TIMEFRAMES period,
                              const FP_StaticQaConfig &qa_cfg,
                              const FP_TimebaseConfig &timebase_cfg,
                              const FP_TimebaseReport &timebase_report,
                              const FP_Config &engine_cfg,
                              const FP_ExportConfig &export_cfg,
                              const FP_RenderConfig &render_cfg,
                              const FP_ValidationConfig &validation_cfg,
                              const FP_ReleaseConfig &release_cfg,
                              const FP_InterfaceConfig &interface_cfg,
                              const FP_AcceptanceConfig &acceptance_cfg,
                              const FP_AmbiguityConfig &ambiguity_cfg,
                              const FP_DetectResult &result,
                              const FP_ExportReport &export_report,
                              const FP_RenderReport &render_report,
                              const FP_ValidationReport &validation_report,
                              const FP_ReleaseReport &release_report,
                              const FP_InterfaceReport &interface_post_report,
                              const FP_AcceptanceReport &acceptance_report,
                              const FP_AmbiguityReport &ambiguity_report,
                              FP_StaticQaReport &report,
                              string &rows[])
{
   FP_ResetStaticQaReport(report);
   ArrayResize(rows, 0);
   report.attempted = qa_cfg.enabled;
   report.mode_name = FP_StaticQaModeName(qa_cfg.mode);
   report.case_id = qa_cfg.case_id;
   report.folder = qa_cfg.folder;
   report.run_id = FP_StaticQaRunId(symbol, period, qa_cfg);
   if(!qa_cfg.enabled)
   {
      report.reason = "static_qa_disabled";
      return false;
   }

   FP_StaticQaAddCompileContractChecks(report, rows, qa_cfg, engine_cfg);
   FP_StaticQaAddRuntimeContractChecks(report, rows, qa_cfg, timebase_report, result);
   FP_StaticQaAddCounterChecks(report, rows, qa_cfg, result);
   FP_StaticQaAddPrintSafetyChecks(report, rows, qa_cfg);
   FP_StaticQaAddInputContractChecks(report, rows, qa_cfg, timebase_cfg, engine_cfg, render_cfg, interface_cfg, ambiguity_cfg);
   FP_StaticQaAddDependencyChecks(report, rows, qa_cfg, export_cfg, render_cfg, validation_cfg, release_report, interface_post_report, acceptance_report, ambiguity_report);
   FP_StaticQaAddIoChecks(report, rows, qa_cfg, export_report, render_report, validation_report);

   // Release config is intentionally consumed here so future profile-level
   // compile hardening can add strict gates without changing the public facade.
   if(release_cfg.profile == FP_RELEASE_PROFILE_SAFE_ROLLBACK)
      FP_StaticQaAddCheck(report, rows, "dependency", "SAFE_ROLLBACK_MODE", "warn", true, "safe_rollback", "allowed", "static_qa_can_run_in_rollback_profile");
   if(acceptance_cfg.enabled && ambiguity_cfg.enabled)
      FP_StaticQaAddCheck(report, rows, "report_alignment", "POST_LADDER_REPORTS", "warn", true, "acceptance+ambiguity", "available", "final_reports_available_before_static_qa");

   FP_StaticQaFinalizeReport(qa_cfg, rows, report);
   return report.ok;
}

void FP_StaticQaApplyReportToResult(const FP_StaticQaReport &qa, FP_DetectResult &r)
{
   r.staticqa_attempted_total += (qa.attempted ? 1 : 0);
   r.staticqa_ok_total += (qa.ok ? 1 : 0);
   r.staticqa_checks_total += qa.checks_total;
   r.staticqa_pass_total += qa.checks_passed;
   r.staticqa_fail_total += qa.checks_failed;
   r.staticqa_warn_total += qa.checks_warned;
   r.staticqa_skipped_total += qa.checks_skipped;
   r.staticqa_file_errors_total += qa.file_errors;
   r.staticqa_compile_failures_total += qa.compile_contract_failures;
   r.staticqa_runtime_failures_total += qa.runtime_contract_failures;
   r.staticqa_print_failures_total += qa.print_safety_failures;
   r.staticqa_input_failures_total += qa.input_contract_failures;
   r.staticqa_dependency_failures_total += qa.dependency_failures;
   r.staticqa_io_failures_total += qa.io_contract_failures;
   r.staticqa_report_alignment_failures_total += qa.report_alignment_failures;
   r.staticqa_toolchain_failures_total += qa.toolchain_failures;
   r.staticqa_blockers_total += qa.blockers;
}

#endif // __FP_STATIC_QA_ENGINE_MQH__
