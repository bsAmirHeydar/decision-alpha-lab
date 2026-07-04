#ifndef __FP_HOOK_PHASE09_RULES_MQH__
#define __FP_HOOK_PHASE09_RULES_MQH__
#property strict

#include "FP_HookPhase09Types.mqh"

bool FP_HookP09ShouldRun(const FP_HookPhase09Config &cfg)
{
   if(!cfg.enabled)
      return false;
   if(cfg.display_family == FP_NDS_HOOK_DISPLAY_RALLY_ONLY && !cfg.allow_rally_only_smoke)
      return false;
   return true;
}

void FP_HookP09AddFinding(FP_HookPhase09Finding &rows[],
                          FP_HookPhase09Report &report,
                          const string code,
                          const FP_HookPhase09Severity severity,
                          const bool passed,
                          const string scope,
                          const string evidence,
                          const string recommendation)
{
   int n = ArraySize(rows);
   ArrayResize(rows, n+1);
   rows[n].check_code = code;
   rows[n].severity = severity;
   rows[n].passed = passed;
   rows[n].scope = scope;
   rows[n].evidence = evidence;
   rows[n].recommendation = recommendation;

   report.findings_total++;
   if(severity == FP_HOOK_P09_SEVERITY_INFO) report.info_count++;
   else if(severity == FP_HOOK_P09_SEVERITY_WARNING) report.warning_count++;
   else if(severity == FP_HOOK_P09_SEVERITY_BLOCKER) report.blocker_count++;

   if(passed) report.passed_count++;
   else report.failed_count++;
}

int FP_HookP09CountObjectsByPrefix(const string prefix)
{
   if(StringLen(prefix) <= 0)
      return 0;

   int count = 0;
   for(int i=ObjectsTotal(0, -1, -1)-1; i>=0; i--)
   {
      string name = ObjectName(0, i, -1, -1);
      if(StringFind(name, prefix) == 0)
         count++;
   }
   return count;
}

void FP_HookP09SetCensusRow(FP_HookPhase09ObjectCensusRow &row,
                            const string phase,
                            const string prefix,
                            const bool cfg_enabled,
                            const bool draw_surface_enabled,
                            const int expected_min_objects,
                            const int actual_objects,
                            const string reason)
{
   row.phase = phase;
   row.prefix = prefix;
   row.cfg_enabled = cfg_enabled;
   row.draw_surface_enabled = draw_surface_enabled;
   row.expected_min_objects = expected_min_objects;
   row.actual_objects = actual_objects;
   row.passed = (actual_objects >= expected_min_objects);
   row.reason = reason;
}

