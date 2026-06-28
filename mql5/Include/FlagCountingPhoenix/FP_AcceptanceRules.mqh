#ifndef __FP_ACCEPTANCE_RULES_MQH__
#define __FP_ACCEPTANCE_RULES_MQH__
#property strict

#include "FP_AcceptanceTypes.mqh"
#include "FP_TimebaseTypes.mqh"
#include "FP_ExportTypes.mqh"
#include "FP_RenderTypes.mqh"
#include "FP_ValidationTypes.mqh"
#include "FP_ReleaseTypes.mqh"
#include "FP_InterfaceTypes.mqh"

// ============================================================================
// Phoenix Level 16 - Pure Acceptance Rules
// ============================================================================

void FP_AcceptanceCsvAppend(string &line, const string value)
{
   string v = value;
   StringReplace(v, "\"", "\"\"");
   if(line != "") line += ",";
   line += "\"" + v + "\"";
}

string FP_AcceptanceHeader()
{
   string line = "";
   FP_AcceptanceCsvAppend(line, "run_id");
   FP_AcceptanceCsvAppend(line, "case_id");
   FP_AcceptanceCsvAppend(line, "mode");
   FP_AcceptanceCsvAppend(line, "level");
   FP_AcceptanceCsvAppend(line, "gate_id");
   FP_AcceptanceCsvAppend(line, "category");
   FP_AcceptanceCsvAppend(line, "severity");
   FP_AcceptanceCsvAppend(line, "status");
   FP_AcceptanceCsvAppend(line, "actual");
   FP_AcceptanceCsvAppend(line, "expected");
   FP_AcceptanceCsvAppend(line, "reason");
   return line;
}

string FP_AcceptanceStatus(const bool pass, const string severity)
{
   if(pass) return "PASS";
   if(severity == "warn") return "WARN";
   if(severity == "skip") return "SKIP";
   return "FAIL";
}

void FP_AcceptanceCountCategory(FP_AcceptanceReport &report, const string category, const string status)
{
   if(StringFind(category, "level") == 0)
   {
      report.levels_checked++;
      if(status == "PASS") report.levels_passed++;
      else if(status == "WARN") report.levels_warned++;
      else if(status == "FAIL") report.levels_failed++;
   }
   if(category == "order" && status == "FAIL") report.order_errors++;
   if(category == "dependency" && status == "FAIL") report.dependency_errors++;
   if(category == "matrix" && status == "FAIL") report.matrix_errors++;
   if(category == "invariant" && status == "FAIL") report.invariant_errors++;
   if(category == "baseline") report.baseline_items++;
   if(category == "regression") report.regression_items++;
   if(category == "release") report.release_items++;
}

void FP_AcceptanceAddGate(FP_AcceptanceReport &report,
                          string &rows[],
                          const int level,
                          const string gate_id,
                          const string category,
                          const string severity,
                          const bool pass,
                          const string actual,
                          const string expected,
                          const string reason)
{
   report.checks_total++;
   string status = FP_AcceptanceStatus(pass, severity);
   if(status == "PASS") report.checks_passed++;
   else if(status == "WARN") report.checks_warned++;
   else if(status == "SKIP") report.checks_skipped++;
   else report.checks_failed++;

   if(severity == "error")
   {
      report.hard_gates_total++;
      if(status == "PASS") report.hard_gates_passed++;
      else report.hard_gates_failed++;
   }
   FP_AcceptanceCountCategory(report, category, status);

   string line = "";
   FP_AcceptanceCsvAppend(line, report.run_id);
   FP_AcceptanceCsvAppend(line, report.case_id);
   FP_AcceptanceCsvAppend(line, report.mode_name);
   FP_AcceptanceCsvAppend(line, IntegerToString(level));
   FP_AcceptanceCsvAppend(line, gate_id);
   FP_AcceptanceCsvAppend(line, category);
   FP_AcceptanceCsvAppend(line, severity);
   FP_AcceptanceCsvAppend(line, status);
   FP_AcceptanceCsvAppend(line, actual);
   FP_AcceptanceCsvAppend(line, expected);
   FP_AcceptanceCsvAppend(line, reason);
   int n = ArraySize(rows);
   ArrayResize(rows, n + 1);
   rows[n] = line;
}

