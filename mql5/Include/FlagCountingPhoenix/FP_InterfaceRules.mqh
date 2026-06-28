#ifndef __FP_INTERFACE_RULES_MQH__
#define __FP_INTERFACE_RULES_MQH__
#property strict

#include "FP_InterfaceTypes.mqh"

// ============================================================================
// Phoenix Level 15 - Pure Interface Rules
// ============================================================================

string FP_InterfaceStatus(const bool pass, const string severity)
{
   if(pass) return "PASS";
   if(severity == "warn") return "WARN";
   if(severity == "skip") return "SKIP";
   return "FAIL";
}

void FP_InterfaceCsvAppend(string &line, const string value)
{
   string v = value;
   StringReplace(v, "\"", "\"\"");
   if(line != "") line += ",";
   line += "\"" + v + "\"";
}

string FP_InterfaceHeader()
{
   string line = "";
   FP_InterfaceCsvAppend(line, "run_id");
   FP_InterfaceCsvAppend(line, "stage");
   FP_InterfaceCsvAppend(line, "check_id");
   FP_InterfaceCsvAppend(line, "category");
   FP_InterfaceCsvAppend(line, "severity");
   FP_InterfaceCsvAppend(line, "status");
   FP_InterfaceCsvAppend(line, "actual");
   FP_InterfaceCsvAppend(line, "expected");
   FP_InterfaceCsvAppend(line, "reason");
   return line;
}

void FP_InterfaceCountCategory(FP_InterfaceReport &report, const string category)
{
   if(category == "facade") report.facade_checks++;
   else if(category == "config") report.config_checks++;
   else if(category == "enum") report.enum_checks++;
   else if(category == "dependency") report.dependency_checks++;
   else if(category == "result") report.result_checks++;
   else if(category == "parent") report.parent_checks++;
   else if(category == "identity") report.id_checks++;
}

void FP_InterfaceAddCheck(FP_InterfaceReport &report,
                          string &rows[],
                          const string check_id,
                          const string category,
                          const string severity,
                          const bool pass,
                          const string actual,
                          const string expected,
                          const string reason)
{
   report.checks_total++;
   FP_InterfaceCountCategory(report, category);
   string status = FP_InterfaceStatus(pass, severity);
   if(status == "PASS") report.checks_passed++;
   else if(status == "WARN") report.checks_warned++;
   else if(status == "SKIP") report.checks_skipped++;
   else report.checks_failed++;

   string line = "";
   FP_InterfaceCsvAppend(line, report.run_id);
   FP_InterfaceCsvAppend(line, report.stage);
   FP_InterfaceCsvAppend(line, check_id);
   FP_InterfaceCsvAppend(line, category);
   FP_InterfaceCsvAppend(line, severity);
   FP_InterfaceCsvAppend(line, status);
   FP_InterfaceCsvAppend(line, actual);
   FP_InterfaceCsvAppend(line, expected);
   FP_InterfaceCsvAppend(line, reason);
   int n = ArraySize(rows);
   ArrayResize(rows, n + 1);
   rows[n] = line;
}

bool FP_InterfaceNonEmpty(const string s)
{
   return (StringLen(s) > 0);
}

bool FP_InterfaceNonNegative(const int v)
{
   return (v >= 0);
}

bool FP_InterfacePositiveOrZero(const double v)
{
   return (v >= 0.0);
}

bool FP_InterfaceRatioPositive(const double v)
{
   return (v > 0.0);
}

bool FP_InterfaceEventHasPublicId(const FP_FlagEvent &e)
{
   return (e.structural_id != "" && e.visual_id != "" && e.phase_id != "" && e.chain_id != "" && e.audit_id != "");
}

bool FP_InterfaceHookHasPublicId(const FP_HookBranch &h)
{
   return (h.structural_id != "" && h.visual_id != "" && h.phase_id != "" && h.audit_id != "");
}

