#ifndef __FP_AMBIGUITY_RULES_MQH__
#define __FP_AMBIGUITY_RULES_MQH__
#property strict

#include "FP_AmbiguityTypes.mqh"
#include "FP_TimebaseTypes.mqh"
#include "FP_ExportTypes.mqh"
#include "FP_RenderTypes.mqh"
#include "FP_ValidationTypes.mqh"
#include "FP_ReleaseTypes.mqh"
#include "FP_InterfaceTypes.mqh"
#include "FP_AcceptanceTypes.mqh"

// ============================================================================
// Phoenix Level 17 - Pure Ambiguity / Decision-Lock Rules
// ============================================================================

void FP_AmbiguityCsvAppend(string &line, const string value)
{
   string v = value;
   StringReplace(v, "\"", "\"\"");
   if(line != "") line += ",";
   line += "\"" + v + "\"";
}

string FP_AmbiguityHeader()
{
   string line = "";
   FP_AmbiguityCsvAppend(line, "run_id");
   FP_AmbiguityCsvAppend(line, "case_id");
   FP_AmbiguityCsvAppend(line, "mode");
   FP_AmbiguityCsvAppend(line, "decision_id");
   FP_AmbiguityCsvAppend(line, "category");
   FP_AmbiguityCsvAppend(line, "severity");
   FP_AmbiguityCsvAppend(line, "status");
   FP_AmbiguityCsvAppend(line, "actual");
   FP_AmbiguityCsvAppend(line, "expected");
   FP_AmbiguityCsvAppend(line, "canon_source");
   FP_AmbiguityCsvAppend(line, "reason");
   return line;
}

string FP_AmbiguityStatus(const bool pass, const string severity)
{
   if(pass) return "LOCKED";
   if(severity == "warn") return "WARN";
   if(severity == "skip") return "SKIP";
   return "UNLOCKED";
}

void FP_AmbiguityCountCategory(FP_AmbiguityReport &report,
                               const string category,
                               const string status)
{
   if(category == "decision")
   {
      report.decisions_total++;
      if(status == "LOCKED") report.decisions_locked++;
      else report.decisions_unlocked++;
   }
   if(category == "diagnostic") report.diagnostic_variants++;
   if(category == "release" && status == "UNLOCKED") report.release_blockers++;
   if(category == "source" && status == "UNLOCKED") report.source_conflicts++;
   if(category == "profile" && status == "UNLOCKED") report.profile_conflicts++;
   if(category == "default" && status == "UNLOCKED") report.default_conflicts++;
   if(category == "runtime" && status == "UNLOCKED") report.runtime_conflicts++;
   if(category == "legacy" && status == "UNLOCKED") report.legacy_conflicts++;
}

void FP_AmbiguityAddDecision(FP_AmbiguityReport &report,
                             string &rows[],
                             const string decision_id,
                             const string category,
                             const string severity,
                             const bool pass,
                             const string actual,
                             const string expected,
                             const string reason)
{
   report.checks_total++;
   string status = FP_AmbiguityStatus(pass, severity);
   if(status == "LOCKED") report.checks_passed++;
   else if(status == "WARN") report.checks_warned++;
   else if(status == "SKIP") report.checks_skipped++;
   else report.checks_failed++;

   FP_AmbiguityCountCategory(report, category, status);

   string line = "";
   FP_AmbiguityCsvAppend(line, report.run_id);
   FP_AmbiguityCsvAppend(line, report.case_id);
   FP_AmbiguityCsvAppend(line, report.mode_name);
   FP_AmbiguityCsvAppend(line, decision_id);
   FP_AmbiguityCsvAppend(line, category);
   FP_AmbiguityCsvAppend(line, severity);
   FP_AmbiguityCsvAppend(line, status);
   FP_AmbiguityCsvAppend(line, actual);
   FP_AmbiguityCsvAppend(line, expected);
   FP_AmbiguityCsvAppend(line, report.canon_source);
   FP_AmbiguityCsvAppend(line, reason);
   int n = ArraySize(rows);
   ArrayResize(rows, n + 1);
   rows[n] = line;
}

string FP_AmbiguityProfileNameFromConfig(const FP_ReleaseConfig &release_cfg)
{
   return FP_ReleaseProfileName(release_cfg.profile);
}

bool FP_AmbiguityReleaseLike(const FP_AmbiguityConfig &cfg,
                             const FP_ReleaseConfig &release_cfg)
{
   if(cfg.mode == FP_AMBIGUITY_MODE_RELEASE) return true;
   if(release_cfg.strict_gate) return true;
   if(release_cfg.profile == FP_RELEASE_PROFILE_VALIDATION) return true;
   return false;
}

