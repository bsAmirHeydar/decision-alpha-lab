#ifndef __FP_HOOK_PHASE08_TYPES_MQH__
#define __FP_HOOK_PHASE08_TYPES_MQH__
#property strict

#include "FP_HookPhase07Engine.mqh"

// ============================================================================
// FlagCounting Phoenix - NDS Hook Phase 08 Types
// ----------------------------------------------------------------------------
// Scope:
// - audit reconciliation for Hook Phase 01..Phase 07
// - config/runtime/export consistency checks
// - phase-matrix and integrity CSV outputs
// - preparation for visual smoke test and Hook v1 freeze
// - no execution, no broker request, no risk sizing, no volume sizing
// ============================================================================

#define FP_HOOK_P08_VERSION "HOOK-P08-audit-csv-reconciliation"
#define FP_HOOK_P08_SCHEMA_VERSION "hook_phase08_audit_v1"
#define FP_HOOK_P08_DEFAULT_FOLDER "FlagCountingPhoenix"
#define FP_HOOK_P08_DEFAULT_PREFIX "DAL_HOOK_P08_"

enum FP_HookPhase08Severity
{
   FP_HOOK_P08_SEVERITY_INFO    = 0,
   FP_HOOK_P08_SEVERITY_WARNING = 1,
   FP_HOOK_P08_SEVERITY_BLOCKER = 2
};

struct FP_HookPhase08Config
{
   bool enabled;
   FP_NDSHookDisplayFamily display_family;

   bool allow_rally_only_audit;
   bool export_csv;
   bool export_phase_matrix_csv;
   bool export_integrity_csv;
   bool print_summary;
   bool print_samples;

   bool require_runtime_report_ok;
   bool require_phase_chain_alignment;
   bool require_unique_object_prefixes;
   bool require_nonnegative_counts;
   bool require_audit_export_profile_alignment;
   bool require_no_file_errors;
   bool require_p06_records_for_quality_audit;

   int max_warnings_allowed;
   int sample_limit;

   string folder;
   string object_prefix;
};

struct FP_HookPhase08Finding
{
   string check_code;
   FP_HookPhase08Severity severity;
   bool passed;
   string phase;
   string evidence;
   string recommendation;
};

struct FP_HookPhase08PhaseRow
{
   string phase;
   bool cfg_enabled;
   bool attempted;
   bool ok;
   string status;
   string reason;
   bool export_enabled;
   int files_written;
   int file_errors;
   int records_seen;
   int positive_seen;
   int negative_seen;
   int objects_created;
   int objects_deleted;
   int drawn_seen;
};

struct FP_HookPhase08Report
{
   bool attempted;
   bool ok;
   string status;
   string reason;

   FP_NDSHookDisplayFamily display_family;
   FP_HookPhase07ViewProfile view_profile;

   int phases_total;
   int phases_enabled;
   int phases_attempted;
   int phases_ok;
   int phases_failed;

   int findings_total;
   int info_count;
   int warning_count;
   int blocker_count;
   int passed_count;
   int failed_count;

   int chain_checks;
   int chain_passed;
   int chain_failed;
   int prefix_checks;
   int prefix_failed;
   int runtime_checks;
   int runtime_failed;
   int export_checks;
   int export_failed;

   int p06_records_total;
   int p06_xy_closed_count;
   int p06_elite_count;
   int p06_high_count;
   int p06_medium_count;
   int p06_low_count;
   int p06_invalid_count;

   int files_written;
   int file_errors;
};

string FP_HookP08BoolName(const bool v)
{
   return (v ? "true" : "false");
}

string FP_HookP08SeverityName(const FP_HookPhase08Severity s)
{
   if(s == FP_HOOK_P08_SEVERITY_INFO) return "INFO";
   if(s == FP_HOOK_P08_SEVERITY_WARNING) return "WARNING";
   if(s == FP_HOOK_P08_SEVERITY_BLOCKER) return "BLOCKER";
   return "UNKNOWN_SEVERITY";
}

void FP_ResetHookPhase08Config(FP_HookPhase08Config &cfg)
{
   cfg.enabled = true;
   cfg.display_family = FP_NDS_HOOK_DISPLAY_RALLY_ONLY;

   cfg.allow_rally_only_audit = false;
   cfg.export_csv = false;
   cfg.export_phase_matrix_csv = true;
   cfg.export_integrity_csv = true;
   cfg.print_summary = false;
   cfg.print_samples = false;

   cfg.require_runtime_report_ok = true;
   cfg.require_phase_chain_alignment = true;
   cfg.require_unique_object_prefixes = true;
   cfg.require_nonnegative_counts = true;
   cfg.require_audit_export_profile_alignment = true;
   cfg.require_no_file_errors = true;
   cfg.require_p06_records_for_quality_audit = false;

   cfg.max_warnings_allowed = 0;
   cfg.sample_limit = 20;

   cfg.folder = FP_HOOK_P08_DEFAULT_FOLDER;
   cfg.object_prefix = FP_HOOK_P08_DEFAULT_PREFIX;
}

void FP_ResetHookPhase08Report(FP_HookPhase08Report &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "HOOK_P08_RESET";
   r.reason = "RESET";

   r.display_family = FP_NDS_HOOK_DISPLAY_RALLY_ONLY;
   r.view_profile = FP_HOOK_P07_VIEW_KEEP_INPUTS;

   r.phases_total = 0;
   r.phases_enabled = 0;
   r.phases_attempted = 0;
   r.phases_ok = 0;
   r.phases_failed = 0;

   r.findings_total = 0;
   r.info_count = 0;
   r.warning_count = 0;
   r.blocker_count = 0;
   r.passed_count = 0;
   r.failed_count = 0;

   r.chain_checks = 0;
   r.chain_passed = 0;
   r.chain_failed = 0;
   r.prefix_checks = 0;
   r.prefix_failed = 0;
   r.runtime_checks = 0;
   r.runtime_failed = 0;
   r.export_checks = 0;
   r.export_failed = 0;

   r.p06_records_total = 0;
   r.p06_xy_closed_count = 0;
   r.p06_elite_count = 0;
   r.p06_high_count = 0;
   r.p06_medium_count = 0;
   r.p06_low_count = 0;
   r.p06_invalid_count = 0;

   r.files_written = 0;
   r.file_errors = 0;
}

#endif // __FP_HOOK_PHASE08_TYPES_MQH__
