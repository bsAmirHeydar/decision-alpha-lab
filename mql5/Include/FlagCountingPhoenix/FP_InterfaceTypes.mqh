#ifndef __FP_INTERFACE_TYPES_MQH__
#define __FP_INTERFACE_TYPES_MQH__
#property strict

#include "FP_ReleaseTypes.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 15 Interface Types
// ----------------------------------------------------------------------------
// Level 15 freezes module boundaries after the runtime layers exist.  It is a
// read-only contract harness: it validates public facade assumptions, config
// bounds, stable enum values, result partitions, and dependency-facing counters.
// It never mutates events, hooks, renderer objects, identities, or lifecycle
// state.
// ============================================================================

#define FP_INTERFACE_CONTRACT_VERSION "15.00"
#define FP_INTERFACE_MIN_LEVEL        1
#define FP_INTERFACE_MAX_LEVEL        15
#define FP_INTERFACE_PUBLIC_FACADE_COUNT 15

struct FP_InterfaceConfig
{
   bool   preflight_enabled;
   bool   postflight_enabled;
   bool   strict;
   bool   write_csv;
   bool   overwrite_latest;
   string folder;
   string run_tag;
   bool   require_preflight_ok;
   bool   require_postflight_ok;
   bool   require_result_partition;
   bool   require_public_ids;
   bool   require_parent_contract;
   bool   require_counter_nonnegative;
   bool   print_sanity;
   bool   print_samples;
   int    sample_limit;
};

struct FP_InterfaceReport
{
   bool   attempted;
   bool   ok;
   string stage;
   string run_id;
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

   int facade_checks;
   int config_checks;
   int enum_checks;
   int dependency_checks;
   int result_checks;
   int parent_checks;
   int id_checks;

   int missing_public_ids;
   int visible_child_parent_errors;
   int negative_counter_errors;
   int partition_errors;
   int dependency_errors;
};

void FP_DefaultInterfaceConfig(FP_InterfaceConfig &cfg)
{
   cfg.preflight_enabled = true;
   cfg.postflight_enabled = true;
   cfg.strict = false;
   cfg.write_csv = false;
   cfg.overwrite_latest = true;
   cfg.folder = "FlagCountingPhoenix";
   cfg.run_tag = "";
   cfg.require_preflight_ok = false;
   cfg.require_postflight_ok = false;
   cfg.require_result_partition = true;
   cfg.require_public_ids = true;
   cfg.require_parent_contract = true;
   cfg.require_counter_nonnegative = true;
   cfg.print_sanity = true;
   cfg.print_samples = false;
   cfg.sample_limit = 8;
}

void FP_ResetInterfaceReport(FP_InterfaceReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.stage = "";
   r.run_id = "";
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
   r.facade_checks = 0;
   r.config_checks = 0;
   r.enum_checks = 0;
   r.dependency_checks = 0;
   r.result_checks = 0;
   r.parent_checks = 0;
   r.id_checks = 0;
   r.missing_public_ids = 0;
   r.visible_child_parent_errors = 0;
   r.negative_counter_errors = 0;
   r.partition_errors = 0;
   r.dependency_errors = 0;
}

string FP_InterfaceBool(const bool v)
{
   return (v ? "true" : "false");
}

string FP_InterfaceInt(const int v)
{
   return IntegerToString(v);
}

string FP_InterfaceRunId(const string symbol,
                         const ENUM_TIMEFRAMES period,
                         const string stage,
                         const FP_InterfaceConfig &cfg)
{
   string tag = cfg.run_tag;
   if(tag == "") tag = "latest";
   return symbol + "_" + EnumToString(period) + "_" + stage + "_" + tag;
}

string FP_InterfaceFileName(const FP_InterfaceConfig &cfg,
                            const string stage)
{
   if(cfg.overwrite_latest)
      return "latest_interface_" + stage + ".csv";
   string tag = cfg.run_tag;
   if(tag == "") tag = TimeToString(TimeCurrent(), TIME_DATE|TIME_MINUTES|TIME_SECONDS);
   StringReplace(tag, ":", "");
   StringReplace(tag, ".", "_");
   StringReplace(tag, " ", "_");
   return "interface_" + stage + "_" + tag + ".csv";
}

#endif // __FP_INTERFACE_TYPES_MQH__
