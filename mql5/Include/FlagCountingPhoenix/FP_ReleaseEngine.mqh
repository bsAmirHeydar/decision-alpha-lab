#ifndef __FP_RELEASE_ENGINE_MQH__
#define __FP_RELEASE_ENGINE_MQH__
#property strict

#include "FP_ReleaseAudit.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 14 Release Engine
// ----------------------------------------------------------------------------
// Runtime profile, release gate, rollback/debug manifest, and summary counters.
// ============================================================================

bool FP_ReleaseEnsureFolder(const string folder)
{
   if(folder == "") return true;
   return FolderCreate(folder);
}

string FP_ReleaseJoinPath(const string folder, const string file_name)
{
   if(folder == "") return file_name;
   return folder + "\\" + file_name;
}

string FP_ReleaseFileName(const FP_ReleaseConfig &cfg)
{
   if(cfg.overwrite_latest) return "latest_release.csv";
   string tag = cfg.run_tag;
   if(tag == "") tag = FP_ReleaseProfileName(cfg.profile) + "_" + TimeToString(TimeCurrent(), TIME_DATE|TIME_MINUTES|TIME_SECONDS);
   StringReplace(tag, ":", "-");
   StringReplace(tag, " ", "_");
   StringReplace(tag, ".", "_");
   return tag + "_release.csv";
}

bool FP_WriteReleaseManifest(const FP_ReleaseConfig &cfg, FP_ReleaseReport &r)
{
   if(!cfg.write_manifest) return true;
   FP_ReleaseEnsureFolder(cfg.folder);
   string path = FP_ReleaseJoinPath(cfg.folder, FP_ReleaseFileName(cfg));
   int handle = FileOpen(path, FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
   {
      r.file_errors++;
      if(r.reason == "ok") r.reason = "release_manifest_open_failed";
      else r.reason += ";release_manifest_open_failed";
      return false;
   }

   FileWriteString(handle, FP_ReleaseCsvHeader() + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("profile", r.profile_name) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("run_tag", r.run_tag) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("gate_passed", FP_BoolName(r.gate_passed)) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("gate_blocking", FP_BoolName(r.gate_blocking)) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("overrides_applied", IntegerToString(r.overrides_applied)) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("cleanup_requested", IntegerToString(r.cleanup_requested)) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("export_forced", IntegerToString(r.export_forced)) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("render_suppressed", IntegerToString(r.render_suppressed)) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("validation_forced", IntegerToString(r.validation_forced)) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("rollback_safe_mode", IntegerToString(r.rollback_safe_mode)) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("release_checks_total", IntegerToString(r.release_checks_total)) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("release_checks_passed", IntegerToString(r.release_checks_passed)) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("release_checks_failed", IntegerToString(r.release_checks_failed)) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("events", IntegerToString(r.actual_events)) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("visible_events", IntegerToString(r.actual_visible_events)) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("hidden_events", IntegerToString(r.actual_hidden_events)) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("hooks", IntegerToString(r.actual_hooks)) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("render_errors", IntegerToString(r.actual_render_errors)) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("export_errors", IntegerToString(r.actual_export_errors)) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("validation_failures", IntegerToString(r.actual_validation_failures)) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("canonical_failures", IntegerToString(r.actual_canonical_failures)) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("override_log", r.override_log) + "\r\n");
   FileWriteString(handle, FP_ReleaseCsvRow("reason", r.reason) + "\r\n");
   FileClose(handle);
   r.manifest_file = path;
   r.files_written++;
   return true;
}

void FP_ReleaseApplyReportToResult(const FP_ReleaseReport &rr, FP_DetectResult &r)
{
   r.release_attempted_total += (rr.attempted ? 1 : 0);
   r.release_ok_total += (rr.ok ? 1 : 0);
   r.release_gate_pass_total += (rr.gate_passed ? 1 : 0);
   r.release_gate_fail_total += (rr.gate_passed ? 0 : 1);
   r.release_overrides_total += rr.overrides_applied;
   r.release_files_written_total += rr.files_written;
   r.release_file_errors_total += rr.file_errors;
   r.release_cleanup_requested_total += rr.cleanup_requested;
   r.release_export_forced_total += rr.export_forced;
   r.release_render_suppressed_total += rr.render_suppressed;
   r.release_validation_forced_total += rr.validation_forced;
   r.release_rollback_safe_total += rr.rollback_safe_mode;
}

void FP_FinalizeReleaseWithManifest(const FP_ReleaseConfig &cfg,
                                    const FP_DetectResult &result,
                                    const FP_ExportReport &export_report,
                                    const FP_RenderReport &render_report,
                                    const FP_ValidationReport &validation_report,
                                    FP_ReleaseReport &release_report)
{
   FP_ReleaseFinalizeReport(cfg, result, export_report, render_report, validation_report, release_report);
   if(cfg.write_manifest)
      FP_WriteReleaseManifest(cfg, release_report);
}

#endif // __FP_RELEASE_ENGINE_MQH__