void FP_HookP09BuildObjectCensus(const FP_HookPhase01Config &p01_cfg,
                                 const FP_HookPhase02Config &p02_cfg,
                                 const FP_HookPhase03Config &p03_cfg,
                                 const FP_HookPhase04Config &p04_cfg,
                                 const FP_HookPhase05Config &p05_cfg,
                                 const FP_HookPhase06Config &p06_cfg,
                                 const FP_HookPhase07Config &p07_cfg,
                                 const FP_HookPhase08Config &p08_cfg,
                                 const FP_HookPhase09Config &p09_cfg,
                                 const FP_HookPhase01Report &p01_report,
                                 const FP_HookPhase02Report &p02_report,
                                 const FP_HookPhase03Report &p03_report,
                                 const FP_HookPhase04Report &p04_report,
                                 const FP_HookPhase05Report &p05_report,
                                 const FP_HookPhase06Report &p06_report,
                                 FP_HookPhase09ObjectCensusRow &rows[],
                                 FP_HookPhase09Report &report)
{
   ArrayResize(rows, 9);

   int p01_expected = (p01_cfg.enabled && p01_cfg.draw_nodes && p01_report.total_nodes > 0 ? 1 : 0);
   int p02_expected = (p02_cfg.enabled && p02_cfg.draw_sequences && p02_report.sequences_total > 0 ? 1 : 0);
   int p03_expected = (p03_cfg.enabled && p03_cfg.draw_y_extremes && p03_report.records_total > 0 ? 1 : 0);
   int p04_expected = (p04_cfg.enabled && (p04_cfg.draw_nd || p04_cfg.draw_death || p04_cfg.draw_x_closure) && p04_report.records_total > 0 ? 1 : 0);
   int p05_expected = (p05_cfg.enabled && (p05_cfg.draw_type_label || p05_cfg.draw_type_anchor) && p05_report.records_total > 0 ? 1 : 0);
   int p06_expected = (p06_cfg.enabled && (p06_cfg.draw_quality_label || p06_cfg.draw_xy_anchor) && p06_report.records_total > 0 ? 1 : 0);
   int p07_expected = 0;
   int p08_expected = 0;
   int p09_expected = (p09_cfg.draw_panel ? 1 : 0);

   FP_HookP09SetCensusRow(rows[0], "P01_NODE_SOURCE", p01_cfg.object_prefix, p01_cfg.enabled, p01_cfg.draw_nodes, p01_expected, FP_HookP09CountObjectsByPrefix(p01_cfg.object_prefix), "node-source draw surface");
   FP_HookP09SetCensusRow(rows[1], "P02_SEQUENCE", p02_cfg.object_prefix, p02_cfg.enabled, p02_cfg.draw_sequences, p02_expected, FP_HookP09CountObjectsByPrefix(p02_cfg.object_prefix), "x-sequence draw surface");
   FP_HookP09SetCensusRow(rows[2], "P03_Y_AXIS", p03_cfg.object_prefix, p03_cfg.enabled, p03_cfg.draw_y_extremes, p03_expected, FP_HookP09CountObjectsByPrefix(p03_cfg.object_prefix), "y-axis draw surface");
   FP_HookP09SetCensusRow(rows[3], "P04_LIFECYCLE", p04_cfg.object_prefix, p04_cfg.enabled, (p04_cfg.draw_nd || p04_cfg.draw_death || p04_cfg.draw_x_closure), p04_expected, FP_HookP09CountObjectsByPrefix(p04_cfg.object_prefix), "lifecycle draw surface");
   FP_HookP09SetCensusRow(rows[4], "P05_TYPE_ABC", p05_cfg.object_prefix, p05_cfg.enabled, (p05_cfg.draw_type_label || p05_cfg.draw_type_anchor), p05_expected, FP_HookP09CountObjectsByPrefix(p05_cfg.object_prefix), "type classifier draw surface");
   FP_HookP09SetCensusRow(rows[5], "P06_XY_QUALITY", p06_cfg.object_prefix, p06_cfg.enabled, (p06_cfg.draw_quality_label || p06_cfg.draw_xy_anchor), p06_expected, FP_HookP09CountObjectsByPrefix(p06_cfg.object_prefix), "quality-score draw surface");
   FP_HookP09SetCensusRow(rows[6], "P07_VIEW_PROFILE", p07_cfg.object_prefix, p07_cfg.enabled, false, p07_expected, FP_HookP09CountObjectsByPrefix(p07_cfg.object_prefix), "profile orchestration has no required draw surface");
   FP_HookP09SetCensusRow(rows[7], "P08_AUDIT", p08_cfg.object_prefix, p08_cfg.enabled, false, p08_expected, FP_HookP09CountObjectsByPrefix(p08_cfg.object_prefix), "audit layer should not draw objects");
   FP_HookP09SetCensusRow(rows[8], "P09_SMOKE", p09_cfg.object_prefix, p09_cfg.enabled, p09_cfg.draw_panel, p09_expected, FP_HookP09CountObjectsByPrefix(p09_cfg.object_prefix), "smoke panel draw surface");

   report.object_prefixes_checked = ArraySize(rows);
   report.object_prefixes_failed = 0;
   report.chart_hook_objects_seen = 0;
   for(int i=0; i<ArraySize(rows); i++)
   {
      report.chart_hook_objects_seen += rows[i].actual_objects;
      if(!rows[i].passed)
         report.object_prefixes_failed++;
   }
}

