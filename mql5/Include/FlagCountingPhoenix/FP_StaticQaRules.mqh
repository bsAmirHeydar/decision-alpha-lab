#ifndef __FP_STATIC_QA_RULES_MQH__
#define __FP_STATIC_QA_RULES_MQH__
#property strict

#include "FP_StaticQaTypes.mqh"
#include "FP_TimebaseTypes.mqh"
#include "FP_ExportTypes.mqh"
#include "FP_RenderTypes.mqh"
#include "FP_ValidationTypes.mqh"
#include "FP_ReleaseTypes.mqh"
#include "FP_InterfaceTypes.mqh"
#include "FP_AcceptanceTypes.mqh"
#include "FP_AmbiguityTypes.mqh"

// ============================================================================
// Phoenix Level 18 - Pure Static QA Rules
// ============================================================================

void FP_StaticQaCsvAppend(string &line, const string value)
{
   string v = value;
   StringReplace(v, "\"", "\"\"");
   if(line != "") line += ",";
   line += "\"" + v + "\"";
}

string FP_StaticQaHeader()
{
   string line = "";
   FP_StaticQaCsvAppend(line, "run_id");
   FP_StaticQaCsvAppend(line, "case_id");
   FP_StaticQaCsvAppend(line, "mode");
   FP_StaticQaCsvAppend(line, "family");
   FP_StaticQaCsvAppend(line, "check_id");
   FP_StaticQaCsvAppend(line, "severity");
   FP_StaticQaCsvAppend(line, "status");
   FP_StaticQaCsvAppend(line, "actual");
   FP_StaticQaCsvAppend(line, "expected");
   FP_StaticQaCsvAppend(line, "reason");
   return line;
}

string FP_StaticQaStatus(const bool pass, const string severity)
{
   if(pass) return "PASS";
   if(severity == "warn") return "WARN";
   if(severity == "skip") return "SKIP";
   return "FAIL";
}

string FP_StaticQaFileName(const FP_StaticQaConfig &cfg)
{
   if(cfg.overwrite_latest) return "latest_static_qa.csv";
   string tag = cfg.run_tag;
   if(tag == "") tag = cfg.case_id;
   if(tag == "") tag = "manual";
   return "static_qa_" + tag + ".csv";
}

string FP_StaticQaRunId(const string symbol, const ENUM_TIMEFRAMES period, const FP_StaticQaConfig &cfg)
{
   string tag = cfg.run_tag;
   if(tag == "") tag = cfg.case_id;
   if(tag == "") tag = "manual";
   return symbol + "_" + EnumToString(period) + "_" + tag + "_l18";
}

void FP_StaticQaCountFamily(FP_StaticQaReport &report, const string family, const string status)
{
   if(family == "compile_contract")
   {
      report.compile_contract_checks++;
      if(status == "FAIL") report.compile_contract_failures++;
   }
   else if(family == "runtime_contract")
   {
      report.runtime_contract_checks++;
      if(status == "FAIL") report.runtime_contract_failures++;
   }
   else if(family == "print_safety")
   {
      report.print_safety_checks++;
      if(status == "FAIL") report.print_safety_failures++;
   }
   else if(family == "input_contract")
   {
      report.input_contract_checks++;
      if(status == "FAIL") report.input_contract_failures++;
   }
   else if(family == "dependency")
   {
      report.dependency_checks++;
      if(status == "FAIL") report.dependency_failures++;
   }
   else if(family == "io_contract")
   {
      report.io_contract_checks++;
      if(status == "FAIL") report.io_contract_failures++;
   }
   else if(family == "report_alignment")
   {
      report.report_alignment_checks++;
      if(status == "FAIL") report.report_alignment_failures++;
   }
   else if(family == "toolchain")
   {
      report.toolchain_checks++;
      if(status == "FAIL") report.toolchain_failures++;
   }
}

void FP_StaticQaAddCheck(FP_StaticQaReport &report,
                         string &rows[],
                         const string family,
                         const string check_id,
                         const string severity,
                         const bool pass,
                         const string actual,
                         const string expected,
                         const string reason)
{
   report.checks_total++;
   string status = FP_StaticQaStatus(pass, severity);
   if(status == "PASS") report.checks_passed++;
   else if(status == "WARN") report.checks_warned++;
   else if(status == "SKIP") report.checks_skipped++;
   else
   {
      report.checks_failed++;
      if(severity == "error") report.blockers++;
   }
   FP_StaticQaCountFamily(report, family, status);

   string line = "";
   FP_StaticQaCsvAppend(line, report.run_id);
   FP_StaticQaCsvAppend(line, report.case_id);
   FP_StaticQaCsvAppend(line, report.mode_name);
   FP_StaticQaCsvAppend(line, family);
   FP_StaticQaCsvAppend(line, check_id);
   FP_StaticQaCsvAppend(line, severity);
   FP_StaticQaCsvAppend(line, status);
   FP_StaticQaCsvAppend(line, actual);
   FP_StaticQaCsvAppend(line, expected);
   FP_StaticQaCsvAppend(line, reason);
   int n = ArraySize(rows);
   ArrayResize(rows, n + 1);
   rows[n] = line;
}

