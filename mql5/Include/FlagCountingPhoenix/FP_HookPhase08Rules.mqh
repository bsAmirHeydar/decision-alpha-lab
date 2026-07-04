#ifndef __FP_HOOK_PHASE08_RULES_MQH__
#define __FP_HOOK_PHASE08_RULES_MQH__
#property strict

#include "FP_HookPhase08Types.mqh"

bool FP_HookP08ShouldRun(const FP_HookPhase08Config &cfg)
{
   if(!cfg.enabled)
      return false;
   if(cfg.display_family == FP_NDS_HOOK_DISPLAY_RALLY_ONLY && !cfg.allow_rally_only_audit)
      return false;
   return true;
}

void FP_HookP08AddFinding(FP_HookPhase08Finding &findings[],
                          FP_HookPhase08Report &report,
                          const string check_code,
                          const FP_HookPhase08Severity severity,
                          const bool passed,
                          const string phase,
                          const string evidence,
                          const string recommendation)
{
   int n = ArraySize(findings);
   ArrayResize(findings, n + 1);
   findings[n].check_code = check_code;
   findings[n].severity = severity;
   findings[n].passed = passed;
   findings[n].phase = phase;
   findings[n].evidence = evidence;
   findings[n].recommendation = recommendation;

   report.findings_total++;
   if(passed)
      report.passed_count++;
   else
      report.failed_count++;

   if(severity == FP_HOOK_P08_SEVERITY_INFO)
      report.info_count++;
   else if(severity == FP_HOOK_P08_SEVERITY_WARNING)
      report.warning_count++;
   else if(severity == FP_HOOK_P08_SEVERITY_BLOCKER)
      report.blocker_count++;
}

void FP_HookP08AddPhaseRow(FP_HookPhase08PhaseRow &rows[],
                           const string phase,
                           const bool cfg_enabled,
                           const bool attempted,
                           const bool ok,
                           const string status,
                           const string reason,
                           const bool export_enabled,
                           const int files_written,
                           const int file_errors,
                           const int records_seen,
                           const int positive_seen,
                           const int negative_seen,
                           const int objects_created,
                           const int objects_deleted,
                           const int drawn_seen)
{
   int n = ArraySize(rows);
   ArrayResize(rows, n + 1);
   rows[n].phase = phase;
   rows[n].cfg_enabled = cfg_enabled;
   rows[n].attempted = attempted;
   rows[n].ok = ok;
   rows[n].status = status;
   rows[n].reason = reason;
   rows[n].export_enabled = export_enabled;
   rows[n].files_written = files_written;
   rows[n].file_errors = file_errors;
   rows[n].records_seen = records_seen;
   rows[n].positive_seen = positive_seen;
   rows[n].negative_seen = negative_seen;
   rows[n].objects_created = objects_created;
   rows[n].objects_deleted = objects_deleted;
   rows[n].drawn_seen = drawn_seen;
}