int FP_InterfaceFindEventById(const FP_FlagEvent &events[], const int event_id)
{
   for(int i=0; i<ArraySize(events); i++)
      if(events[i].event_id == event_id) return i;
   return -1;
}

bool FP_InterfaceVisibleParentOk(const FP_FlagEvent &events[], const FP_FlagEvent &e)
{
   if(!e.visible_main) return true;
   if(e.level == FP_LEVEL_F1 || e.parent_event_id < 0) return true;
   int p = FP_InterfaceFindEventById(events, e.parent_event_id);
   if(p < 0) return false;
   return events[p].visible_main;
}

void FP_InterfaceAddEnumChecks(FP_InterfaceReport &report, string &rows[])
{
   FP_InterfaceAddCheck(report, rows, "ENUM_F_LEVELS", "enum", "error",
                        (FP_LEVEL_F1 == 1 && FP_LEVEL_F2 == 2 && FP_LEVEL_F3 == 3 && FP_LEVEL_ND == 10),
                        FP_InterfaceInt(FP_LEVEL_F1) + "/" + FP_InterfaceInt(FP_LEVEL_F2) + "/" + FP_InterfaceInt(FP_LEVEL_F3) + "/" + FP_InterfaceInt(FP_LEVEL_ND),
                        "1/2/3/10", "level_enum_contract");
   FP_InterfaceAddCheck(report, rows, "ENUM_DIRECTION", "enum", "error",
                        (FP_DIR_BULLISH == 1 && FP_DIR_BEARISH == -1 && FP_DIR_NONE == 0),
                        FP_InterfaceInt(FP_DIR_BULLISH) + "/" + FP_InterfaceInt(FP_DIR_BEARISH) + "/" + FP_InterfaceInt(FP_DIR_NONE),
                        "1/-1/0", "direction_enum_contract");
   FP_InterfaceAddCheck(report, rows, "ENUM_NODE_KIND", "enum", "error",
                        (FP_NODE_HIGH == 1 && FP_NODE_LOW == -1 && FP_NODE_NONE == 0),
                        FP_InterfaceInt(FP_NODE_HIGH) + "/" + FP_InterfaceInt(FP_NODE_LOW) + "/" + FP_InterfaceInt(FP_NODE_NONE),
                        "1/-1/0", "node_kind_enum_contract");
   FP_InterfaceAddCheck(report, rows, "CONST_INTERNAL_MAX", "enum", "error",
                        (FP_MAX_INTERNAL_NODES == 4),
                        FP_InterfaceInt(FP_MAX_INTERNAL_NODES), "4", "internal_count_contract");
   FP_InterfaceAddCheck(report, rows, "CONST_INTERFACE_VERSION", "enum", "error",
                        (FP_INTERFACE_CONTRACT_VERSION == "16.00"),
                        FP_INTERFACE_CONTRACT_VERSION, "16.00", "interface_contract_version");
}

void FP_InterfaceAddFacadeChecks(FP_InterfaceReport &report, string &rows[], const FP_Config &engine_cfg)
{
   FP_InterfaceAddCheck(report, rows, "FACADE_PUBLIC_COUNT", "facade", "error",
                        (FP_INTERFACE_PUBLIC_FACADE_COUNT >= 16),
                        FP_InterfaceInt(FP_INTERFACE_PUBLIC_FACADE_COUNT), ">=16", "public_facade_registry_count");
   FP_InterfaceAddCheck(report, rows, "FACADE_IDENTITY_PASS", "facade", "error",
                        (engine_cfg.identity_generation_pass == "phoenix_level16"),
                        engine_cfg.identity_generation_pass, "phoenix_level16", "identity_generation_pass_must_match_level16");
   FP_InterfaceAddCheck(report, rows, "FACADE_CONTEXT_SYMBOL", "facade", "error",
                        FP_InterfaceNonEmpty(engine_cfg.context_symbol),
                        engine_cfg.context_symbol, "non_empty", "engine_context_symbol_required");
   FP_InterfaceAddCheck(report, rows, "FACADE_CONTEXT_TIMEFRAME", "facade", "error",
                        FP_InterfaceNonEmpty(engine_cfg.context_timeframe),
                        engine_cfg.context_timeframe, "non_empty", "engine_context_timeframe_required");
}

