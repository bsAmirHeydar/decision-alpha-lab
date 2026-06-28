#ifndef __FP_AMBIGUITY_TYPES_MQH__
#define __FP_AMBIGUITY_TYPES_MQH__
#property strict

#include "FP_AcceptanceTypes.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 17 Ambiguity Types
// ----------------------------------------------------------------------------
// Level 17 closes the implementation ladder by turning formerly open decisions
// into a runtime decision registry. It is read-only: it audits default policy,
// diagnostic variants, profile consistency, and source-of-truth alignment after
// Level 16 acceptance has run.
// ============================================================================

#define FP_AMBIGUITY_CONTRACT_VERSION "17.00"
#define FP_AMBIGUITY_DECISION_COUNT   17
#define FP_AMBIGUITY_CANON_SOURCE     "FLAG_COUNTING_CURRENT_CANON.md"

enum FP_AmbiguityMode
{
   FP_AMBIGUITY_MODE_OBSERVE    = 0,
   FP_AMBIGUITY_MODE_BASELINE   = 1,
   FP_AMBIGUITY_MODE_REGRESSION = 2,
   FP_AMBIGUITY_MODE_RELEASE    = 3
};

struct FP_AmbiguityConfig
{
   bool   enabled;
   int    mode;
   bool   strict;
   bool   write_csv;
   bool   overwrite_latest;
   string folder;
   string run_tag;
   string case_id;
   string canon_source;
   string contract_version;

   bool   require_decision_lock;
   bool   require_no_release_blockers;
   bool   require_canonical_source;
   bool   require_closed_bar_default;
   bool   require_confirmed_f_bodies;
   bool   require_strict_renderer_visibility;
   bool   require_canonical_object_names;
   bool   require_seeded_hook_main_chart;
   bool   require_export_before_renderer;
   bool   require_validation_before_release;
   bool   require_acceptance_before_summary;
   bool   require_interface_pass_alignment;

   bool   allow_fail_open_diagnostic;
   bool   allow_candidate_display_diagnostic;
   bool   allow_or_rejected_f3_diagnostic;
   bool   allow_debug_unseeded_hooks;

   bool   print_sanity;
   bool   print_samples;
   int    sample_limit;
};

struct FP_AmbiguityReport
{
   bool   attempted;
   bool   ok;
   string mode_name;
   string run_id;
   string case_id;
   string folder;
   string report_file;
   string canon_source;
   string reason;

   int checks_total;
   int checks_passed;
   int checks_failed;
   int checks_warned;
   int checks_skipped;
   int file_errors;
   int files_written;

   int decisions_total;
   int decisions_locked;
   int decisions_unlocked;
   int diagnostic_variants;
   int release_blockers;
   int source_conflicts;
   int profile_conflicts;
   int default_conflicts;
   int runtime_conflicts;
   int legacy_conflicts;
};

string FP_AmbiguityModeName(const int mode)
{
   if(mode == FP_AMBIGUITY_MODE_BASELINE)   return "baseline";
   if(mode == FP_AMBIGUITY_MODE_REGRESSION) return "regression";
   if(mode == FP_AMBIGUITY_MODE_RELEASE)    return "release";
   return "observe";
}

void FP_DefaultAmbiguityConfig(FP_AmbiguityConfig &cfg)
{
   cfg.enabled = true;
   cfg.mode = FP_AMBIGUITY_MODE_OBSERVE;
   cfg.strict = false;
   cfg.write_csv = false;
   cfg.overwrite_latest = true;
   cfg.folder = "FlagCountingPhoenix";
   cfg.run_tag = "";
   cfg.case_id = "manual";
   cfg.canon_source = FP_AMBIGUITY_CANON_SOURCE;
   cfg.contract_version = FP_AMBIGUITY_CONTRACT_VERSION;

   cfg.require_decision_lock = true;
   cfg.require_no_release_blockers = false;
   cfg.require_canonical_source = true;
   cfg.require_closed_bar_default = true;
   cfg.require_confirmed_f_bodies = true;
   cfg.require_strict_renderer_visibility = true;
   cfg.require_canonical_object_names = true;
   cfg.require_seeded_hook_main_chart = true;
   cfg.require_export_before_renderer = true;
   cfg.require_validation_before_release = true;
   cfg.require_acceptance_before_summary = true;
   cfg.require_interface_pass_alignment = false;

   cfg.allow_fail_open_diagnostic = true;
   cfg.allow_candidate_display_diagnostic = true;
   cfg.allow_or_rejected_f3_diagnostic = false;
   cfg.allow_debug_unseeded_hooks = false;

   cfg.print_sanity = true;
   cfg.print_samples = false;
   cfg.sample_limit = 8;
}

void FP_ResetAmbiguityReport(FP_AmbiguityReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.mode_name = "";
   r.run_id = "";
   r.case_id = "";
   r.folder = "";
   r.report_file = "";
   r.canon_source = "";
   r.reason = "";

   r.checks_total = 0;
   r.checks_passed = 0;
   r.checks_failed = 0;
   r.checks_warned = 0;
   r.checks_skipped = 0;
   r.file_errors = 0;
   r.files_written = 0;

   r.decisions_total = 0;
   r.decisions_locked = 0;
   r.decisions_unlocked = 0;
   r.diagnostic_variants = 0;
   r.release_blockers = 0;
   r.source_conflicts = 0;
   r.profile_conflicts = 0;
   r.default_conflicts = 0;
   r.runtime_conflicts = 0;
   r.legacy_conflicts = 0;
}

string FP_AmbiguityBool(const bool v)
{
   return (v ? "true" : "false");
}

string FP_AmbiguityInt(const int v)
{
   return IntegerToString(v);
}

string FP_AmbiguityRunId(const string symbol,
                         const ENUM_TIMEFRAMES period,
                         const FP_AmbiguityConfig &cfg)
{
   string tag = cfg.run_tag;
   if(tag == "") tag = "latest";
   return symbol + "_" + EnumToString(period) + "_ambiguity_" + tag;
}

string FP_AmbiguityFileName(const FP_AmbiguityConfig &cfg)
{
   if(cfg.overwrite_latest)
      return "latest_ambiguity.csv";
   string tag = cfg.run_tag;
   if(tag == "") tag = TimeToString(TimeCurrent(), TIME_DATE|TIME_MINUTES|TIME_SECONDS);
   StringReplace(tag, ":", "");
   StringReplace(tag, ".", "_");
   StringReplace(tag, " ", "_");
   return "ambiguity_" + tag + ".csv";
}

#endif // __FP_AMBIGUITY_TYPES_MQH__