void FP_HookP09AddScenario(FP_HookPhase09ScenarioRow &rows[],
                           FP_HookPhase09Report &report,
                           const string code,
                           const string view_profile,
                           const bool required,
                           const int expected_min_objects,
                           const int actual_objects,
                           const int records_seen,
                           const string evidence,
                           const string recommendation)
{
   int n = ArraySize(rows);
   ArrayResize(rows, n+1);
   rows[n].scenario_code = code;
   rows[n].view_profile = view_profile;
   rows[n].required_for_current_profile = required;
   rows[n].expected_min_objects = expected_min_objects;
   rows[n].actual_objects = actual_objects;
   rows[n].records_seen = records_seen;
   rows[n].evidence = evidence;
   rows[n].recommendation = recommendation;

   if(!required)
   {
      rows[n].state = FP_HOOK_P09_SCENARIO_SKIPPED;
      rows[n].passed = true;
      report.scenarios_skipped++;
   }
   else if(actual_objects >= expected_min_objects)
   {
      rows[n].state = FP_HOOK_P09_SCENARIO_PASSED;
      rows[n].passed = true;
      report.scenarios_required++;
      report.scenarios_passed++;
   }
   else
   {
      rows[n].state = FP_HOOK_P09_SCENARIO_FAILED;
      rows[n].passed = false;
      report.scenarios_required++;
      report.scenarios_failed++;
   }
   report.scenarios_total++;
}

void FP_HookP09BuildCurrentProfileScenarios(const FP_HookPhase07Config &p07_cfg,
                                            const FP_HookPhase09ObjectCensusRow &census[],
                                            const FP_HookPhase01Report &p01_report,
                                            const FP_HookPhase02Report &p02_report,
                                            const FP_HookPhase03Report &p03_report,
                                            const FP_HookPhase04Report &p04_report,
                                            const FP_HookPhase05Report &p05_report,
                                            const FP_HookPhase06Report &p06_report,
                                            FP_HookPhase09ScenarioRow &rows[],
                                            FP_HookPhase09Report &report)
{
   ArrayResize(rows, 0);
   string vp = FP_HookP07ViewProfileName(p07_cfg.view_profile);

   int p01_obj = (ArraySize(census) > 0 ? census[0].actual_objects : 0);
   int p02_obj = (ArraySize(census) > 1 ? census[1].actual_objects : 0);
   int p03_obj = (ArraySize(census) > 2 ? census[2].actual_objects : 0);
   int p04_obj = (ArraySize(census) > 3 ? census[3].actual_objects : 0);
   int p05_obj = (ArraySize(census) > 4 ? census[4].actual_objects : 0);
   int p06_obj = (ArraySize(census) > 5 ? census[5].actual_objects : 0);

   bool raw_required = (p07_cfg.view_profile == FP_HOOK_P07_VIEW_RAW_NODES);
   bool sequence_required = (p07_cfg.view_profile == FP_HOOK_P07_VIEW_SEQUENCE_XY);
   bool lifecycle_required = (p07_cfg.view_profile == FP_HOOK_P07_VIEW_LIFECYCLE);
   bool type_required = (p07_cfg.view_profile == FP_HOOK_P07_VIEW_TYPE_QUALITY);
   bool quality_required = (p07_cfg.view_profile == FP_HOOK_P07_VIEW_QUALITY_FOCUS);
   bool full_required = (p07_cfg.view_profile == FP_HOOK_P07_VIEW_FULL_DEBUG);
   bool audit_only_required = (p07_cfg.view_profile == FP_HOOK_P07_VIEW_AUDIT_EXPORT_ONLY);

   FP_HookP09AddScenario(rows, report, "RAW_NODES_VISIBLE", vp,
                         raw_required || full_required,
                         (p01_report.total_nodes > 0 ? 1 : 0),
                         p01_obj,
                         p01_report.total_nodes,
                         "P01 object census must show node-source objects when raw nodes are requested",
                         "Enable P01 draw_nodes or reduce visual profile to audit/export only.");

   FP_HookP09AddScenario(rows, report, "SEQUENCE_XY_VISIBLE", vp,
                         sequence_required || full_required,
                         ((p02_report.sequences_total + p03_report.records_total) > 0 ? 1 : 0),
                         p02_obj + p03_obj,
                         p02_report.sequences_total + p03_report.records_total,
                         "P02/P03 object census must show X/Y sequence objects when sequence XY is requested",
                         "Enable P02/P03 drawing or check strict sequence input availability.");

   FP_HookP09AddScenario(rows, report, "LIFECYCLE_VISIBLE", vp,
                         lifecycle_required || full_required,
                         (p04_report.records_total > 0 ? 1 : 0),
                         p04_obj,
                         p04_report.records_total,
                         "P04 object census must show ND/death/X-closure objects when lifecycle is requested",
                         "Enable P04 lifecycle drawing or inspect Phase 04 record count.");

   FP_HookP09AddScenario(rows, report, "TYPE_QUALITY_VISIBLE", vp,
                         type_required || full_required,
                         ((p05_report.records_total + p06_report.records_total) > 0 ? 1 : 0),
                         p05_obj + p06_obj,
                         p05_report.records_total + p06_report.records_total,
                         "P05/P06 object census must show type and quality surfaces when type quality is requested",
                         "Enable P05/P06 drawing or inspect Hook Type/quality record counts.");

   FP_HookP09AddScenario(rows, report, "QUALITY_FOCUS_VISIBLE", vp,
                         quality_required,
                         (p06_report.records_total > 0 ? 1 : 0),
                         p06_obj,
                         p06_report.records_total,
                         "P06 object census must show quality-score objects when quality focus is requested",
                         "Enable P06 quality drawing or inspect Phase 06 quality records.");

   FP_HookP09AddScenario(rows, report, "AUDIT_EXPORT_ONLY_CLEAN", vp,
                         audit_only_required,
                         0,
                         p01_obj + p02_obj + p03_obj + p04_obj + p05_obj + p06_obj,
                         0,
                         "AUDIT_EXPORT_ONLY should not require chart drawing from P01 through P06",
                         "Turn off stale Hook drawings or run Phase 07 cleanup before audit-only smoke.");
}