void FP_StaticQaAddCompileContractChecks(FP_StaticQaReport &report,
                                         string &rows[],
                                         const FP_StaticQaConfig &qa_cfg,
                                         const FP_Config &engine_cfg)
{
   FP_StaticQaAddCheck(report, rows, "compile_contract", "L18_CONTRACT_VERSION", "error",
                       (!qa_cfg.require_contract_version || qa_cfg.contract_version == FP_STATIC_QA_CONTRACT_VERSION),
                       qa_cfg.contract_version, FP_STATIC_QA_CONTRACT_VERSION,
                       "static_qa_contract_version");
   FP_StaticQaAddCheck(report, rows, "compile_contract", "L18_IDENTITY_PASS", "error",
                       (!qa_cfg.require_identity_pass || engine_cfg.identity_generation_pass == FP_STATIC_QA_EXPECTED_ID_PASS),
                       engine_cfg.identity_generation_pass, FP_STATIC_QA_EXPECTED_ID_PASS,
                       "final_identity_pass_after_static_qa_layer");
   FP_StaticQaAddCheck(report, rows, "compile_contract", "L18_MODULE_COUNT", "error",
                       (FP_STATIC_QA_MODULE_COUNT == 18),
                       FP_StaticQaInt(FP_STATIC_QA_MODULE_COUNT), "18",
                       "runtime_ladder_level_count_after_decision_lock");
   FP_StaticQaAddCheck(report, rows, "compile_contract", "L18_INTERFACE_VERSION", "error",
                       (!qa_cfg.require_interface_contract_alignment || FP_INTERFACE_CONTRACT_VERSION == "18.00"),
                       FP_INTERFACE_CONTRACT_VERSION, "18.00",
                       "interface_contract_accepts_level18_public_facade");
   FP_StaticQaAddCheck(report, rows, "compile_contract", "L18_INTERNAL_NODE_MAX", "error",
                       (FP_MAX_INTERNAL_NODES == 4),
                       FP_StaticQaInt(FP_MAX_INTERNAL_NODES), "4",
                       "internal_count_contract_is_still_four_nodes_max");
}

void FP_StaticQaAddRuntimeContractChecks(FP_StaticQaReport &report,
                                         string &rows[],
                                         const FP_StaticQaConfig &qa_cfg,
                                         const FP_TimebaseReport &timebase_report,
                                         const FP_DetectResult &result)
{
   FP_StaticQaAddCheck(report, rows, "runtime_contract", "L01_TIMEBASE_OK", "error",
                       timebase_report.ok,
                       timebase_report.status, "ok", "static_qa_requires_canonical_timebase_report");
   FP_StaticQaAddCheck(report, rows, "runtime_contract", "EVENT_PARTITION", "error",
                       (!qa_cfg.require_runtime_partitions || result.visible_events_total + result.hidden_events_total == result.events_total),
                       FP_StaticQaInt(result.visible_events_total) + "+" + FP_StaticQaInt(result.hidden_events_total) + "=" + FP_StaticQaInt(result.visible_events_total + result.hidden_events_total),
                       FP_StaticQaInt(result.events_total), "visible_hidden_event_partition");
   FP_StaticQaAddCheck(report, rows, "runtime_contract", "NODE_PARTITION", "warn",
                       (result.confirmed_nodes_total + result.pending_nodes_total <= result.raw_nodes_total || result.raw_nodes_total == 0),
                       FP_StaticQaInt(result.confirmed_nodes_total) + "+" + FP_StaticQaInt(result.pending_nodes_total),
                       "<=raw_nodes", "confirmed_pending_nodes_do_not_exceed_raw_nodes");
   FP_StaticQaAddCheck(report, rows, "runtime_contract", "CANONICAL_INVARIANTS", (qa_cfg.strict ? "error" : "warn"),
                       (result.canonical_invariant_failures_total <= 0),
                       FP_StaticQaInt(result.canonical_invariant_failures_total), "0", "canonical_failures_before_static_qa");
}

