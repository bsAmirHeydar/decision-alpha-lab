#ifndef __FP_HOOK_PHASE10_TYPES_MQH__
#define __FP_HOOK_PHASE10_TYPES_MQH__
#property strict

#include "FP_HookPhase09Engine.mqh"

// ============================================================================
// FlagCounting Phoenix - NDS Hook Phase 10 Types
// ----------------------------------------------------------------------------
// Scope:
// - freeze Hook v1 runtime contract after audit and visual smoke tests
// - define the training/export contract that later AI layers may consume
// - emit explicit freeze, contract-check, training-schema, and manifest CSVs
// - no execution, no broker request, no risk sizing, no volume sizing
// ============================================================================

#define FP_HOOK_P10_VERSION "HOOK-P10-freeze-training-contract"
#define FP_HOOK_P10_SCHEMA_VERSION "hook_phase10_freeze_contract_v1"
#define FP_HOOK_P10_DEFAULT_FOLDER "FlagCountingPhoenix"
#define FP_HOOK_P10_DEFAULT_PREFIX "DAL_HOOK_P10_"

// Contract mode is intentionally separate from the display-family input.
// Display-family answers what is drawn. Contract mode answers how strict the
// freeze gate is before using Hook output as a training-ready object stream.
enum FP_HookPhase10FreezeMode
{
   FP_HOOK_P10_FREEZE_OBSERVE_ONLY       = 0,
   FP_HOOK_P10_FREEZE_V1_CANDIDATE       = 1,
   FP_HOOK_P10_FREEZE_TRAINING_READY     = 2,
   FP_HOOK_P10_FREEZE_STRICT_LOCK        = 3
};

enum FP_HookPhase10Severity
{
   FP_HOOK_P10_SEVERITY_INFO    = 0,
   FP_HOOK_P10_SEVERITY_WARNING = 1,
   FP_HOOK_P10_SEVERITY_BLOCKER = 2
};

enum FP_HookPhase10ContractState
{
   FP_HOOK_P10_CONTRACT_UNKNOWN = 0,
   FP_HOOK_P10_CONTRACT_SKIPPED = 1,
   FP_HOOK_P10_CONTRACT_PASSED  = 2,
   FP_HOOK_P10_CONTRACT_FAILED  = 3
};

struct FP_HookPhase10Config
{
   bool enabled;
   FP_NDSHookDisplayFamily display_family;
   FP_HookPhase10FreezeMode freeze_mode;

   bool allow_rally_only_freeze;
   bool require_phase08_ok;
   bool require_phase09_ok;
   bool require_hook_records;
   bool require_xy_quality_records;
   bool require_high_quality_records;
   bool require_view_profile_not_keep_inputs;
   bool require_export_contract;
   bool require_no_file_errors;

   bool export_csv;
   bool export_contract_checks_csv;
   bool export_training_schema_csv;
   bool export_freeze_manifest_csv;
   bool print_summary;
   bool print_samples;

   int min_p06_records_total;
   int min_xy_closed_records;
   int min_high_or_elite_records;
   int max_warnings_allowed;
   int sample_limit;

   string folder;
   string object_prefix;
};

struct FP_HookPhase10ContractRow
{
   string contract_code;
   FP_HookPhase10Severity severity;
   bool required;
   FP_HookPhase10ContractState state;
   bool passed;
   string evidence;
   string recommendation;
};

struct FP_HookPhase10TrainingSchemaRow
{
   string column_name;
   string source_phase;
   bool required;
   string semantic_type;
   string description;
};

struct FP_HookPhase10Report
{
   bool attempted;
   bool ok;
   bool freeze_ready;
   string status;
   string reason;
   string contract_id;

   FP_NDSHookDisplayFamily display_family;
   FP_HookPhase07ViewProfile view_profile;
   FP_HookPhase10FreezeMode freeze_mode;

   int contract_checks_total;
   int contract_checks_required;
   int contract_checks_passed;
   int contract_checks_failed;
   int contract_checks_skipped;

   int info_count;
   int warning_count;
   int blocker_count;
   int failed_required_count;

   bool phase08_ok;
   string phase08_status;
   string phase08_reason;
   bool phase09_ok;
   string phase09_status;
   string phase09_reason;

   int p06_records_total;
   int p06_xy_closed_count;
   int p06_elite_count;
   int p06_high_count;
   int p06_medium_count;
   int p06_low_count;
   int p06_invalid_count;
   int p06_high_or_elite_count;

   int training_schema_columns;
   int files_written;
   int file_errors;
};