void FP_AmbiguityAddSourceChecks(FP_AmbiguityReport &report,
                                 string &rows[],
                                 const FP_AmbiguityConfig &cfg,
                                 const FP_Config &engine_cfg)
{
   FP_AmbiguityAddDecision(report, rows, "SRC_CANON", "source", (cfg.require_canonical_source ? "error" : "warn"),
                           (!cfg.require_canonical_source || cfg.canon_source == FP_AMBIGUITY_CANON_SOURCE),
                           cfg.canon_source, FP_AMBIGUITY_CANON_SOURCE,
                           "current_canon_is_single_source_of_truth");
   FP_AmbiguityAddDecision(report, rows, "SRC_CONTRACT_VERSION", "source", "error",
                           (cfg.contract_version == FP_AMBIGUITY_CONTRACT_VERSION),
                           cfg.contract_version, FP_AMBIGUITY_CONTRACT_VERSION,
                           "ambiguity_contract_version");
   FP_AmbiguityAddDecision(report, rows, "SRC_IDENTITY_PASS", "source", "error",
                           (engine_cfg.identity_generation_pass == "phoenix_level18"),
                           engine_cfg.identity_generation_pass, "phoenix_level18",
                           "identity_generation_pass_must_match_level18_static_qa_hardened_build");
}

