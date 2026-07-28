#ifndef __FP_AMBIGUITY_ENGINE_MQH__
#define __FP_AMBIGUITY_ENGINE_MQH__
#property strict

#include "FP_ExportEngine.mqh"
#include "FP_AmbiguityAudit.mqh"
#include <AlphaLab/UC04/AL_UC04CorePrimitives.mqh>

// ============================================================================
// Phoenix Level 17 - Ambiguity / Decision-Lock Engine
// ============================================================================

bool FP_AmbiguityWriteLine(const int handle, const string line)
{
   return AL_UC04WriteLine(handle, line);
}

bool FP_AmbiguityWriteCsv(const FP_AmbiguityConfig &cfg,
                          const string &rows[],
                          FP_AmbiguityReport &report)
{
   if(!cfg.write_csv) return true;
   FP_ExportEnsureFolder(cfg.folder);
   string path = cfg.folder + "/" + FP_AmbiguityFileName(cfg);
   int handle = FileOpen(path, FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      report.file_errors++;
      report.reason = report.reason + ";ambiguity_open_failed_" + path;
      return false;
   }
   FP_AmbiguityWriteLine(handle, FP_AmbiguityHeader());
   for(int i=0; i<ArraySize(rows); i++)
      FP_AmbiguityWriteLine(handle, rows[i]);
   FileClose(handle);
   report.report_file = path;
   report.files_written++;
   return true;
}

void FP_AmbiguityFinalizeReport(const FP_AmbiguityConfig &cfg,
                                const string &rows[],
                                FP_AmbiguityReport &report)
{
   report.ok = (report.checks_failed == 0 && report.file_errors == 0);
   if(report.reason == "") report.reason = (report.ok ? "ok" : "ambiguity_decision_lock_failed");
   FP_AmbiguityWriteCsv(cfg, rows, report);
   report.ok = (report.checks_failed == 0 && report.file_errors == 0);
   if(!report.ok && report.reason == "ok") report.reason = "ambiguity_decision_lock_failed";
}