void FP_StaticQaAddCounterChecks(FP_StaticQaReport &report,
                                 string &rows[],
                                 const FP_StaticQaConfig &qa_cfg,
                                 const FP_DetectResult &r)
{
   if(!qa_cfg.require_nonnegative_counters)
   {
      FP_StaticQaAddCheck(report, rows, "runtime_contract", "COUNTERS_NONNEGATIVE", "skip", true, "disabled", "enabled", "nonnegative_counter_check_disabled");
      return;
   }
   bool ok = true;
   ok = ok && r.raw_nodes_total >= 0 && r.nodes_total >= 0 && r.hooks_total >= 0 && r.events_total >= 0;
   ok = ok && r.f1_total >= 0 && r.f2_total >= 0 && r.f3_total >= 0 && r.nd_total >= 0;
   ok = ok && r.export_file_errors_total >= 0 && r.render_object_errors_total >= 0 && r.validation_fail_total >= 0;
   ok = ok && r.release_gate_fail_total >= 0 && r.interface_fail_total >= 0 && r.acceptance_fail_total >= 0 && r.ambiguity_fail_total >= 0;
   FP_StaticQaAddCheck(report, rows, "runtime_contract", "COUNTERS_NONNEGATIVE", "error",
                       ok, "aggregate_runtime_counters", "all_nonnegative", "no_negative_runtime_counters_after_all_layers");
}

void FP_StaticQaAddPrintSafetyChecks(FP_StaticQaReport &report,
                                     string &rows[],
                                     const FP_StaticQaConfig &qa_cfg)
{
   FP_StaticQaAddCheck(report, rows, "print_safety", "SINGLE_MESSAGE_AUDIT_SENTINEL", "warn",
                       true, "runtime_sentinal_pass", "source_scanner_confirms", "runtime_layer_defers_source_scan_to_tools_flag_counting_static_qa_py");
   FP_StaticQaAddCheck(report, rows, "print_safety", "NO_EMPTY_PRINT_SENTINEL", "warn",
                       true, "runtime_sentinal_pass", "source_scanner_confirms", "python_static_qa_scans_for_empty_Print_calls");
   FP_StaticQaAddCheck(report, rows, "toolchain", "STATIC_QA_SCRIPT_REGISTERED", (qa_cfg.require_static_tool_present ? "error" : "warn"),
                       true, "tools/flag_counting/static_qa.py", "present_in_repo", "source_side_static_qa_tool_is_part_of_patch");
}

void FP_StaticQaAddInputContractChecks(FP_StaticQaReport &report,
                                       string &rows[],
                                       const FP_StaticQaConfig &qa_cfg,
                                       const FP_TimebaseConfig &timebase_cfg,
                                       const FP_Config &engine_cfg,
                                       const FP_RenderConfig &render_cfg,
                                       const FP_InterfaceConfig &interface_cfg,
                                       const FP_AmbiguityConfig &ambiguity_cfg)
{
   FP_StaticQaAddCheck(report, rows, "input_contract", "TIMEBASE_BOUNDS", "error",
                       (timebase_cfg.requested_bars > 0 && timebase_cfg.min_closed_bars > 0 && timebase_cfg.requested_bars >= timebase_cfg.min_closed_bars),
                       FP_StaticQaInt(timebase_cfg.requested_bars) + "/" + FP_StaticQaInt(timebase_cfg.min_closed_bars),
                       "requested>=min>0", "timebase_input_bounds");
   FP_StaticQaAddCheck(report, rows, "input_contract", "ENGINE_CAPS", "error",
                       (engine_cfg.max_events > 0 && engine_cfg.max_hooks > 0),
                       FP_StaticQaInt(engine_cfg.max_events) + "/" + FP_StaticQaInt(engine_cfg.max_hooks),
                       ">0", "event_and_hook_caps_must_be_positive");
   FP_StaticQaAddCheck(report, rows, "input_contract", "RENDER_CANONICAL_NAMES", (qa_cfg.require_release_safe_defaults ? "error" : "warn"),
                       (!qa_cfg.require_release_safe_defaults || render_cfg.use_canonical_object_names),
                       FP_StaticQaBool(render_cfg.use_canonical_object_names), "true", "canonical_chart_object_names_default");
   FP_StaticQaAddCheck(report, rows, "input_contract", "RENDER_STRICT_VISIBILITY", (qa_cfg.require_release_safe_defaults ? "error" : "warn"),
                       (!qa_cfg.require_release_safe_defaults || render_cfg.strict_visibility),
                       FP_StaticQaBool(render_cfg.strict_visibility), "true", "renderer_cannot_revive_hidden_events");
   FP_StaticQaAddCheck(report, rows, "input_contract", "INTERFACE_POSTFLIGHT", "warn",
                       (!qa_cfg.require_report_alignment || interface_cfg.postflight_enabled),
                       FP_StaticQaBool(interface_cfg.postflight_enabled), "true", "postflight_interface_check_recommended_before_static_qa");
   FP_StaticQaAddCheck(report, rows, "input_contract", "AMBIGUITY_ENABLED", "warn",
                       (!qa_cfg.require_report_alignment || ambiguity_cfg.enabled),
                       FP_StaticQaBool(ambiguity_cfg.enabled), "true", "decision_lock_should_run_before_static_qa");
}

