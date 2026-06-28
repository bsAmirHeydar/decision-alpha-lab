#ifndef __FP_RELEASE_AUDIT_MQH__
#define __FP_RELEASE_AUDIT_MQH__
#property strict

#include "FP_ReleaseRules.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 14 Release Audit
// ============================================================================

string FP_ReleaseCsvHeader()
{
   return "field,value";
}

string FP_ReleaseCsvRow(const string field, const string value)
{
   return FP_ExportCsvCell(field) + "," + FP_ExportCsvCell(value);
}

void FP_PrintReleaseReport(const string prefix, const FP_ReleaseReport &r)
{
   string msg = prefix;
   msg += " status=" + (r.ok ? "ok" : "failed");
   msg += " profile=" + r.profile_name;
   msg += " run_tag=" + r.run_tag;
   msg += " gate=" + (r.gate_passed ? "pass" : "fail");
   msg += " blocking=" + FP_BoolName(r.gate_blocking);
   msg += " overrides=" + IntegerToString(r.overrides_applied);
   msg += " cleanup=" + IntegerToString(r.cleanup_requested);
   msg += " export_forced=" + IntegerToString(r.export_forced);
   msg += " render_suppressed=" + IntegerToString(r.render_suppressed);
   msg += " validation_forced=" + IntegerToString(r.validation_forced);
   msg += " rollback_safe=" + IntegerToString(r.rollback_safe_mode);
   msg += " checks=" + IntegerToString(r.release_checks_total);
   msg += " pass=" + IntegerToString(r.release_checks_passed);
   msg += " fail=" + IntegerToString(r.release_checks_failed);
   msg += " events=" + IntegerToString(r.actual_events);
   msg += " visible=" + IntegerToString(r.actual_visible_events);
   msg += " hidden=" + IntegerToString(r.actual_hidden_events);
   msg += " hooks=" + IntegerToString(r.actual_hooks);
   msg += " render_errors=" + IntegerToString(r.actual_render_errors);
   msg += " export_errors=" + IntegerToString(r.actual_export_errors);
   msg += " validation_failures=" + IntegerToString(r.actual_validation_failures);
   msg += " canonical_failures=" + IntegerToString(r.actual_canonical_failures);
   msg += " manifest=" + r.manifest_file;
   msg += " files=" + IntegerToString(r.files_written);
   msg += " file_errors=" + IntegerToString(r.file_errors);
   msg += " reason=" + r.reason;
   Print(msg);
}

void FP_PrintReleaseSamples(const string prefix, const FP_ReleaseReport &r)
{
   Print(prefix,
         "_SAMPLE profile=", r.profile_name,
         " overrides=", r.override_log,
         " manifest=", r.manifest_file,
         " reason=", r.reason);
}

#endif // __FP_RELEASE_AUDIT_MQH__