void FP_HookP08BuildPhaseMatrix(const FP_HookPhase01Config &p01_cfg,
                                const FP_HookPhase02Config &p02_cfg,
                                const FP_HookPhase03Config &p03_cfg,
                                const FP_HookPhase04Config &p04_cfg,
                                const FP_HookPhase05Config &p05_cfg,
                                const FP_HookPhase06Config &p06_cfg,
                                const FP_HookPhase07Config &p07_cfg,
                                const FP_HookPhase01Report &p01,
                                const FP_HookPhase02Report &p02,
                                const FP_HookPhase03Report &p03,
                                const FP_HookPhase04Report &p04,
                                const FP_HookPhase05Report &p05,
                                const FP_HookPhase06Report &p06,
                                const FP_HookPhase07Report &p07,
                                FP_HookPhase08PhaseRow &rows[],
                                FP_HookPhase08Report &report)
{
   ArrayResize(rows, 0);

   FP_HookP08AddPhaseRow(rows, "P01_NODE_SOURCE", p01_cfg.enabled, p01.attempted, p01.ok, p01.status, p01.reason, p01_cfg.export_csv, p01.files_written, p01.file_errors, p01.total_nodes, p01.peak_nodes, p01.valley_nodes, p01.objects_created, p01.objects_deleted, p01.nodes_drawn);
   FP_HookP08AddPhaseRow(rows, "P02_SEQUENCE_BUILDER", p02_cfg.enabled, p02.attempted, p02.ok, p02.status, p02.reason, p02_cfg.export_csv, p02.files_written, p02.file_errors, p02.sequences_total, p02.sequences_positive, p02.sequences_negative, p02.objects_created, p02.objects_deleted, p02.sequences_drawn);
   FP_HookP08AddPhaseRow(rows, "P03_Y_AXIS", p03_cfg.enabled, p03.attempted, p03.ok, p03.status, p03.reason, p03_cfg.export_csv, p03.files_written, p03.file_errors, p03.records_total, p03.records_positive, p03.records_negative, p03.objects_created, p03.objects_deleted, p03.records_drawn);
   FP_HookP08AddPhaseRow(rows, "P04_LIFECYCLE", p04_cfg.enabled, p04.attempted, p04.ok, p04.status, p04.reason, p04_cfg.export_csv, p04.files_written, p04.file_errors, p04.records_total, p04.records_positive, p04.records_negative, p04.objects_created, p04.objects_deleted, p04.records_drawn);
   FP_HookP08AddPhaseRow(rows, "P05_TYPE_ABC", p05_cfg.enabled, p05.attempted, p05.ok, p05.status, p05.reason, p05_cfg.export_csv, p05.files_written, p05.file_errors, p05.records_total, p05.records_positive, p05.records_negative, p05.objects_created, p05.objects_deleted, p05.records_drawn);
   FP_HookP08AddPhaseRow(rows, "P06_XY_QUALITY", p06_cfg.enabled, p06.attempted, p06.ok, p06.status, p06.reason, p06_cfg.export_csv, p06.files_written, p06.file_errors, p06.records_total, p06.records_positive, p06.records_negative, p06.objects_created, p06.objects_deleted, p06.records_drawn);
   FP_HookP08AddPhaseRow(rows, "P07_VIEW_PROFILE", p07_cfg.enabled, p07.attempted, p07.ok, p07.status, p07.reason, p07_cfg.export_profile_csv, p07.files_written, p07.file_errors, p07.profiles_applied, 0, 0, 0, p07.objects_deleted, 0);

   report.phases_total = ArraySize(rows);
   report.phases_enabled = 0;
   report.phases_attempted = 0;
   report.phases_ok = 0;
   report.phases_failed = 0;

   for(int i=0; i<ArraySize(rows); i++)
   {
      if(rows[i].cfg_enabled)
         report.phases_enabled++;
      if(rows[i].attempted)
         report.phases_attempted++;
      if(rows[i].ok)
         report.phases_ok++;
      if(rows[i].attempted && !rows[i].ok)
         report.phases_failed++;
   }
}

string FP_HookP08CountEvidence(const string left_name,
                               const int left_value,
                               const string right_name,
                               const int right_value)
{
   return left_name + "=" + IntegerToString(left_value) + ";" + right_name + "=" + IntegerToString(right_value);
}

void FP_HookP08CheckRuntimeReports(const FP_HookPhase08Config &cfg,
                                   const FP_HookPhase08PhaseRow &rows[],
                                   FP_HookPhase08Finding &findings[],
                                   FP_HookPhase08Report &report)
{
   if(!cfg.require_runtime_report_ok)
      return;

   for(int i=0; i<ArraySize(rows); i++)
   {
      if(!rows[i].cfg_enabled)
         continue;

      bool passed = (rows[i].attempted && rows[i].ok);
      report.runtime_checks++;
      if(!passed)
         report.runtime_failed++;

      FP_HookP08AddFinding(findings, report, "RUNTIME_REPORT_OK", FP_HOOK_P08_SEVERITY_BLOCKER, passed,
                           rows[i].phase,
                           "enabled=" + FP_HookP08BoolName(rows[i].cfg_enabled) + ";attempted=" + FP_HookP08BoolName(rows[i].attempted) + ";ok=" + FP_HookP08BoolName(rows[i].ok) + ";status=" + rows[i].status,
                           "Inspect the phase status/reason and rerun before using Hook records as training input.");
   }
}