void FP_InterfaceAddConfigChecks(FP_InterfaceReport &report,
                                 string &rows[],
                                 const FP_TimebaseConfig &timebase_cfg,
                                 const FP_Config &engine_cfg,
                                 const FP_ExportConfig &export_cfg,
                                 const FP_RenderConfig &render_cfg,
                                 const FP_ValidationConfig &validation_cfg,
                                 const FP_ReleaseConfig &release_cfg,
                                 const FP_InterfaceConfig &interface_cfg)
{
   FP_InterfaceAddCheck(report, rows, "CFG_TIMEBASE_BARS", "config", "error",
                        (timebase_cfg.requested_bars > 0 && timebase_cfg.min_closed_bars >= 0),
                        FP_InterfaceInt(timebase_cfg.requested_bars) + "/" + FP_InterfaceInt(timebase_cfg.min_closed_bars),
                        "requested>0/min>=0", "timebase_bar_bounds");
   FP_InterfaceAddCheck(report, rows, "CFG_ENGINE_CAPS", "config", "error",
                        (engine_cfg.max_events >= 0 && engine_cfg.max_hooks >= 0),
                        FP_InterfaceInt(engine_cfg.max_events) + "/" + FP_InterfaceInt(engine_cfg.max_hooks),
                        "max_events>=0/max_hooks>=0", "engine_caps_nonnegative");
   FP_InterfaceAddCheck(report, rows, "CFG_RATIOS", "config", "error",
                        (FP_InterfaceRatioPositive(engine_cfg.f2_min_parent_size_ratio) && FP_InterfaceRatioPositive(engine_cfg.f3_min_parent_size_ratio) && FP_InterfaceRatioPositive(engine_cfg.f3_leg1_L_min_ratio) && FP_InterfaceRatioPositive(engine_cfg.nd_min_retrace_ratio)),
                        DoubleToString(engine_cfg.f2_min_parent_size_ratio, 4) + "/" + DoubleToString(engine_cfg.f3_min_parent_size_ratio, 4) + "/" + DoubleToString(engine_cfg.f3_leg1_L_min_ratio, 4) + "/" + DoubleToString(engine_cfg.nd_min_retrace_ratio, 4),
                        ">0/>0/>0/>0", "ratio_contract");
   FP_InterfaceAddCheck(report, rows, "CFG_EPSILON", "config", "error",
                        FP_InterfacePositiveOrZero(engine_cfg.boundary_epsilon_points),
                        DoubleToString(engine_cfg.boundary_epsilon_points, 4), ">=0", "epsilon_nonnegative");
   FP_InterfaceAddCheck(report, rows, "CFG_EXPORT_FOLDER", "config", "error",
                        (!export_cfg.enabled || FP_InterfaceNonEmpty(export_cfg.folder)),
                        export_cfg.folder, "non_empty_when_export_enabled", "export_folder_contract");
   FP_InterfaceAddCheck(report, rows, "CFG_RENDER_PREFIX", "config", "error",
                        FP_InterfaceNonEmpty(render_cfg.prefix),
                        render_cfg.prefix, "non_empty", "renderer_prefix_contract");
   FP_InterfaceAddCheck(report, rows, "CFG_RENDER_LIMITS", "config", "error",
                        (render_cfg.max_events_to_draw >= 0 && render_cfg.max_hooks_to_draw >= 0 && render_cfg.curve_segments >= 1 && render_cfg.label_font_size >= 1),
                        FP_InterfaceInt(render_cfg.max_events_to_draw) + "/" + FP_InterfaceInt(render_cfg.max_hooks_to_draw) + "/" + FP_InterfaceInt(render_cfg.curve_segments) + "/" + FP_InterfaceInt(render_cfg.label_font_size),
                        "draw_limits>=0/curve>=1/font>=1", "renderer_limit_contract");
   FP_InterfaceAddCheck(report, rows, "CFG_VALIDATION_FOLDER", "config", "error",
                        (!validation_cfg.enabled || FP_InterfaceNonEmpty(validation_cfg.folder)),
                        validation_cfg.folder, "non_empty_when_validation_enabled", "validation_folder_contract");
   FP_InterfaceAddCheck(report, rows, "CFG_RELEASE_FOLDER", "config", "error",
                        (!release_cfg.write_manifest || FP_InterfaceNonEmpty(release_cfg.folder)),
                        release_cfg.folder, "non_empty_when_manifest_enabled", "release_folder_contract");
   FP_InterfaceAddCheck(report, rows, "CFG_INTERFACE_FOLDER", "config", "error",
                        (!interface_cfg.write_csv || FP_InterfaceNonEmpty(interface_cfg.folder)),
                        interface_cfg.folder, "non_empty_when_interface_csv_enabled", "interface_folder_contract");
}