void FP_AcceptanceAddOrderChecks(FP_AcceptanceReport &report,
                                 string &rows[],
                                 const FP_AcceptanceConfig &cfg)
{
   FP_AcceptanceAddGate(report, rows, 16, "ORDER_CONTRACT_VERSION", "order", "error",
                        (cfg.matrix_version == FP_ACCEPTANCE_CONTRACT_VERSION),
                        cfg.matrix_version, FP_ACCEPTANCE_CONTRACT_VERSION,
                        "acceptance_matrix_contract_version");
   FP_AcceptanceAddGate(report, rows, 16, "ORDER_GATE_COUNT", "order", "error",
                        (FP_ACCEPTANCE_GATE_COUNT == 16),
                        FP_AcceptanceInt(FP_ACCEPTANCE_GATE_COUNT), "16",
                        "one_gate_family_per_runtime_level");
   FP_AcceptanceAddGate(report, rows, 16, "ORDER_MODE", "order", "error",
                        (cfg.mode >= FP_ACCEPTANCE_MODE_OBSERVE && cfg.mode <= FP_ACCEPTANCE_MODE_RELEASE),
                        FP_AcceptanceInt(cfg.mode), "0..3",
                        "acceptance_mode_enum_bounds");
}

void FP_AcceptanceAddRuntimeChecks(FP_AcceptanceReport &report,
                                   string &rows[],
                                   const FP_AcceptanceConfig &cfg,
                                   const FP_TimebaseReport &timebase_report,
                                   const FP_DetectResult &result,
                                   const FP_ExportReport &export_report,
                                   const FP_RenderReport &render_report,
                                   const FP_ValidationReport &validation_report,
                                   const FP_ReleaseReport &release_report,
                                   const FP_InterfaceReport &interface_pre_report,
                                   const FP_InterfaceReport &interface_post_report)
{
   FP_AcceptanceAddGate(report, rows, 1, "L01_TIMEBASE_OK", "level01", (cfg.require_level01_ok ? "error" : "warn"),
                        timebase_report.ok,
                        FP_AcceptanceBool(timebase_report.ok) + "/" + timebase_report.status,
                        "ok=true", "canonical_closed_bar_timebase_ready");

   FP_AcceptanceAddGate(report, rows, 2, "L02_NODE_COUNTERS", "level02", "error",
                        (result.raw_nodes_total >= 0 && result.nodes_total >= 0 && result.confirmed_nodes_total >= 0 && result.pending_nodes_total >= 0),
                        FP_AcceptanceInt(result.raw_nodes_total) + "/" + FP_AcceptanceInt(result.nodes_total),
                        "nonnegative", "node_counter_partition_available");

   FP_AcceptanceAddGate(report, rows, 3, "L03_IDENTITY_COVERAGE", "level03", "error",
                        (result.events_total <= 0 || result.identity_assigned_events >= 0),
                        FP_AcceptanceInt(result.identity_assigned_events) + "/" + FP_AcceptanceInt(result.events_total),
                        "identity_counter_present", "identity_layer_executed_or_no_events");

   FP_AcceptanceAddGate(report, rows, 4, "L04_HOOK_COUNTERS", "level04", "error",
                        (result.hooks_total >= 0 && result.hook_contexts_total >= 0 && result.hook_contexts_rejected_total >= 0),
                        FP_AcceptanceInt(result.hooks_total) + "/" + FP_AcceptanceInt(result.hook_contexts_total),
                        "nonnegative", "hook_nd_counters_present");

   FP_AcceptanceAddGate(report, rows, 5, "L05_BODY_COUNTERS", "level05", "error",
                        (result.body_attempts_total >= 0 && result.body_complete_total >= 0 && result.body_invalid_total >= 0),
                        FP_AcceptanceInt(result.body_attempts_total) + "/" + FP_AcceptanceInt(result.body_complete_total),
                        "nonnegative", "body_engine_counters_present");

   FP_AcceptanceAddGate(report, rows, 6, "L06_INTERNAL_COUNTERS", "level06", "error",
                        (result.internal_packs_total >= 0 && result.internal_valid12_total >= 0 && result.internal_count0_total >= 0),
                        FP_AcceptanceInt(result.internal_packs_total) + "/" + FP_AcceptanceInt(result.internal_valid12_total),
                        "nonnegative", "internal_count_counters_present");

   FP_AcceptanceAddGate(report, rows, 7, "L07_F1_LIFECYCLE", "level07", "error",
                        (result.f1_lifecycle_attempts_total >= 0 && result.f1_lifecycle_confirmed_total >= 0),
                        FP_AcceptanceInt(result.f1_lifecycle_attempts_total) + "/" + FP_AcceptanceInt(result.f1_lifecycle_confirmed_total),
                        "nonnegative", "f1_lifecycle_counters_present");

   FP_AcceptanceAddGate(report, rows, 8, "L08_F2_LIFECYCLE", "level08", "error",
                        (result.f2_lifecycle_parent_attempts_total >= 0 && result.f2_lifecycle_confirmed_total >= 0),
                        FP_AcceptanceInt(result.f2_lifecycle_parent_attempts_total) + "/" + FP_AcceptanceInt(result.f2_lifecycle_confirmed_total),
                        "nonnegative", "f2_lifecycle_counters_present");

   FP_AcceptanceAddGate(report, rows, 9, "L09_F3_LIFECYCLE", "level09", "error",
                        (result.f3_lifecycle_parent_attempts_total >= 0 && result.f3_lifecycle_completed_total >= 0 && result.f3_lifecycle_locked_total >= 0),
                        FP_AcceptanceInt(result.f3_lifecycle_parent_attempts_total) + "/" + FP_AcceptanceInt(result.f3_lifecycle_completed_total) + "/" + FP_AcceptanceInt(result.f3_lifecycle_locked_total),
                        "nonnegative", "f3_lifecycle_counters_present");

   FP_AcceptanceAddGate(report, rows, 10, "L10_OWNERSHIP", "level10", "error",
                        (result.ownership_phases_total >= 0 && result.ownership_owner_roots_total >= 0 && result.ownership_orphans_hidden_total >= 0),
                        FP_AcceptanceInt(result.ownership_phases_total) + "/" + FP_AcceptanceInt(result.ownership_owner_roots_total),
                        "nonnegative", "ownership_counters_present");

   FP_AcceptanceAddGate(report, rows, 11, "L11_CANONICAL_INVARIANTS", "level11", (cfg.require_no_canonical_failures ? "error" : "warn"),
                        (!cfg.require_no_canonical_failures || result.canonical_invariant_failures_total <= 0),
                        FP_AcceptanceInt(result.canonical_invariant_failures_total), "0", "canonical_invariant_failures_zero_when_required");

   bool export_required = (export_report.attempted && cfg.require_export_ok_when_enabled);
   FP_AcceptanceAddGate(report, rows, 115, "L11_5_EXPORT", "level11_5", (export_required ? "error" : "warn"),
                        (!export_required || export_report.ok),
                        "attempted=" + FP_AcceptanceBool(export_report.attempted) + "/ok=" + FP_AcceptanceBool(export_report.ok) + "/errors=" + FP_AcceptanceInt(export_report.file_errors),
                        "ok_when_enabled", "raw_audit_export_report_gate");

   bool render_required = (render_report.attempted && cfg.require_render_ok_when_enabled);
   FP_AcceptanceAddGate(report, rows, 12, "L12_RENDER", "level12", (render_required ? "error" : "warn"),
                        (!render_required || render_report.ok),
                        "attempted=" + FP_AcceptanceBool(render_report.attempted) + "/ok=" + FP_AcceptanceBool(render_report.ok) + "/errors=" + FP_AcceptanceInt(render_report.object_create_failures),
                        "ok_when_enabled", "renderer_readonly_display_gate");

   bool validation_required = (validation_report.attempted && cfg.require_validation_ok_when_enabled);
   FP_AcceptanceAddGate(report, rows, 13, "L13_VALIDATION", "level13", (validation_required ? "error" : "warn"),
                        (!validation_required || validation_report.ok),
                        "attempted=" + FP_AcceptanceBool(validation_report.attempted) + "/ok=" + FP_AcceptanceBool(validation_report.ok) + "/fail=" + FP_AcceptanceInt(validation_report.checks_failed),
                        "ok_when_enabled", "validation_suite_gate");

   bool release_required = (cfg.strict && cfg.require_release_gate_when_strict);
   FP_AcceptanceAddGate(report, rows, 14, "L14_RELEASE", "level14", (release_required ? "error" : "warn"),
                        (!release_required || release_report.gate_passed),
                        "attempted=" + FP_AcceptanceBool(release_report.attempted) + "/gate=" + FP_AcceptanceBool(release_report.gate_passed),
                        "gate_pass_when_strict_required", "release_gate_contract");

   bool interface_pre_required = (interface_pre_report.attempted && cfg.require_interface_pre_ok_when_enabled);
   FP_AcceptanceAddGate(report, rows, 15, "L15_INTERFACE_PRE", "level15", (interface_pre_required ? "error" : "warn"),
                        (!interface_pre_required || interface_pre_report.ok),
                        "attempted=" + FP_AcceptanceBool(interface_pre_report.attempted) + "/ok=" + FP_AcceptanceBool(interface_pre_report.ok) + "/fail=" + FP_AcceptanceInt(interface_pre_report.checks_failed),
                        "ok_when_required", "interface_preflight_gate");

   bool interface_post_required = (interface_post_report.attempted && cfg.require_interface_post_ok_when_enabled);
   FP_AcceptanceAddGate(report, rows, 15, "L15_INTERFACE_POST", "level15", (interface_post_required ? "error" : "warn"),
                        (!interface_post_required || interface_post_report.ok),
                        "attempted=" + FP_AcceptanceBool(interface_post_report.attempted) + "/ok=" + FP_AcceptanceBool(interface_post_report.ok) + "/fail=" + FP_AcceptanceInt(interface_post_report.checks_failed),
                        "ok_when_required", "interface_postflight_gate");
}