void FP_HookP08CheckNonnegativeCounts(const FP_HookPhase08Config &cfg,
                                      const FP_HookPhase08PhaseRow &rows[],
                                      FP_HookPhase08Finding &findings[],
                                      FP_HookPhase08Report &report)
{
   if(!cfg.require_nonnegative_counts)
      return;

   for(int i=0; i<ArraySize(rows); i++)
   {
      bool passed = (rows[i].files_written >= 0 && rows[i].file_errors >= 0 && rows[i].records_seen >= 0 && rows[i].positive_seen >= 0 && rows[i].negative_seen >= 0 && rows[i].objects_created >= 0 && rows[i].objects_deleted >= 0 && rows[i].drawn_seen >= 0);
      FP_HookP08AddFinding(findings, report, "NONNEGATIVE_COUNTS", FP_HOOK_P08_SEVERITY_BLOCKER, passed,
                           rows[i].phase,
                           "records=" + IntegerToString(rows[i].records_seen) + ";files=" + IntegerToString(rows[i].files_written) + ";errors=" + IntegerToString(rows[i].file_errors) + ";drawn=" + IntegerToString(rows[i].drawn_seen),
                           "Negative counters indicate corrupted report accounting and must be fixed before audit release.");
   }
}

void FP_HookP08CheckNoFileErrors(const FP_HookPhase08Config &cfg,
                                 const FP_HookPhase08PhaseRow &rows[],
                                 FP_HookPhase08Finding &findings[],
                                 FP_HookPhase08Report &report)
{
   if(!cfg.require_no_file_errors)
      return;

   for(int i=0; i<ArraySize(rows); i++)
   {
      if(!rows[i].export_enabled)
         continue;

      bool passed = (rows[i].file_errors == 0);
      report.export_checks++;
      if(!passed)
         report.export_failed++;

      FP_HookP08AddFinding(findings, report, "CSV_FILE_ERRORS_ZERO", FP_HOOK_P08_SEVERITY_BLOCKER, passed,
                           rows[i].phase,
                           "export_enabled=true;files_written=" + IntegerToString(rows[i].files_written) + ";file_errors=" + IntegerToString(rows[i].file_errors),
                           "Check MQL5 Files permissions, folder path, and concurrent file locks.");
   }
}

void FP_HookP08CheckExportProfileAlignment(const FP_HookPhase08Config &cfg,
                                           const FP_HookPhase07Config &p07_cfg,
                                           const FP_HookPhase07Report &p07,
                                           FP_HookPhase08Finding &findings[],
                                           FP_HookPhase08Report &report)
{
   if(!cfg.require_audit_export_profile_alignment)
      return;

   bool audit_profile = (p07_cfg.view_profile == FP_HOOK_P07_VIEW_AUDIT_EXPORT_ONLY);
   bool any_export = (p07.p01_export || p07.p02_export || p07.p03_export || p07.p04_export || p07.p05_export || p07.p06_export || p07_cfg.export_profile_csv || cfg.export_csv);
   bool passed = (!audit_profile || any_export);

   report.export_checks++;
   if(!passed)
      report.export_failed++;

   FP_HookP08AddFinding(findings, report, "AUDIT_PROFILE_EXPORT_ALIGNMENT", FP_HOOK_P08_SEVERITY_WARNING, passed,
                        "P07_VIEW_PROFILE",
                        "view_profile=" + FP_HookP07ViewProfileName(p07_cfg.view_profile) + ";any_export=" + FP_HookP08BoolName(any_export),
                        "When using AUDIT_EXPORT_ONLY, enable at least one Hook CSV export or Phase 08 export_csv.");
}

