#ifndef __FP_ACCEPTANCE_TYPES_MQH__
#define __FP_ACCEPTANCE_TYPES_MQH__
#property strict

#include "FP_InterfaceTypes.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 16 Acceptance Types
// ----------------------------------------------------------------------------
// Level 16 is the runtime implementation-order and acceptance-matrix layer. It
// is read-only. It aggregates the already-produced Level 01..15 reports into a
// single operator-facing runbook gate before FP_SUMMARY.
// ============================================================================

#define FP_ACCEPTANCE_CONTRACT_VERSION "16.00"
#define FP_ACCEPTANCE_MIN_LEVEL        1
#define FP_ACCEPTANCE_MAX_LEVEL        16
#define FP_ACCEPTANCE_GATE_COUNT       16

enum FP_AcceptanceMode
{
   FP_ACCEPTANCE_MODE_OBSERVE    = 0,
   FP_ACCEPTANCE_MODE_BASELINE   = 1,
   FP_ACCEPTANCE_MODE_REGRESSION = 2,
   FP_ACCEPTANCE_MODE_RELEASE    = 3
};

struct FP_AcceptanceConfig
{
   bool   enabled;
   int    mode;
   bool   strict;
   bool   write_csv;
   bool   overwrite_latest;
   string folder;
   string run_tag;
   string case_id;
   string matrix_version;

   bool   require_level01_ok;
   bool   require_no_canonical_failures;
   bool   require_export_ok_when_enabled;
   bool   require_render_ok_when_enabled;
   bool   require_validation_ok_when_enabled;
   bool   require_release_gate_when_strict;
   bool   require_interface_pre_ok_when_enabled;
   bool   require_interface_post_ok_when_enabled;
   bool   require_visible_partition;
   bool   require_locked_f3_if_expected;

   int    expected_min_visible_events;
   int    expected_min_f1;
   int    expected_min_f2;
   int    expected_min_f3;
   int    expected_min_locked_f3;

   bool   print_sanity;
   bool   print_samples;
   int    sample_limit;
};

struct FP_AcceptanceReport
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

   int levels_checked;
   int levels_passed;
   int levels_failed;
   int levels_warned;
   int hard_gates_total;
   int hard_gates_passed;
   int hard_gates_failed;
   int baseline_items;
   int regression_items;
   int release_items;

   int order_errors;
   int dependency_errors;
   int matrix_errors;
   int invariant_errors;
};

string FP_AcceptanceModeName(const int mode)
{
   if(mode == FP_ACCEPTANCE_MODE_BASELINE)   return "baseline";
   if(mode == FP_ACCEPTANCE_MODE_REGRESSION) return "regression";
   if(mode == FP_ACCEPTANCE_MODE_RELEASE)    return "release";
   return "observe";
}

void FP_DefaultAcceptanceConfig(FP_AcceptanceConfig &cfg)
{
   cfg.enabled = true;
   cfg.mode = FP_ACCEPTANCE_MODE_OBSERVE;
   cfg.strict = false;
   cfg.write_csv = false;
   cfg.overwrite_latest = true;
   cfg.folder = "FlagCountingPhoenix";
   cfg.run_tag = "";
   cfg.case_id = "manual";
   cfg.matrix_version = FP_ACCEPTANCE_CONTRACT_VERSION;

   cfg.require_level01_ok = true;
   cfg.require_no_canonical_failures = true;
   cfg.require_export_ok_when_enabled = true;
   cfg.require_render_ok_when_enabled = true;
   cfg.require_validation_ok_when_enabled = true;
   cfg.require_release_gate_when_strict = false;
   cfg.require_interface_pre_ok_when_enabled = false;
   cfg.require_interface_post_ok_when_enabled = false;
   cfg.require_visible_partition = true;
   cfg.require_locked_f3_if_expected = true;

   cfg.expected_min_visible_events = -1;
   cfg.expected_min_f1 = -1;
   cfg.expected_min_f2 = -1;
   cfg.expected_min_f3 = -1;
   cfg.expected_min_locked_f3 = -1;

   cfg.print_sanity = true;
   cfg.print_samples = false;
   cfg.sample_limit = 8;
}

void FP_ResetAcceptanceReport(FP_AcceptanceReport &r)
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
   r.levels_checked = 0;
   r.levels_passed = 0;
   r.levels_failed = 0;
   r.levels_warned = 0;
   r.hard_gates_total = 0;
   r.hard_gates_passed = 0;
   r.hard_gates_failed = 0;
   r.baseline_items = 0;
   r.regression_items = 0;
   r.release_items = 0;
   r.order_errors = 0;
   r.dependency_errors = 0;
   r.matrix_errors = 0;
   r.invariant_errors = 0;
}

string FP_AcceptanceBool(const bool v)
{
   return (v ? "true" : "false");
}

string FP_AcceptanceInt(const int v)
{
   return IntegerToString(v);
}

string FP_AcceptanceRunId(const string symbol,
                          const ENUM_TIMEFRAMES period,
                          const FP_AcceptanceConfig &cfg)
{
   string tag = cfg.run_tag;
   if(tag == "") tag = "latest";
   return symbol + "_" + EnumToString(period) + "_acceptance_" + tag;
}

string FP_AcceptanceFileName(const FP_AcceptanceConfig &cfg)
{
   if(cfg.overwrite_latest)
      return "latest_acceptance.csv";
   string tag = cfg.run_tag;
   if(tag == "") tag = TimeToString(TimeCurrent(), TIME_DATE|TIME_MINUTES|TIME_SECONDS);
   StringReplace(tag, ":", "");
   StringReplace(tag, ".", "_");
   StringReplace(tag, " ", "_");
   return "acceptance_" + tag + ".csv";
}

#endif // __FP_ACCEPTANCE_TYPES_MQH__