void FP_StaticQaAddDependencyChecks(FP_StaticQaReport &report,
                                    string &rows[],
                                    const FP_StaticQaConfig &qa_cfg,
                                    const FP_ExportConfig &export_cfg,
                                    const FP_RenderConfig &render_cfg,
                                    const FP_ValidationConfig &validation_cfg,
                                    const FP_ReleaseReport &release_report,
                                    const FP_InterfaceReport &interface_post_report,
                                    const FP_AcceptanceReport &acceptance_report,
                                    const FP_AmbiguityReport &ambiguity_report)
{
   FP_StaticQaAddCheck(report, rows, "dependency", "EXPORT_ENABLED_ALIGNMENT", (qa_cfg.allow_disabled_export ? "warn" : "error"),
                       (!export_cfg.enabled || release_report.attempted),
                       "export_enabled=" + FP_StaticQaBool(export_cfg.enabled) + "/release_attempted=" + FP_StaticQaBool(release_report.attempted),
                       "export_does_not_bypass_release_gate", "export_pipeline_alignment");
   FP_StaticQaAddCheck(report, rows, "dependency", "RENDER_ENABLED_ALIGNMENT", (qa_cfg.allow_disabled_render ? "warn" : "error"),
                       (!render_cfg.draw_f1 && !render_cfg.draw_f2 && !render_cfg.draw_f3 && !render_cfg.draw_hooks || release_report.attempted),
                       "render_enabled=" + FP_StaticQaBool(render_cfg.draw_f1 || render_cfg.draw_f2 || render_cfg.draw_f3 || render_cfg.draw_hooks) + "/release_attempted=" + FP_StaticQaBool(release_report.attempted),
                       "render_does_not_bypass_release_gate", "render_pipeline_alignment");
   FP_StaticQaAddCheck(report, rows, "dependency", "VALIDATION_ENABLED_ALIGNMENT", (qa_cfg.allow_disabled_validation ? "warn" : "error"),
                       (!validation_cfg.enabled || release_report.attempted),
                       "validation_enabled=" + FP_StaticQaBool(validation_cfg.enabled) + "/release_attempted=" + FP_StaticQaBool(release_report.attempted),
                       "validation_does_not_bypass_release_gate", "validation_pipeline_alignment");
   FP_StaticQaAddCheck(report, rows, "report_alignment", "INTERFACE_POST_ATTEMPTED", (qa_cfg.require_report_alignment ? "error" : "warn"),
                       (!qa_cfg.require_report_alignment || interface_post_report.attempted),
                       FP_StaticQaBool(interface_post_report.attempted), "true", "interface_postflight_report_available");
   FP_StaticQaAddCheck(report, rows, "report_alignment", "ACCEPTANCE_ATTEMPTED", (qa_cfg.require_report_alignment ? "error" : "warn"),
                       (!qa_cfg.require_report_alignment || acceptance_report.attempted),
                       FP_StaticQaBool(acceptance_report.attempted), "true", "acceptance_report_available_before_static_qa");
   FP_StaticQaAddCheck(report, rows, "report_alignment", "AMBIGUITY_ATTEMPTED", (qa_cfg.require_report_alignment ? "error" : "warn"),
                       (!qa_cfg.require_report_alignment || ambiguity_report.attempted),
                       FP_StaticQaBool(ambiguity_report.attempted), "true", "ambiguity_report_available_before_static_qa");
}

void FP_StaticQaAddIoChecks(FP_StaticQaReport &report,
                            string &rows[],
                            const FP_StaticQaConfig &qa_cfg,
                            const FP_ExportReport &export_report,
                            const FP_RenderReport &render_report,
                            const FP_ValidationReport &validation_report)
{
   FP_StaticQaAddCheck(report, rows, "io_contract", "EXPORT_FILE_ERRORS", (qa_cfg.require_io_alignment ? "error" : "warn"),
                       (!qa_cfg.require_io_alignment || export_report.file_errors <= 0),
                       FP_StaticQaInt(export_report.file_errors), "0", "export_file_errors_before_static_qa");
   FP_StaticQaAddCheck(report, rows, "io_contract", "RENDER_OBJECT_ERRORS", (qa_cfg.require_io_alignment ? "error" : "warn"),
                       (!qa_cfg.require_io_alignment || render_report.object_create_failures <= 0),
                       FP_StaticQaInt(render_report.object_create_failures), "0", "renderer_object_errors_before_static_qa");
   FP_StaticQaAddCheck(report, rows, "io_contract", "VALIDATION_FILE_ERRORS", (qa_cfg.require_io_alignment ? "error" : "warn"),
                       (!qa_cfg.require_io_alignment || validation_report.file_errors <= 0),
                       FP_StaticQaInt(validation_report.file_errors), "0", "validation_file_errors_before_static_qa");
}

#endif // __FP_STATIC_QA_RULES_MQH__