void FP_InterfaceAddDependencyChecks(FP_InterfaceReport &report,
                                     string &rows[],
                                     const FP_ExportConfig &export_cfg,
                                     const FP_RenderConfig &render_cfg,
                                     const FP_ValidationConfig &validation_cfg,
                                     const FP_ReleaseConfig &release_cfg)
{
   FP_InterfaceAddCheck(report, rows, "DEP_RENDER_CANON_NAMES", "dependency", "warn",
                        render_cfg.use_canonical_object_names,
                        FP_InterfaceBool(render_cfg.use_canonical_object_names), "true", "renderer_should_use_canonical_identity");
   FP_InterfaceAddCheck(report, rows, "DEP_RENDER_STRICT_VIS", "dependency", "warn",
                        render_cfg.strict_visibility,
                        FP_InterfaceBool(render_cfg.strict_visibility), "true", "renderer_should_obey_engine_visibility");
   FP_InterfaceAddCheck(report, rows, "DEP_VALIDATION_EXPORT", "dependency", "warn",
                        (!validation_cfg.enabled || export_cfg.enabled || !validation_cfg.require_export_ok),
                        "validation=" + FP_InterfaceBool(validation_cfg.enabled) + "/export=" + FP_InterfaceBool(export_cfg.enabled) + "/require_export=" + FP_InterfaceBool(validation_cfg.require_export_ok),
                        "export_enabled_when_validation_requires_export", "validation_export_dependency");
   FP_InterfaceAddCheck(report, rows, "DEP_RELEASE_VALIDATION", "dependency", "warn",
                        (!release_cfg.require_validation_ok || validation_cfg.enabled),
                        "require_validation=" + FP_InterfaceBool(release_cfg.require_validation_ok) + "/validation=" + FP_InterfaceBool(validation_cfg.enabled),
                        "validation_enabled_when_release_requires_validation", "release_validation_dependency");
}