void FP_HookP09CheckObjectCensus(const FP_HookPhase09Config &cfg,
                                 const FP_HookPhase09ObjectCensusRow &census[],
                                 FP_HookPhase09Finding &findings[],
                                 FP_HookPhase09Report &report)
{
   if(!cfg.require_object_census)
      return;

   for(int i=0; i<ArraySize(census); i++)
   {
      bool passed = census[i].passed;
      string evidence = "actual=" + IntegerToString(census[i].actual_objects) +
                        " expected_min=" + IntegerToString(census[i].expected_min_objects) +
                        " prefix=" + census[i].prefix;
      FP_HookP09AddFinding(findings, report, "OBJECT_CENSUS", (passed ? FP_HOOK_P09_SEVERITY_INFO : FP_HOOK_P09_SEVERITY_BLOCKER),
                           passed, census[i].phase, evidence,
                           "Use Phase 07 cleanup/profile controls and verify the selected visual profile.");
   }
}

void FP_HookP09CheckCurrentProfileCoverage(const FP_HookPhase09Config &cfg,
                                           const FP_HookPhase09ScenarioRow &scenarios[],
                                           FP_HookPhase09Finding &findings[],
                                           FP_HookPhase09Report &report)
{
   if(!cfg.require_current_profile_coverage)
      return;

   for(int i=0; i<ArraySize(scenarios); i++)
   {
      if(!scenarios[i].required_for_current_profile)
         continue;

      bool passed = scenarios[i].passed;
      string evidence = "actual_objects=" + IntegerToString(scenarios[i].actual_objects) +
                        " expected_min=" + IntegerToString(scenarios[i].expected_min_objects) +
                        " records_seen=" + IntegerToString(scenarios[i].records_seen);
      FP_HookP09AddFinding(findings, report, "PROFILE_SCENARIO_COVERAGE", (passed ? FP_HOOK_P09_SEVERITY_INFO : FP_HOOK_P09_SEVERITY_BLOCKER),
                           passed, scenarios[i].scenario_code, evidence, scenarios[i].recommendation);
   }
}