void FP_HookP08CheckChainAlignment(const FP_HookPhase08Config &cfg,
                                   const FP_HookPhase02Report &p02,
                                   const FP_HookPhase03Report &p03,
                                   const FP_HookPhase04Report &p04,
                                   const FP_HookPhase05Report &p05,
                                   const FP_HookPhase06Report &p06,
                                   FP_HookPhase08Finding &findings[],
                                   FP_HookPhase08Report &report)
{
   if(!cfg.require_phase_chain_alignment)
      return;

   bool pass_03 = (p03.phase02_sequences_seen == p02.sequences_total);
   report.chain_checks++;
   if(pass_03) report.chain_passed++; else report.chain_failed++;
   FP_HookP08AddFinding(findings, report, "CHAIN_P03_SEES_P02", FP_HOOK_P08_SEVERITY_BLOCKER, pass_03,
                        "P03_Y_AXIS",
                        FP_HookP08CountEvidence("p03.phase02_sequences_seen", p03.phase02_sequences_seen, "p02.sequences_total", p02.sequences_total),
                        "Phase 03 must rebuild/consume the same sequence universe emitted by Phase 02.");

   bool pass_04 = (p04.phase03_records_seen == p03.records_total);
   report.chain_checks++;
   if(pass_04) report.chain_passed++; else report.chain_failed++;
   FP_HookP08AddFinding(findings, report, "CHAIN_P04_SEES_P03", FP_HOOK_P08_SEVERITY_BLOCKER, pass_04,
                        "P04_LIFECYCLE",
                        FP_HookP08CountEvidence("p04.phase03_records_seen", p04.phase03_records_seen, "p03.records_total", p03.records_total),
                        "Phase 04 lifecycle records must match Phase 03 X/Y records.");

   bool pass_05 = (p05.phase04_records_seen == p04.records_total);
   report.chain_checks++;
   if(pass_05) report.chain_passed++; else report.chain_failed++;
   FP_HookP08AddFinding(findings, report, "CHAIN_P05_SEES_P04", FP_HOOK_P08_SEVERITY_BLOCKER, pass_05,
                        "P05_TYPE_ABC",
                        FP_HookP08CountEvidence("p05.phase04_records_seen", p05.phase04_records_seen, "p04.records_total", p04.records_total),
                        "Phase 05 Type A/B/C classifier must consume the same lifecycle set from Phase 04.");

   bool pass_06 = (p06.phase05_records_seen == p05.records_total);
   report.chain_checks++;
   if(pass_06) report.chain_passed++; else report.chain_failed++;
   FP_HookP08AddFinding(findings, report, "CHAIN_P06_SEES_P05", FP_HOOK_P08_SEVERITY_BLOCKER, pass_06,
                        "P06_XY_QUALITY",
                        FP_HookP08CountEvidence("p06.phase05_records_seen", p06.phase05_records_seen, "p05.records_total", p05.records_total),
                        "Phase 06 quality scoring must consume the same classified set from Phase 05.");
}

bool FP_HookP08PrefixDuplicate(const string a, const string b)
{
   return (StringLen(a) > 0 && StringLen(b) > 0 && a == b);
}

void FP_HookP08CheckPrefixPair(const string left_phase,
                               const string left_prefix,
                               const string right_phase,
                               const string right_prefix,
                               FP_HookPhase08Finding &findings[],
                               FP_HookPhase08Report &report)
{
   bool passed = !FP_HookP08PrefixDuplicate(left_prefix, right_prefix);
   report.prefix_checks++;
   if(!passed)
      report.prefix_failed++;

   FP_HookP08AddFinding(findings, report, "UNIQUE_OBJECT_PREFIX", FP_HOOK_P08_SEVERITY_BLOCKER, passed,
                        left_phase + "/" + right_phase,
                        "left_prefix=" + left_prefix + ";right_prefix=" + right_prefix,
                        "Each Hook phase must keep a unique object_prefix so cleanup never deletes another phase by accident.");
}

void FP_HookP08CheckUniquePrefixes(const FP_HookPhase08Config &cfg,
                                   const FP_HookPhase01Config &p01_cfg,
                                   const FP_HookPhase02Config &p02_cfg,
                                   const FP_HookPhase03Config &p03_cfg,
                                   const FP_HookPhase04Config &p04_cfg,
                                   const FP_HookPhase05Config &p05_cfg,
                                   const FP_HookPhase06Config &p06_cfg,
                                   const FP_HookPhase07Config &p07_cfg,
                                   FP_HookPhase08Finding &findings[],
                                   FP_HookPhase08Report &report)
{
   if(!cfg.require_unique_object_prefixes)
      return;

   string names[8];
   string prefixes[8];

   names[0] = "P01"; prefixes[0] = p01_cfg.object_prefix;
   names[1] = "P02"; prefixes[1] = p02_cfg.object_prefix;
   names[2] = "P03"; prefixes[2] = p03_cfg.object_prefix;
   names[3] = "P04"; prefixes[3] = p04_cfg.object_prefix;
   names[4] = "P05"; prefixes[4] = p05_cfg.object_prefix;
   names[5] = "P06"; prefixes[5] = p06_cfg.object_prefix;
   names[6] = "P07"; prefixes[6] = p07_cfg.object_prefix;
   names[7] = "P08"; prefixes[7] = cfg.object_prefix;

   for(int i=0; i<8; i++)
   {
      bool nonempty = (StringLen(prefixes[i]) > 0);
      report.prefix_checks++;
      if(!nonempty)
         report.prefix_failed++;
      FP_HookP08AddFinding(findings, report, "OBJECT_PREFIX_NONEMPTY", FP_HOOK_P08_SEVERITY_BLOCKER, nonempty,
                           names[i],
                           "prefix=" + prefixes[i],
                           "Set a non-empty object_prefix for every Hook phase.");
   }

   for(int i=0; i<8; i++)
   {
      for(int j=i+1; j<8; j++)
         FP_HookP08CheckPrefixPair(names[i], prefixes[i], names[j], prefixes[j], findings, report);
   }
}

