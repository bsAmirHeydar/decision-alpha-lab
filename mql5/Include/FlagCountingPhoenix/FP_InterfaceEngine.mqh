#ifndef __FP_INTERFACE_ENGINE_MQH__
#define __FP_INTERFACE_ENGINE_MQH__
#property strict

#include "FP_InterfaceAudit.mqh"
#include <AlphaLab/UC04/AL_UC04CorePrimitives.mqh>

// ============================================================================
// Phoenix Level 15 - Interface Contract Engine
// ============================================================================

bool FP_InterfaceWriteLine(const int handle, const string line)
{
   return AL_UC04WriteLine(handle, line);
}

bool FP_InterfaceWriteCsv(const FP_InterfaceConfig &cfg,
                          const string stage,
                          const string &rows[],
                          FP_InterfaceReport &report)
{
   if(!cfg.write_csv) return true;
   FP_ExportEnsureFolder(cfg.folder);
   string path = cfg.folder + "/" + FP_InterfaceFileName(cfg, stage);
   int handle = FileOpen(path, FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = report.reason + ";interface_open_failed_" + path;
      return false;
   }
   FP_InterfaceWriteLine(handle, FP_InterfaceHeader());
   for(int i=0; i<ArraySize(rows); i++)
      FP_InterfaceWriteLine(handle, rows[i]);
   FileClose(handle);
   report.report_file = path;
   report.files_written++;
   return true;
}

void FP_InterfaceFinalizeReport(const FP_InterfaceConfig &cfg,
                                const string stage,
                                const string &rows[],
                                FP_InterfaceReport &report)
{
   if(cfg.strict)
      report.ok = (report.checks_failed == 0 && report.file_errors == 0);
   else
      report.ok = (report.file_errors == 0);

   if(report.reason == "") report.reason = (report.ok ? "ok" : "interface_contract_failed");
   FP_InterfaceWriteCsv(cfg, stage, rows, report);
   if(cfg.strict)
      report.ok = (report.checks_failed == 0 && report.file_errors == 0);
   else
      report.ok = (report.file_errors == 0);
   if(!report.ok && report.reason == "ok") report.reason = "interface_contract_failed";
}

bool FP_RunInterfacePreflightWithReport(const string symbol,
                                        const ENUM_TIMEFRAMES period,
                                        const FP_TimebaseConfig &timebase_cfg,
                                        const FP_Config &engine_cfg,
                                        const FP_ExportConfig &export_cfg,
                                        const FP_RenderConfig &render_cfg,
                                        const FP_ValidationConfig &validation_cfg,
                                        const FP_ReleaseConfig &release_cfg,
                                        const FP_InterfaceConfig &interface_cfg,
                                        FP_InterfaceReport &report,
                                        string &rows[])
{
   FP_ResetInterfaceReport(report);
   ArrayResize(rows, 0);
   report.stage = "pre";
   report.folder = interface_cfg.folder;
   report.run_id = FP_InterfaceRunId(symbol, period, report.stage, interface_cfg);
   report.attempted = interface_cfg.preflight_enabled;
   if(!interface_cfg.preflight_enabled)
   {
      report.reason = "preflight_disabled";
      return false;
   }

   FP_InterfaceAddEnumChecks(report, rows);
   FP_InterfaceAddFacadeChecks(report, rows, engine_cfg);
   FP_InterfaceAddConfigChecks(report, rows, timebase_cfg, engine_cfg, export_cfg, render_cfg, validation_cfg, release_cfg, interface_cfg);
   FP_InterfaceAddDependencyChecks(report, rows, export_cfg, render_cfg, validation_cfg, release_cfg);

   FP_InterfaceFinalizeReport(interface_cfg, report.stage, rows, report);
   return report.ok;
}

bool FP_RunInterfacePostflightWithReport(const string symbol,
                                         const ENUM_TIMEFRAMES period,
                                         const FP_InterfaceConfig &interface_cfg,
                                         const FP_FlagEvent &events[],
                                         const FP_HookBranch &hooks[],
                                         const FP_DetectResult &result,
                                         FP_InterfaceReport &report,
                                         string &rows[])
{
   FP_ResetInterfaceReport(report);
   ArrayResize(rows, 0);
   report.stage = "post";
   report.folder = interface_cfg.folder;
   report.run_id = FP_InterfaceRunId(symbol, period, report.stage, interface_cfg);
   report.attempted = interface_cfg.postflight_enabled;
   if(!interface_cfg.postflight_enabled)
   {
      report.reason = "postflight_disabled";
      return false;
   }

   FP_InterfaceAddResultChecks(report, rows, interface_cfg, events, hooks, result);
   FP_InterfaceAddCounterChecks(report, rows, interface_cfg, result);

   FP_InterfaceFinalizeReport(interface_cfg, report.stage, rows, report);
   return report.ok;
}

void FP_InterfaceApplyReportToResult(const FP_InterfaceReport &ir, FP_DetectResult &r)
{
   r.interface_attempted_total += (ir.attempted ? 1 : 0);
   r.interface_ok_total += (ir.ok ? 1 : 0);
   r.interface_checks_total += ir.checks_total;
   r.interface_pass_total += ir.checks_passed;
   r.interface_fail_total += ir.checks_failed;
   r.interface_warn_total += ir.checks_warned;
   r.interface_skipped_total += ir.checks_skipped;
   r.interface_file_errors_total += ir.file_errors;
   r.interface_missing_ids_total += ir.missing_public_ids;
   r.interface_parent_errors_total += ir.visible_child_parent_errors;
   r.interface_negative_counter_errors_total += ir.negative_counter_errors;
   r.interface_partition_errors_total += ir.partition_errors;
}

#endif // __FP_INTERFACE_ENGINE_MQH__