void FP_InterfaceAddResultChecks(FP_InterfaceReport &report,
                                 string &rows[],
                                 const FP_InterfaceConfig &cfg,
                                 const FP_FlagEvent &events[],
                                 const FP_HookBranch &hooks[],
                                 const FP_DetectResult &result)
{
   int visible_events = 0;
   int hidden_events = 0;
   int f1 = 0;
   int f2 = 0;
   int f3 = 0;
   int missing_ids = 0;
   int parent_errors = 0;
   for(int i=0; i<ArraySize(events); i++)
   {
      if(events[i].visible_main) visible_events++; else hidden_events++;
      if(events[i].level == FP_LEVEL_F1) f1++;
      else if(events[i].level == FP_LEVEL_F2) f2++;
      else if(events[i].level == FP_LEVEL_F3) f3++;
      if(cfg.require_public_ids && !FP_InterfaceEventHasPublicId(events[i])) missing_ids++;
      if(cfg.require_parent_contract && !FP_InterfaceVisibleParentOk(events, events[i])) parent_errors++;
   }

   int missing_hook_ids = 0;
   for(int h=0; h<ArraySize(hooks); h++)
      if(cfg.require_public_ids && !FP_InterfaceHookHasPublicId(hooks[h])) missing_hook_ids++;

   report.missing_public_ids += missing_ids + missing_hook_ids;
   report.visible_child_parent_errors += parent_errors;
   if(visible_events + hidden_events != ArraySize(events)) report.partition_errors++;
   if(result.visible_events_total + result.hidden_events_total != result.events_total) report.partition_errors++;

   FP_InterfaceAddCheck(report, rows, "RES_EVENT_ARRAY_PARTITION", "result", "error",
                        (!cfg.require_result_partition || visible_events + hidden_events == ArraySize(events)),
                        FP_InterfaceInt(visible_events) + "+" + FP_InterfaceInt(hidden_events) + "=" + FP_InterfaceInt(visible_events + hidden_events),
                        FP_InterfaceInt(ArraySize(events)), "event_array_partition");
   FP_InterfaceAddCheck(report, rows, "RES_RESULT_PARTITION", "result", "error",
                        (!cfg.require_result_partition || result.visible_events_total + result.hidden_events_total == result.events_total),
                        FP_InterfaceInt(result.visible_events_total) + "+" + FP_InterfaceInt(result.hidden_events_total) + "=" + FP_InterfaceInt(result.visible_events_total + result.hidden_events_total),
                        FP_InterfaceInt(result.events_total), "detect_result_partition");
   FP_InterfaceAddCheck(report, rows, "RES_LEVEL_COUNT", "result", "warn",
                        (f1 + f2 + f3 <= ArraySize(events)),
                        FP_InterfaceInt(f1) + "+" + FP_InterfaceInt(f2) + "+" + FP_InterfaceInt(f3),
                        "<=events", "event_level_count_contract");
   FP_InterfaceAddCheck(report, rows, "ID_EVENT_PUBLIC", "identity", "error",
                        (!cfg.require_public_ids || missing_ids == 0),
                        FP_InterfaceInt(missing_ids), "0", "events_have_public_interface_ids");
   FP_InterfaceAddCheck(report, rows, "ID_HOOK_PUBLIC", "identity", "warn",
                        (!cfg.require_public_ids || missing_hook_ids == 0),
                        FP_InterfaceInt(missing_hook_ids), "0", "hooks_have_public_interface_ids");
   FP_InterfaceAddCheck(report, rows, "PARENT_VISIBLE_CHAIN", "parent", "error",
                        (!cfg.require_parent_contract || parent_errors == 0),
                        FP_InterfaceInt(parent_errors), "0", "visible_f2_f3_parent_chain_contract");
}

void FP_InterfaceAddCounterChecks(FP_InterfaceReport &report,
                                  string &rows[],
                                  const FP_InterfaceConfig &cfg,
                                  const FP_DetectResult &result)
{
   int neg = 0;
   if(result.raw_nodes_total < 0) neg++;
   if(result.nodes_total < 0) neg++;
   if(result.hooks_total < 0) neg++;
   if(result.events_total < 0) neg++;
   if(result.render_object_errors_total < 0) neg++;
   if(result.export_file_errors_total < 0) neg++;
   if(result.validation_file_errors_total < 0) neg++;
   if(result.release_file_errors_total < 0) neg++;
   report.negative_counter_errors += neg;
   FP_InterfaceAddCheck(report, rows, "RES_COUNTERS_NONNEG", "result", "error",
                        (!cfg.require_counter_nonnegative || neg == 0),
                        FP_InterfaceInt(neg), "0", "detect_result_negative_counter_contract");
}

#endif // __FP_INTERFACE_RULES_MQH__