void FP_HookP08CheckP06QualityAudit(const FP_HookPhase08Config &cfg,
                                    const FP_HookPhase06Report &p06,
                                    FP_HookPhase08Finding &findings[],
                                    FP_HookPhase08Report &report)
{
   if(!cfg.require_p06_records_for_quality_audit)
      return;

   bool passed = (p06.records_total > 0);
   FP_HookP08AddFinding(findings, report, "P06_RECORDS_AVAILABLE", FP_HOOK_P08_SEVERITY_WARNING, passed,
                        "P06_XY_QUALITY",
                        "p06.records_total=" + IntegerToString(p06.records_total) + ";xy_closed=" + IntegerToString(p06.xy_closed_count),
                        "If no Phase 06 records exist, expand scan window, lower minimum X requirements, or inspect Phase 01 node source.");
}

void FP_HookP08FillQualitySnapshot(const FP_HookPhase06Report &p06,
                                   FP_HookPhase08Report &report)
{
   report.p06_records_total = p06.records_total;
   report.p06_xy_closed_count = p06.xy_closed_count;
   report.p06_elite_count = p06.elite_count;
   report.p06_high_count = p06.high_count;
   report.p06_medium_count = p06.medium_count;
   report.p06_low_count = p06.low_count;
   report.p06_invalid_count = p06.invalid_count;
}

void FP_HookP08FinalizeReport(const FP_HookPhase08Config &cfg,
                              FP_HookPhase08Report &report)
{
   bool no_blockers = (report.blocker_count == 0);
   bool warnings_allowed = (report.warning_count <= cfg.max_warnings_allowed);
   bool no_file_errors = (report.file_errors == 0);

   report.ok = (no_blockers && warnings_allowed && no_file_errors);

   if(report.ok)
   {
      report.status = "HOOK_P08_OK";
      report.reason = "HOOK_AUDIT_RECONCILED";
   }
   else if(!no_blockers)
   {
      report.status = "HOOK_P08_BLOCKED";
      report.reason = "BLOCKER_FINDINGS_PRESENT";
   }
   else if(!warnings_allowed)
   {
      report.status = "HOOK_P08_WARNINGS_EXCEEDED";
      report.reason = "WARNING_COUNT_EXCEEDS_LIMIT";
   }
   else
   {
      report.status = "HOOK_P08_FILE_ERROR";
      report.reason = "PHASE08_EXPORT_FILE_ERROR";
   }
}

void FP_PrintHookPhase08Report(const string tag,
                               const FP_HookPhase08Report &r)
{
   Print(tag,
         " status=", r.status,
         " ok=", FP_HookP08BoolName(r.ok),
         " reason=", r.reason,
         " family=", FP_HookP01DisplayFamilyName(r.display_family),
         " profile=", FP_HookP07ViewProfileName(r.view_profile),
         " phases=", r.phases_total,
         " enabled=", r.phases_enabled,
         " attempted=", r.phases_attempted,
         " failed=", r.phases_failed,
         " findings=", r.findings_total,
         " blockers=", r.blocker_count,
         " warnings=", r.warning_count,
         " chain_failed=", r.chain_failed,
         " prefix_failed=", r.prefix_failed,
         " runtime_failed=", r.runtime_failed,
         " export_failed=", r.export_failed,
         " p06_records=", r.p06_records_total,
         " xy_closed=", r.p06_xy_closed_count,
         " files=", r.files_written,
         " file_errors=", r.file_errors);
}

void FP_PrintHookPhase08Findings(const string tag,
                                 const FP_HookPhase08Finding &findings[],
                                 const int limit)
{
   int n = ArraySize(findings);
   int lim = limit;
   if(lim <= 0 || lim > n)
      lim = n;

   for(int i=0; i<lim; i++)
   {
      if(findings[i].passed)
         continue;
      Print(tag,
            " sample=", i,
            " severity=", FP_HookP08SeverityName(findings[i].severity),
            " check=", findings[i].check_code,
            " phase=", findings[i].phase,
            " evidence=", findings[i].evidence,
            " recommendation=", findings[i].recommendation);
   }
}

#endif // __FP_HOOK_PHASE08_RULES_MQH__
