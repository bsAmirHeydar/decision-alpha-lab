#ifndef __FP_STATIC_QA_TYPES_MQH__
#define __FP_STATIC_QA_TYPES_MQH__
#property strict

#include "FP_AmbiguityTypes.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 18 Static QA / Compile Hardening Types
// ----------------------------------------------------------------------------
// Level 18 is the post-ladder compile/static QA guard. It is read-only and runs
// after Level 17. Runtime checks are paired with the repository-side Python
// scanner in contexts/legacy/tools/flag_counting/static_qa.py.
// ============================================================================

#define FP_STATIC_QA_CONTRACT_VERSION "18.00"
#define FP_STATIC_QA_EXPECTED_ID_PASS "phoenix_level18"
#define FP_STATIC_QA_MODULE_COUNT     18
#define FP_STATIC_QA_CHECK_FAMILIES   8

enum FP_StaticQaMode
{
   FP_STATIC_QA_MODE_OBSERVE    = 0,
   FP_STATIC_QA_MODE_BASELINE   = 1,
   FP_STATIC_QA_MODE_REGRESSION = 2,
   FP_STATIC_QA_MODE_RELEASE    = 3
};

struct FP_StaticQaConfig
{
   bool   enabled;
   int    mode;
   bool   strict;
   bool   write_csv;
   bool   overwrite_latest;
   string folder;
   string run_tag;
   string case_id;
   string contract_version;

   bool   require_contract_version;
   bool   require_identity_pass;
   bool   require_interface_contract_alignment;
   bool   require_runtime_partitions;
   bool   require_nonnegative_counters;
   bool   require_report_alignment;
   bool   require_io_alignment;
   bool   require_release_safe_defaults;
   bool   require_static_tool_present;
   bool   require_zero_runtime_blockers;

   bool   allow_observe_warnings;
   bool   allow_disabled_export;
   bool   allow_disabled_validation;
   bool   allow_disabled_render;

   bool   print_sanity;
   bool   print_samples;
   int    sample_limit;
};

struct FP_StaticQaReport
{
   bool   attempted;
   bool   ok;
   string mode_name;
   string run_id;
   string case_id;
   string folder;
   string report_file;
   string reason;

   int checks_total;
   int checks_passed;
   int checks_failed;
   int checks_warned;
   int checks_skipped;
   int file_errors;
   int files_written;

   int compile_contract_checks;
   int compile_contract_failures;
   int runtime_contract_checks;
   int runtime_contract_failures;
   int print_safety_checks;
   int print_safety_failures;
   int input_contract_checks;
   int input_contract_failures;
   int dependency_checks;
   int dependency_failures;
   int io_contract_checks;
   int io_contract_failures;
   int report_alignment_checks;
   int report_alignment_failures;
   int toolchain_checks;
   int toolchain_failures;
   int blockers;
};

string FP_StaticQaModeName(const int mode)
{
   if(mode == FP_STATIC_QA_MODE_BASELINE)   return "baseline";
   if(mode == FP_STATIC_QA_MODE_REGRESSION) return "regression";
   if(mode == FP_STATIC_QA_MODE_RELEASE)    return "release";
   return "observe";
}

void FP_DefaultStaticQaConfig(FP_StaticQaConfig &cfg)
{
   cfg.enabled = true;
   cfg.mode = FP_STATIC_QA_MODE_OBSERVE;
   cfg.strict = false;
   cfg.write_csv = false;
   cfg.overwrite_latest = true;
   cfg.folder = "FlagCountingPhoenix";
   cfg.run_tag = "";
   cfg.case_id = "manual";
   cfg.contract_version = FP_STATIC_QA_CONTRACT_VERSION;

   cfg.require_contract_version = true;
   cfg.require_identity_pass = true;
   cfg.require_interface_contract_alignment = true;
   cfg.require_runtime_partitions = true;
   cfg.require_nonnegative_counters = true;
   cfg.require_report_alignment = true;
   cfg.require_io_alignment = true;
   cfg.require_release_safe_defaults = true;
   cfg.require_static_tool_present = true;
   cfg.require_zero_runtime_blockers = false;

   cfg.allow_observe_warnings = true;
   cfg.allow_disabled_export = true;
   cfg.allow_disabled_validation = true;
   cfg.allow_disabled_render = false;

   cfg.print_sanity = true;
   cfg.print_samples = false;
   cfg.sample_limit = 8;
}

void FP_ResetStaticQaReport(FP_StaticQaReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.mode_name = "";
   r.run_id = "";
   r.case_id = "";
   r.folder = "";
   r.report_file = "";
   r.reason = "";
   r.checks_total = 0;
   r.checks_passed = 0;
   r.checks_failed = 0;
   r.checks_warned = 0;
   r.checks_skipped = 0;
   r.file_errors = 0;
   r.files_written = 0;
   r.compile_contract_checks = 0;
   r.compile_contract_failures = 0;
   r.runtime_contract_checks = 0;
   r.runtime_contract_failures = 0;
   r.print_safety_checks = 0;
   r.print_safety_failures = 0;
   r.input_contract_checks = 0;
   r.input_contract_failures = 0;
   r.dependency_checks = 0;
   r.dependency_failures = 0;
   r.io_contract_checks = 0;
   r.io_contract_failures = 0;
   r.report_alignment_checks = 0;
   r.report_alignment_failures = 0;
   r.toolchain_checks = 0;
   r.toolchain_failures = 0;
   r.blockers = 0;
}

string FP_StaticQaBool(const bool v)
{
   return (v ? "true" : "false");
}

string FP_StaticQaInt(const int v)
{
   return IntegerToString(v);
}

#endif // __FP_STATIC_QA_TYPES_MQH__