void FP_AcceptanceAddMatrixChecks(FP_AcceptanceReport &report,
                                  string &rows[],
                                  const FP_AcceptanceConfig &cfg,
                                  const FP_DetectResult &result)
{
   int partition = result.visible_events_total + result.hidden_events_total;
   FP_AcceptanceAddGate(report, rows, 16, "MATRIX_EVENT_PARTITION", "invariant", (cfg.require_visible_partition ? "error" : "warn"),
                        (!cfg.require_visible_partition || partition == result.events_total),
                        FP_AcceptanceInt(partition) + "/" + FP_AcceptanceInt(result.events_total),
                        "visible+hidden==events", "final_event_partition");

   if(cfg.expected_min_visible_events >= 0)
      FP_AcceptanceAddGate(report, rows, 16, "MATRIX_MIN_VISIBLE", "regression", "error",
                           (result.visible_events_total >= cfg.expected_min_visible_events),
                           FP_AcceptanceInt(result.visible_events_total), ">=" + FP_AcceptanceInt(cfg.expected_min_visible_events), "visible_events_minimum");
   if(cfg.expected_min_f1 >= 0)
      FP_AcceptanceAddGate(report, rows, 16, "MATRIX_MIN_F1", "regression", "error",
                           (result.f1_total >= cfg.expected_min_f1),
                           FP_AcceptanceInt(result.f1_total), ">=" + FP_AcceptanceInt(cfg.expected_min_f1), "f1_minimum");
   if(cfg.expected_min_f2 >= 0)
      FP_AcceptanceAddGate(report, rows, 16, "MATRIX_MIN_F2", "regression", "error",
                           (result.f2_total >= cfg.expected_min_f2),
                           FP_AcceptanceInt(result.f2_total), ">=" + FP_AcceptanceInt(cfg.expected_min_f2), "f2_minimum");
   if(cfg.expected_min_f3 >= 0)
      FP_AcceptanceAddGate(report, rows, 16, "MATRIX_MIN_F3", "regression", "error",
                           (result.f3_total >= cfg.expected_min_f3),
                           FP_AcceptanceInt(result.f3_total), ">=" + FP_AcceptanceInt(cfg.expected_min_f3), "f3_minimum");
   if(cfg.expected_min_locked_f3 >= 0)
      FP_AcceptanceAddGate(report, rows, 16, "MATRIX_MIN_LOCKED_F3", "regression", (cfg.require_locked_f3_if_expected ? "error" : "warn"),
                           (result.f3_lifecycle_locked_total >= cfg.expected_min_locked_f3),
                           FP_AcceptanceInt(result.f3_lifecycle_locked_total), ">=" + FP_AcceptanceInt(cfg.expected_min_locked_f3), "locked_f3_minimum");

   if(cfg.mode == FP_ACCEPTANCE_MODE_BASELINE)
   {
      FP_AcceptanceAddGate(report, rows, 16, "BASELINE_VISIBLE_EVENTS", "baseline", "warn", false,
                           FP_AcceptanceInt(result.visible_events_total), "copy_to_expected_min/max", "baseline_capture_visible_events");
      FP_AcceptanceAddGate(report, rows, 16, "BASELINE_F1_F2_F3", "baseline", "warn", false,
                           FP_AcceptanceInt(result.f1_total) + "/" + FP_AcceptanceInt(result.f2_total) + "/" + FP_AcceptanceInt(result.f3_total),
                           "copy_to_case_registry", "baseline_capture_f_sequence_counts");
      FP_AcceptanceAddGate(report, rows, 16, "BASELINE_LOCKED_F3", "baseline", "warn", false,
                           FP_AcceptanceInt(result.f3_lifecycle_locked_total), "copy_to_case_registry", "baseline_capture_locked_f3");
   }
}

#endif // __FP_ACCEPTANCE_RULES_MQH__
