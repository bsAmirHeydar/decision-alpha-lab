#ifndef __FP_VALIDATION_TYPES_MQH__
#define __FP_VALIDATION_TYPES_MQH__
#property strict

#include "FP_ExportRows.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 13 Validation Types
// ----------------------------------------------------------------------------
// Validation is a read-only acceptance harness. It consumes the final canonical
// stream, export/render counters, and deterministic user-provided expected
// ranges. It must never mutate events, hooks, visibility, identity, or chart
// objects.
// ============================================================================

struct FP_ValidationConfig
{
   bool   enabled;
   string case_id;
   string suite_tag;
   string folder;
   bool   write_csv;
   bool   overwrite_latest;
   bool   strict;
   bool   baseline_mode;
   bool   require_export_ok;
   bool   require_render_ok;
   bool   require_no_canonical_failures;
   bool   require_no_render_errors;
   bool   require_no_export_errors;
   bool   print_sanity;
   bool   print_samples;
   int    sample_limit;

   int expected_min_bars;
   int expected_max_bars;
   int expected_min_scales;
   int expected_max_scales;
   int expected_min_raw_nodes;
   int expected_max_raw_nodes;
   int expected_min_canonical_nodes;
   int expected_max_canonical_nodes;
   int expected_min_hooks;
   int expected_max_hooks;
   int expected_min_nd;
   int expected_max_nd;
   int expected_min_events;
   int expected_max_events;
   int expected_min_visible_events;
   int expected_max_visible_events;
   int expected_min_hidden_events;
   int expected_max_hidden_events;
   int expected_min_f1;
   int expected_max_f1;
   int expected_min_f2;
   int expected_max_f2;
   int expected_min_f3;
   int expected_max_f3;
   int expected_min_locked_f3;
   int expected_max_locked_f3;
};

struct FP_ValidationReport
{
   bool   attempted;
   bool   ok;
   string case_id;
   string suite_tag;
   string validation_file;
   int    checks_total;
   int    checks_passed;
   int    checks_failed;
   int    checks_warned;
   int    checks_skipped;
   int    files_written;
   int    file_errors;
   int    actual_bars;
   int    actual_scales;
   int    actual_raw_nodes;
   int    actual_canonical_nodes;
   int    actual_hooks;
   int    actual_nd;
   int    actual_events;
   int    actual_visible_events;
   int    actual_hidden_events;
   int    actual_f1;
   int    actual_f2;
   int    actual_f3;
   int    actual_locked_f3;
   int    visible_with_hidden_reason;
   int    hidden_without_reason;
   int    visible_child_without_visible_parent;
   int    visible_duplicate_canonical_id;
   int    canonical_failures;
   int    render_errors;
   int    export_errors;
   string reason;
};

void FP_DefaultValidationConfig(FP_ValidationConfig &cfg)
{
   cfg.enabled = false;
   cfg.case_id = "manual";
   cfg.suite_tag = "phoenix_level13";
   cfg.folder = "FlagCountingPhoenix";
   cfg.write_csv = true;
   cfg.overwrite_latest = true;
   cfg.strict = true;
   cfg.baseline_mode = true;
   cfg.require_export_ok = false;
   cfg.require_render_ok = true;
   cfg.require_no_canonical_failures = true;
   cfg.require_no_render_errors = true;
   cfg.require_no_export_errors = false;
   cfg.print_sanity = true;
   cfg.print_samples = false;
   cfg.sample_limit = 8;

   cfg.expected_min_bars = -1;
   cfg.expected_max_bars = -1;
   cfg.expected_min_scales = -1;
   cfg.expected_max_scales = -1;
   cfg.expected_min_raw_nodes = -1;
   cfg.expected_max_raw_nodes = -1;
   cfg.expected_min_canonical_nodes = -1;
   cfg.expected_max_canonical_nodes = -1;
   cfg.expected_min_hooks = -1;
   cfg.expected_max_hooks = -1;
   cfg.expected_min_nd = -1;
   cfg.expected_max_nd = -1;
   cfg.expected_min_events = -1;
   cfg.expected_max_events = -1;
   cfg.expected_min_visible_events = -1;
   cfg.expected_max_visible_events = -1;
   cfg.expected_min_hidden_events = -1;
   cfg.expected_max_hidden_events = -1;
   cfg.expected_min_f1 = -1;
   cfg.expected_max_f1 = -1;
   cfg.expected_min_f2 = -1;
   cfg.expected_max_f2 = -1;
   cfg.expected_min_f3 = -1;
   cfg.expected_max_f3 = -1;
   cfg.expected_min_locked_f3 = -1;
   cfg.expected_max_locked_f3 = -1;
}

void FP_ResetValidationReport(FP_ValidationReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.case_id = "";
   r.suite_tag = "";
   r.validation_file = "";
   r.checks_total = 0;
   r.checks_passed = 0;
   r.checks_failed = 0;
   r.checks_warned = 0;
   r.checks_skipped = 0;
   r.files_written = 0;
   r.file_errors = 0;
   r.actual_bars = 0;
   r.actual_scales = 0;
   r.actual_raw_nodes = 0;
   r.actual_canonical_nodes = 0;
   r.actual_hooks = 0;
   r.actual_nd = 0;
   r.actual_events = 0;
   r.actual_visible_events = 0;
   r.actual_hidden_events = 0;
   r.actual_f1 = 0;
   r.actual_f2 = 0;
   r.actual_f3 = 0;
   r.actual_locked_f3 = 0;
   r.visible_with_hidden_reason = 0;
   r.hidden_without_reason = 0;
   r.visible_child_without_visible_parent = 0;
   r.visible_duplicate_canonical_id = 0;
   r.canonical_failures = 0;
   r.render_errors = 0;
   r.export_errors = 0;
   r.reason = "not_attempted";
}

#endif // __FP_VALIDATION_TYPES_MQH__