void FP_HookP09CheckAuditOnlyNoDraw(const FP_HookPhase09Config &cfg,
                                    const FP_HookPhase07Config &p07_cfg,
                                    const FP_HookPhase09ObjectCensusRow &census[],
                                    FP_HookPhase09Finding &findings[],
                                    FP_HookPhase09Report &report)
{
   if(!cfg.require_audit_only_no_hook_draw)
      return;
   if(p07_cfg.view_profile != FP_HOOK_P07_VIEW_AUDIT_EXPORT_ONLY)
      return;

   report.audit_only_checks++;
   int draw_objects = 0;
   for(int i=0; i<ArraySize(census) && i<6; i++)
      draw_objects += census[i].actual_objects;

   bool passed = (draw_objects <= 0);
   if(!passed)
   {
      report.audit_only_failed++;
   }
   FP_HookP09AddFinding(findings, report, "AUDIT_ONLY_NO_DRAW", (passed ? FP_HOOK_P09_SEVERITY_INFO : FP_HOOK_P09_SEVERITY_BLOCKER),
                        passed, "P07_AUDIT_EXPORT_ONLY", "p01_to_p06_objects=" + IntegerToString(draw_objects),
                        "Set InpHookPhase07CleanBeforeApply=true before switching to AUDIT_EXPORT_ONLY.");
}

void FP_HookP09CheckPhase08Ok(const FP_HookPhase09Config &cfg,
                              const FP_HookPhase08Report &p08_report,
                              FP_HookPhase09Finding &findings[],
                              FP_HookPhase09Report &report)
{
   report.phase08_attempted = (p08_report.attempted ? 1 : 0);
   report.phase08_ok = p08_report.ok;
   report.phase08_status = p08_report.status;
   report.phase08_reason = p08_report.reason;

   if(!cfg.require_phase08_ok)
      return;

   bool passed = p08_report.ok;
   FP_HookP09AddFinding(findings, report, "PHASE08_AUDIT_OK", (passed ? FP_HOOK_P09_SEVERITY_INFO : FP_HOOK_P09_SEVERITY_BLOCKER),
                        passed, "P08_AUDIT", "status=" + p08_report.status + " reason=" + p08_report.reason,
                        "Fix Phase 08 audit blockers before treating visual smoke as valid.");
}

void FP_HookP09CheckNoPhaseFileErrors(const FP_HookPhase09Config &cfg,
                                      const FP_HookPhase01Report &p01,
                                      const FP_HookPhase02Report &p02,
                                      const FP_HookPhase03Report &p03,
                                      const FP_HookPhase04Report &p04,
                                      const FP_HookPhase05Report &p05,
                                      const FP_HookPhase06Report &p06,
                                      const FP_HookPhase07Report &p07,
                                      const FP_HookPhase08Report &p08,
                                      FP_HookPhase09Finding &findings[],
                                      FP_HookPhase09Report &report)
{
   if(!cfg.require_no_phase_file_errors)
      return;

   int total_errors = p01.file_errors + p02.file_errors + p03.file_errors + p04.file_errors + p05.file_errors + p06.file_errors + p07.file_errors + p08.file_errors;
   report.phase_file_error_checks++;
   bool passed = (total_errors <= 0);
   if(!passed)
      report.phase_file_error_failed++;

   FP_HookP09AddFinding(findings, report, "NO_PHASE_FILE_ERRORS", (passed ? FP_HOOK_P09_SEVERITY_INFO : FP_HOOK_P09_SEVERITY_BLOCKER),
                        passed, "P01_TO_P08", "file_errors_total=" + IntegerToString(total_errors),
                        "Check Files folder permissions and export folder names before smoke-freeze.");
}