string FP_HookP10BoolName(const bool v)
{
   return (v ? "true" : "false");
}

string FP_HookP10FreezeModeName(const FP_HookPhase10FreezeMode m)
{
   if(m == FP_HOOK_P10_FREEZE_OBSERVE_ONLY) return "OBSERVE_ONLY";
   if(m == FP_HOOK_P10_FREEZE_V1_CANDIDATE) return "V1_CANDIDATE";
   if(m == FP_HOOK_P10_FREEZE_TRAINING_READY) return "TRAINING_READY";
   if(m == FP_HOOK_P10_FREEZE_STRICT_LOCK) return "STRICT_LOCK";
   return "UNKNOWN_FREEZE_MODE";
}

string FP_HookP10SeverityName(const FP_HookPhase10Severity s)
{
   if(s == FP_HOOK_P10_SEVERITY_INFO) return "INFO";
   if(s == FP_HOOK_P10_SEVERITY_WARNING) return "WARNING";
   if(s == FP_HOOK_P10_SEVERITY_BLOCKER) return "BLOCKER";
   return "UNKNOWN_SEVERITY";
}

string FP_HookP10ContractStateName(const FP_HookPhase10ContractState s)
{
   if(s == FP_HOOK_P10_CONTRACT_UNKNOWN) return "UNKNOWN";
   if(s == FP_HOOK_P10_CONTRACT_SKIPPED) return "SKIPPED";
   if(s == FP_HOOK_P10_CONTRACT_PASSED) return "PASSED";
   if(s == FP_HOOK_P10_CONTRACT_FAILED) return "FAILED";
   return "UNKNOWN_CONTRACT_STATE";
}

void FP_ResetHookPhase10Config(FP_HookPhase10Config &cfg)
{
   cfg.enabled = true;
   cfg.display_family = FP_NDS_HOOK_DISPLAY_RALLY_ONLY;
   cfg.freeze_mode = FP_HOOK_P10_FREEZE_V1_CANDIDATE;

   cfg.allow_rally_only_freeze = false;
   cfg.require_phase08_ok = true;
   cfg.require_phase09_ok = true;
   cfg.require_hook_records = true;
   cfg.require_xy_quality_records = true;
   cfg.require_high_quality_records = false;
   cfg.require_view_profile_not_keep_inputs = false;
   cfg.require_export_contract = false;
   cfg.require_no_file_errors = true;

   cfg.export_csv = false;
   cfg.export_contract_checks_csv = true;
   cfg.export_training_schema_csv = true;
   cfg.export_freeze_manifest_csv = true;
   cfg.print_summary = false;
   cfg.print_samples = false;

   cfg.min_p06_records_total = 1;
   cfg.min_xy_closed_records = 0;
   cfg.min_high_or_elite_records = 0;
   cfg.max_warnings_allowed = 0;
   cfg.sample_limit = 20;

   cfg.folder = FP_HOOK_P10_DEFAULT_FOLDER;
   cfg.object_prefix = FP_HOOK_P10_DEFAULT_PREFIX;
}

void FP_ResetHookPhase10Report(FP_HookPhase10Report &r)
{
   r.attempted = false;
   r.ok = false;
   r.freeze_ready = false;
   r.status = "HOOK_P10_RESET";
   r.reason = "RESET";
   r.contract_id = "";

   r.display_family = FP_NDS_HOOK_DISPLAY_RALLY_ONLY;
   r.view_profile = FP_HOOK_P07_VIEW_KEEP_INPUTS;
   r.freeze_mode = FP_HOOK_P10_FREEZE_V1_CANDIDATE;

   r.contract_checks_total = 0;
   r.contract_checks_required = 0;
   r.contract_checks_passed = 0;
   r.contract_checks_failed = 0;
   r.contract_checks_skipped = 0;

   r.info_count = 0;
   r.warning_count = 0;
   r.blocker_count = 0;
   r.failed_required_count = 0;

   r.phase08_ok = false;
   r.phase08_status = "";
   r.phase08_reason = "";
   r.phase09_ok = false;
   r.phase09_status = "";
   r.phase09_reason = "";

   r.p06_records_total = 0;
   r.p06_xy_closed_count = 0;
   r.p06_elite_count = 0;
   r.p06_high_count = 0;
   r.p06_medium_count = 0;
   r.p06_low_count = 0;
   r.p06_invalid_count = 0;
   r.p06_high_or_elite_count = 0;

   r.training_schema_columns = 0;
   r.files_written = 0;
   r.file_errors = 0;
}

#endif // __FP_HOOK_PHASE10_TYPES_MQH__