bool FP_RunAmbiguityWithReport(const string symbol,
                               const ENUM_TIMEFRAMES period,
                               const FP_AmbiguityConfig &amb_cfg,
                               const FP_TimebaseConfig &timebase_cfg,
                               const FP_Config &engine_cfg,
                               const FP_ExportConfig &export_cfg,
                               const FP_RenderConfig &render_cfg,
                               const FP_ValidationConfig &validation_cfg,
                               const FP_ReleaseConfig &release_cfg,
                               const FP_InterfaceConfig &interface_cfg,
                               const FP_AcceptanceConfig &acceptance_cfg,
                               const FP_DetectResult &result,
                               const FP_ExportReport &export_report,
                               const FP_RenderReport &render_report,
                               const FP_ValidationReport &validation_report,
                               const FP_ReleaseReport &release_report,
                               const FP_InterfaceReport &interface_pre_report,
                               const FP_InterfaceReport &interface_post_report,
                               const FP_AcceptanceReport &acceptance_report,
                               FP_AmbiguityReport &report,
                               string &rows[])
{
   FP_ResetAmbiguityReport(report);
   ArrayResize(rows, 0);
   report.attempted = amb_cfg.enabled;
   report.mode_name = FP_AmbiguityModeName(amb_cfg.mode);
   report.case_id = amb_cfg.case_id;
   report.folder = amb_cfg.folder;
   report.canon_source = amb_cfg.canon_source;
   report.run_id = FP_AmbiguityRunId(symbol, period, amb_cfg);
   if(!amb_cfg.enabled)
   {
      report.reason = "ambiguity_disabled";
      return false;
   }

   FP_AmbiguityAddSourceChecks(report, rows, amb_cfg, engine_cfg);
   FP_AmbiguityAddDefaultPolicyChecks(report, rows, amb_cfg, timebase_cfg, engine_cfg, render_cfg);
   FP_AmbiguityAddPipelineChecks(report, rows, amb_cfg, export_report, render_report, validation_report, release_report, interface_pre_report, interface_post_report, acceptance_report);
   FP_AmbiguityAddReleaseChecks(report, rows, amb_cfg, release_cfg, render_cfg, validation_report, acceptance_report, result);

   // Explicit dependency declarations. These are warnings because Level 17 is
   // allowed to audit both fully enabled and partially disabled operator modes.
   FP_AmbiguityAddDecision(report, rows, "X01_EXPORT_CONFIG_PRESENT", "runtime", "warn",
                           (!export_cfg.enabled || export_report.attempted || !amb_cfg.require_export_before_renderer),
                           "cfg=" + FP_AmbiguityBool(export_cfg.enabled) + "/report=" + FP_AmbiguityBool(export_report.attempted),
                           "if_enabled_then_attempted", "export_config_and_report_alignment");
   FP_AmbiguityAddDecision(report, rows, "X02_VALIDATION_CONFIG_PRESENT", "runtime", "warn",
                           (!validation_cfg.enabled || validation_report.attempted),
                           "cfg=" + FP_AmbiguityBool(validation_cfg.enabled) + "/report=" + FP_AmbiguityBool(validation_report.attempted),
                           "if_enabled_then_attempted", "validation_config_and_report_alignment");
   FP_AmbiguityAddDecision(report, rows, "X03_INTERFACE_CONFIG_PRESENT", "runtime", "warn",
                           ((!interface_cfg.preflight_enabled || interface_pre_report.attempted) && (!interface_cfg.postflight_enabled || interface_post_report.attempted)),
                           "pre_cfg=" + FP_AmbiguityBool(interface_cfg.preflight_enabled) + "/pre_report=" + FP_AmbiguityBool(interface_pre_report.attempted) +
                           "/post_cfg=" + FP_AmbiguityBool(interface_cfg.postflight_enabled) + "/post_report=" + FP_AmbiguityBool(interface_post_report.attempted),
                           "enabled_stages_attempted", "interface_config_and_report_alignment");
   FP_AmbiguityAddDecision(report, rows, "X04_ACCEPTANCE_CONFIG_PRESENT", "runtime", "warn",
                           (!acceptance_cfg.enabled || acceptance_report.attempted),
                           "cfg=" + FP_AmbiguityBool(acceptance_cfg.enabled) + "/report=" + FP_AmbiguityBool(acceptance_report.attempted),
                           "if_enabled_then_attempted", "acceptance_config_and_report_alignment");

   FP_AmbiguityFinalizeReport(amb_cfg, rows, report);
   return report.ok;
}

void FP_AmbiguityApplyReportToResult(const FP_AmbiguityReport &ar, FP_DetectResult &r)
{
   r.ambiguity_attempted_total += (ar.attempted ? 1 : 0);
   r.ambiguity_ok_total += (ar.ok ? 1 : 0);
   r.ambiguity_checks_total += ar.checks_total;
   r.ambiguity_pass_total += ar.checks_passed;
   r.ambiguity_fail_total += ar.checks_failed;
   r.ambiguity_warn_total += ar.checks_warned;
   r.ambiguity_skipped_total += ar.checks_skipped;
   r.ambiguity_file_errors_total += ar.file_errors;
   r.ambiguity_decisions_locked_total += ar.decisions_locked;
   r.ambiguity_decisions_unlocked_total += ar.decisions_unlocked;
   r.ambiguity_diagnostic_variants_total += ar.diagnostic_variants;
   r.ambiguity_release_blockers_total += ar.release_blockers;
   r.ambiguity_conflicts_total += (ar.source_conflicts + ar.profile_conflicts + ar.default_conflicts + ar.runtime_conflicts + ar.legacy_conflicts);
}

#endif // __FP_AMBIGUITY_ENGINE_MQH__