void FP_HookP09CheckDrawContract(const FP_HookPhase09Config &cfg,
                                 const FP_HookPhase09ObjectCensusRow &census[],
                                 FP_HookPhase09Finding &findings[],
                                 FP_HookPhase09Report &report)
{
   if(!cfg.require_draw_contract_when_records_exist)
      return;

   for(int i=0; i<ArraySize(census); i++)
   {
      if(!census[i].draw_surface_enabled || census[i].expected_min_objects <= 0)
         continue;

      report.draw_contract_checks++;
      bool passed = census[i].passed;
      if(!passed)
         report.draw_contract_failed++;
      FP_HookP09AddFinding(findings, report, "DRAW_CONTRACT_WHEN_RECORDS_EXIST", (passed ? FP_HOOK_P09_SEVERITY_INFO : FP_HOOK_P09_SEVERITY_BLOCKER),
                           passed, census[i].phase,
                           "expected_min=" + IntegerToString(census[i].expected_min_objects) + " actual=" + IntegerToString(census[i].actual_objects),
                           "A phase that has records and drawing enabled should leave at least one chart object.");
   }
}

void FP_HookP09CheckPanelContract(const FP_HookPhase09Config &cfg,
                                  const FP_HookPhase09ObjectCensusRow &census[],
                                  FP_HookPhase09Finding &findings[],
                                  FP_HookPhase09Report &report)
{
   if(!cfg.require_p09_panel_when_enabled || !cfg.draw_panel)
      return;

   int p09_objects = 0;
   if(ArraySize(census) > 8)
      p09_objects = census[8].actual_objects;
   bool passed = (p09_objects > 0 || report.p09_objects_created > 0);
   FP_HookP09AddFinding(findings, report, "P09_PANEL_OBJECT_EXISTS", (passed ? FP_HOOK_P09_SEVERITY_INFO : FP_HOOK_P09_SEVERITY_BLOCKER),
                        passed, "P09_SMOKE", "p09_objects=" + IntegerToString(p09_objects) + " created=" + IntegerToString(report.p09_objects_created),
                        "When draw_panel=true, Phase 09 should create a smoke status label.");
}

void FP_HookP09FinalizeReport(const FP_HookPhase09Config &cfg,
                              FP_HookPhase09Report &report)
{
   if(report.blocker_count > 0)
   {
      report.ok = false;
      report.status = "HOOK_P09_BLOCKED";
      report.reason = "SMOKE_BLOCKERS=" + IntegerToString(report.blocker_count);
      return;
   }

   if(report.warning_count > cfg.max_warnings_allowed)
   {
      report.ok = false;
      report.status = "HOOK_P09_WARNING_LIMIT_FAILED";
      report.reason = "WARNINGS=" + IntegerToString(report.warning_count) + " MAX=" + IntegerToString(cfg.max_warnings_allowed);
      return;
   }

   report.ok = true;
   report.status = "HOOK_P09_SMOKE_OK";
   report.reason = "VISUAL_SMOKE_RECONCILED";
}

void FP_PrintHookPhase09Report(const string tag, const FP_HookPhase09Report &r)
{
   Print(tag,
         " status=", r.status,
         " ok=", FP_HookP09BoolName(r.ok),
         " reason=", r.reason,
         " display_family=", FP_HookP01DisplayFamilyName(r.display_family),
         " view_profile=", FP_HookP07ViewProfileName(r.view_profile),
         " scenarios=", r.scenarios_total,
         " required=", r.scenarios_required,
         " passed=", r.scenarios_passed,
         " failed=", r.scenarios_failed,
         " hook_objects=", r.chart_hook_objects_seen,
         " findings=", r.findings_total,
         " blockers=", r.blocker_count,
         " warnings=", r.warning_count,
         " files=", r.files_written,
         " file_errors=", r.file_errors);
}

void FP_PrintHookPhase09Findings(const string tag,
                                 const FP_HookPhase09Finding &findings[],
                                 const int limit)
{
   int max_rows = limit;
   if(max_rows <= 0 || max_rows > ArraySize(findings))
      max_rows = ArraySize(findings);
   for(int i=0; i<max_rows; i++)
   {
      Print(tag,
            " finding[", i, "] code=", findings[i].check_code,
            " severity=", FP_HookP09SeverityName(findings[i].severity),
            " passed=", FP_HookP09BoolName(findings[i].passed),
            " scope=", findings[i].scope,
            " evidence=", findings[i].evidence,
            " recommendation=", findings[i].recommendation);
   }
}

#endif // __FP_HOOK_PHASE09_RULES_MQH__