void FP_AmbiguityAddDefaultPolicyChecks(FP_AmbiguityReport &report,
                                        string &rows[],
                                        const FP_AmbiguityConfig &cfg,
                                        const FP_TimebaseConfig &timebase_cfg,
                                        const FP_Config &engine_cfg,
                                        const FP_RenderConfig &render_cfg)
{
   FP_AmbiguityAddDecision(report, rows, "D01_CLOSED_BAR_TIMEBASE", "default", (cfg.require_closed_bar_default ? "error" : "warn"),
                           (!cfg.require_closed_bar_default || timebase_cfg.exclude_live_bar),
                           FP_AmbiguityBool(timebase_cfg.exclude_live_bar), "true",
                           "structural_detection_uses_closed_bars_by_default");
   FP_AmbiguityAddDecision(report, rows, "D02_PENDING_F_BODIES", "decision", (cfg.require_confirmed_f_bodies ? "error" : "warn"),
                           (!cfg.require_confirmed_f_bodies || !engine_cfg.include_pending_nodes),
                           FP_AmbiguityBool(engine_cfg.include_pending_nodes), "false",
                           "confirmed_F_bodies_must_not_consume_live_pending_nodes_by_default");
   FP_AmbiguityAddDecision(report, rows, "D03_F1_PHASE_GATE", "decision", "error",
                           engine_cfg.require_f1_phase_boundary,
                           FP_AmbiguityBool(engine_cfg.require_f1_phase_boundary), "true",
                           "F1_roots_are_phase_boundary_gated_by_default");
   FP_AmbiguityAddDecision(report, rows, "D04_FAIL_OPEN_DIAGNOSTIC", "diagnostic", (cfg.allow_fail_open_diagnostic ? "warn" : "error"),
                           (cfg.allow_fail_open_diagnostic || !engine_cfg.allow_f1_fail_open_when_no_hook),
                           FP_AmbiguityBool(engine_cfg.allow_f1_fail_open_when_no_hook), "diagnostic_only",
                           "fail_open_is_allowed_only_as_tagged_diagnostic_not_source_of_truth");
   FP_AmbiguityAddDecision(report, rows, "D05_PRE_INTERNAL_EXTENSION_ABSORB", "decision", "error",
                           engine_cfg.absorb_pre_internal_extensions,
                           FP_AmbiguityBool(engine_cfg.absorb_pre_internal_extensions), "true",
                           "pre_internal_favorable_break_extends_leg2_not_confirm");
   FP_AmbiguityAddDecision(report, rows, "D06_F2_SIZE_GATE", "decision", "error",
                           (engine_cfg.f2_min_parent_size_ratio >= 1.0 && !engine_cfg.f2_show_size_rejected_candidates),
                           DoubleToString(engine_cfg.f2_min_parent_size_ratio, 4) + "/show_rejected=" + FP_AmbiguityBool(engine_cfg.f2_show_size_rejected_candidates),
                           ">=1.0/show_rejected=false",
                           "F2_main_chart_requires_size_qualified_by_default");
   FP_AmbiguityAddDecision(report, rows, "D07_F3_OR_DIAGNOSTIC", "diagnostic", (cfg.allow_or_rejected_f3_diagnostic ? "warn" : "error"),
                           (cfg.allow_or_rejected_f3_diagnostic || !engine_cfg.f3_show_or_rejected_candidates),
                           FP_AmbiguityBool(engine_cfg.f3_show_or_rejected_candidates), "false_by_default",
                           "OR_rejected_F3_candidates_are_audit_only_by_default");
   FP_AmbiguityAddDecision(report, rows, "D08_HOOK_MAIN_SEEDED", "decision", (cfg.require_seeded_hook_main_chart ? "error" : "warn"),
                           (!cfg.require_seeded_hook_main_chart || engine_cfg.hook_main_requires_visible_f1),
                           FP_AmbiguityBool(engine_cfg.hook_main_requires_visible_f1), "true",
                           "main_chart_hook_requires_seeded_visible_F1_by_default");
   FP_AmbiguityAddDecision(report, rows, "D09_UNSEEDED_HOOK_DEBUG", "diagnostic", (cfg.allow_debug_unseeded_hooks ? "warn" : "error"),
                           (cfg.allow_debug_unseeded_hooks || !engine_cfg.hook_keep_unseeded_visible_for_debug),
                           FP_AmbiguityBool(engine_cfg.hook_keep_unseeded_visible_for_debug), "false_by_default",
                           "unseeded_hooks_are_debug_only");
   FP_AmbiguityAddDecision(report, rows, "D10_STRICT_OWNERSHIP", "decision", "error",
                           engine_cfg.strict_main_chart_ownership,
                           FP_AmbiguityBool(engine_cfg.strict_main_chart_ownership), "true",
                           "one_phase_one_canonical_owner_on_main_chart");
   FP_AmbiguityAddDecision(report, rows, "D11_CANONICAL_STRICT", "decision", "error",
                           engine_cfg.canonical_strict_invariants,
                           FP_AmbiguityBool(engine_cfg.canonical_strict_invariants), "true",
                           "canonical_invariants_are_enforced_before_export_renderer");
   FP_AmbiguityAddDecision(report, rows, "D12_RENDER_STRICT_VISIBILITY", "decision", (cfg.require_strict_renderer_visibility ? "error" : "warn"),
                           (!cfg.require_strict_renderer_visibility || render_cfg.strict_visibility),
                           FP_AmbiguityBool(render_cfg.strict_visibility), "true",
                           "renderer_must_not_draw_hidden_structures_by_default");
   FP_AmbiguityAddDecision(report, rows, "D13_RENDER_CANONICAL_NAMES", "decision", (cfg.require_canonical_object_names ? "error" : "warn"),
                           (!cfg.require_canonical_object_names || render_cfg.use_canonical_object_names),
                           FP_AmbiguityBool(render_cfg.use_canonical_object_names), "true",
                           "chart_object_names_use_canonical_identity_by_default");
   bool candidate_display = (engine_cfg.f1_show_post_flag_candidates || engine_cfg.f1_show_live_body_candidates ||
                             engine_cfg.f2_show_post_flag_candidates || engine_cfg.f2_show_live_body_candidates ||
                             engine_cfg.f3_show_live_body_candidates);
   FP_AmbiguityAddDecision(report, rows, "D14_CANDIDATE_DISPLAY_DIAGNOSTIC", "diagnostic", (cfg.allow_candidate_display_diagnostic ? "warn" : "error"),
                           (cfg.allow_candidate_display_diagnostic || !candidate_display),
                           FP_AmbiguityBool(candidate_display), "diagnostic_only",
                           "developing_candidate_display_must_not_change_logical_emission");
}

void FP_AmbiguityAddPipelineChecks(FP_AmbiguityReport &report,
                                   string &rows[],
                                   const FP_AmbiguityConfig &cfg,
                                   const FP_ExportReport &export_report,
                                   const FP_RenderReport &render_report,
                                   const FP_ValidationReport &validation_report,
                                   const FP_ReleaseReport &release_report,
                                   const FP_InterfaceReport &interface_pre_report,
                                   const FP_InterfaceReport &interface_post_report,
                                   const FP_AcceptanceReport &acceptance_report)
{
   FP_AmbiguityAddDecision(report, rows, "P01_EXPORT_BEFORE_RENDER", "runtime", (cfg.require_export_before_renderer ? "error" : "warn"),
                           (!cfg.require_export_before_renderer || !export_report.attempted || export_report.ok || export_report.file_errors == 0),
                           "export_attempted=" + FP_AmbiguityBool(export_report.attempted) + "/ok=" + FP_AmbiguityBool(export_report.ok),
                           "export_readonly_before_renderer", "Level_11_5_is_report_layer_before_Level_12");
   FP_AmbiguityAddDecision(report, rows, "P02_RENDER_READONLY_OK", "runtime", "warn",
                           (!render_report.attempted || render_report.ok || render_report.object_create_failures == 0),
                           "render_attempted=" + FP_AmbiguityBool(render_report.attempted) + "/errors=" + FP_AmbiguityInt(render_report.object_create_failures),
                           "renderer_errors_zero_or_nonblocking", "renderer_is_non_authoritative");
   FP_AmbiguityAddDecision(report, rows, "P03_VALIDATION_BEFORE_RELEASE", "runtime", (cfg.require_validation_before_release ? "error" : "warn"),
                           (!cfg.require_validation_before_release || !validation_report.attempted || validation_report.ok || !release_report.gate_blocking),
                           "validation_attempted=" + FP_AmbiguityBool(validation_report.attempted) + "/ok=" + FP_AmbiguityBool(validation_report.ok) + "/release_blocking=" + FP_AmbiguityBool(release_report.gate_blocking),
                           "validation_available_for_release_gate", "validation_result_is_seen_before_release_gate");
   FP_AmbiguityAddDecision(report, rows, "P04_ACCEPTANCE_BEFORE_SUMMARY", "runtime", (cfg.require_acceptance_before_summary ? "error" : "warn"),
                           (!cfg.require_acceptance_before_summary || acceptance_report.attempted),
                           FP_AmbiguityBool(acceptance_report.attempted), "true", "acceptance_matrix_runs_before_final_summary");
   FP_AmbiguityAddDecision(report, rows, "P05_INTERFACE_ALIGNMENT", "runtime", (cfg.require_interface_pass_alignment ? "error" : "warn"),
                           (!cfg.require_interface_pass_alignment || ((!interface_pre_report.attempted || interface_pre_report.ok) && (!interface_post_report.attempted || interface_post_report.ok))),
                           "pre=" + FP_AmbiguityBool(interface_pre_report.ok) + "/post=" + FP_AmbiguityBool(interface_post_report.ok),
                           "interface_ok_when_required", "module_interface_contracts_remain_green");
}

void FP_AmbiguityAddReleaseChecks(FP_AmbiguityReport &report,
                                  string &rows[],
                                  const FP_AmbiguityConfig &cfg,
                                  const FP_ReleaseConfig &release_cfg,
                                  const FP_RenderConfig &render_cfg,
                                  const FP_ValidationReport &validation_report,
                                  const FP_AcceptanceReport &acceptance_report,
                                  const FP_DetectResult &result)
{
   bool release_like = FP_AmbiguityReleaseLike(cfg, release_cfg);
   bool no_blockers = (result.canonical_invariant_failures_total <= 0 &&
                       result.render_object_errors_total <= 0 &&
                       result.export_file_errors_total <= 0 &&
                       (!validation_report.attempted || validation_report.checks_failed <= 0) &&
                       (!acceptance_report.attempted || acceptance_report.hard_gates_failed <= 0));
   FP_AmbiguityAddDecision(report, rows, "R01_RELEASE_NO_BLOCKERS", "release", (cfg.require_no_release_blockers || release_like ? "error" : "warn"),
                           (!cfg.require_no_release_blockers && !release_like ? true : no_blockers),
                           "canon=" + FP_AmbiguityInt(result.canonical_invariant_failures_total) +
                           "/render=" + FP_AmbiguityInt(result.render_object_errors_total) +
                           "/export=" + FP_AmbiguityInt(result.export_file_errors_total) +
                           "/validation_fail=" + FP_AmbiguityInt(validation_report.checks_failed) +
                           "/acceptance_hard_fail=" + FP_AmbiguityInt(acceptance_report.hard_gates_failed),
                           "zero_blockers", "release_like_profiles_must_not_have_blocking_failures");
   FP_AmbiguityAddDecision(report, rows, "R02_RELEASE_RENDER_STRICT", "release", (release_like ? "error" : "warn"),
                           (!release_like || render_cfg.strict_visibility),
                           FP_AmbiguityBool(render_cfg.strict_visibility), "true", "release_like_profiles_keep_renderer_strict");
   FP_AmbiguityAddDecision(report, rows, "R03_RELEASE_PROFILE_NAME", "profile", "error",
                           (release_cfg.profile >= FP_RELEASE_PROFILE_NORMAL && release_cfg.profile <= FP_RELEASE_PROFILE_SAFE_ROLLBACK),
                           FP_AmbiguityProfileNameFromConfig(release_cfg), "known_profile", "release_profile_enum_is_known");
}

#endif // __FP_AMBIGUITY_RULES_MQH__
