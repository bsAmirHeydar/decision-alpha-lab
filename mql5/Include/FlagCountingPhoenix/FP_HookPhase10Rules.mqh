#ifndef __FP_HOOK_PHASE10_RULES_MQH__
#define __FP_HOOK_PHASE10_RULES_MQH__
#property strict

#include "FP_HookPhase10Types.mqh"

bool FP_HookP10ShouldRun(const FP_HookPhase10Config &cfg)
{
   if(!cfg.enabled)
      return false;
   if(cfg.display_family == FP_NDS_HOOK_DISPLAY_RALLY_ONLY && !cfg.allow_rally_only_freeze)
      return false;
   return true;
}

string FP_HookP10BuildContractId(const string symbol,
                                 const ENUM_TIMEFRAMES period,
                                 const FP_HookPhase10Config &cfg,
                                 const FP_HookPhase07Config &p07_cfg)
{
   string id = "HOOK_V1";
   id += "_" + symbol;
   id += "_" + EnumToString(period);
   id += "_" + FP_HookP01DisplayFamilyName(cfg.display_family);
   id += "_" + FP_HookP07ViewProfileName(p07_cfg.view_profile);
   id += "_" + FP_HookP10FreezeModeName(cfg.freeze_mode);
   return id;
}

void FP_HookP10AddContract(FP_HookPhase10ContractRow &rows[],
                           FP_HookPhase10Report &report,
                           const string code,
                           const FP_HookPhase10Severity severity,
                           const bool required,
                           const bool passed,
                           const string evidence,
                           const string recommendation)
{
   int n = ArraySize(rows);
   ArrayResize(rows, n+1);
   rows[n].contract_code = code;
   rows[n].severity = severity;
   rows[n].required = required;
   rows[n].passed = passed;
   rows[n].state = (passed ? FP_HOOK_P10_CONTRACT_PASSED : FP_HOOK_P10_CONTRACT_FAILED);
   rows[n].evidence = evidence;
   rows[n].recommendation = recommendation;

   report.contract_checks_total++;
   if(required) report.contract_checks_required++;
   if(passed) report.contract_checks_passed++;
   else report.contract_checks_failed++;
   if(required && !passed) report.failed_required_count++;

   if(severity == FP_HOOK_P10_SEVERITY_INFO)
      report.info_count++;
   else if(severity == FP_HOOK_P10_SEVERITY_WARNING && !passed)
      report.warning_count++;
   else if(severity == FP_HOOK_P10_SEVERITY_BLOCKER && !passed)
      report.blocker_count++;
}

void FP_HookP10AddSkippedContract(FP_HookPhase10ContractRow &rows[],
                                  FP_HookPhase10Report &report,
                                  const string code,
                                  const FP_HookPhase10Severity severity,
                                  const bool required,
                                  const string evidence,
                                  const string recommendation)
{
   int n = ArraySize(rows);
   ArrayResize(rows, n+1);
   rows[n].contract_code = code;
   rows[n].severity = severity;
   rows[n].required = required;
   rows[n].passed = true;
   rows[n].state = FP_HOOK_P10_CONTRACT_SKIPPED;
   rows[n].evidence = evidence;
   rows[n].recommendation = recommendation;

   report.contract_checks_total++;
   report.contract_checks_skipped++;
   if(required) report.contract_checks_required++;
   if(severity == FP_HOOK_P10_SEVERITY_INFO)
      report.info_count++;
   else if(severity == FP_HOOK_P10_SEVERITY_WARNING && required)
      report.warning_count++;
   else if(severity == FP_HOOK_P10_SEVERITY_BLOCKER && required)
      report.blocker_count++;
}

void FP_HookP10AddSchema(FP_HookPhase10TrainingSchemaRow &rows[],
                         const string column_name,
                         const string source_phase,
                         const bool required,
                         const string semantic_type,
                         const string description)
{
   int n = ArraySize(rows);
   ArrayResize(rows, n+1);
   rows[n].column_name = column_name;
   rows[n].source_phase = source_phase;
   rows[n].required = required;
   rows[n].semantic_type = semantic_type;
   rows[n].description = description;
}

void FP_HookP10BuildTrainingSchema(FP_HookPhase10TrainingSchemaRow &schema[],
                                   FP_HookPhase10Report &report)
{
   ArrayResize(schema, 0);

   FP_HookP10AddSchema(schema, "contract_id", "P10", true, "identifier", "Stable identifier for this freeze contract run.");
   FP_HookP10AddSchema(schema, "schema_version", "P10", true, "schema", "Training contract schema version.");
   FP_HookP10AddSchema(schema, "symbol", "runtime", true, "market", "MT5 chart symbol.");
   FP_HookP10AddSchema(schema, "period", "runtime", true, "timeframe", "MT5 chart timeframe.");
   FP_HookP10AddSchema(schema, "display_family", "P01-P10", true, "config", "RALLY_ONLY, HOOK_ONLY, or RALLY_AND_HOOK.");
   FP_HookP10AddSchema(schema, "view_profile", "P07", true, "config", "Visual profile used to produce the Hook evidence layer.");
   FP_HookP10AddSchema(schema, "direction", "P02-P06", true, "categorical", "Positive or negative Hook sequence direction.");
   FP_HookP10AddSchema(schema, "scale", "P01-P06", true, "integer", "Swing/fractal scale used by the source node model.");
   FP_HookP10AddSchema(schema, "sequence_id", "P02-P06", true, "identifier", "Internal sequence identifier.");
   FP_HookP10AddSchema(schema, "origin_time", "P02", true, "datetime", "Origin timestamp of the CycleHook sequence.");
   FP_HookP10AddSchema(schema, "origin_price", "P02", true, "price", "Origin price of the CycleHook sequence.");
   FP_HookP10AddSchema(schema, "x0_time", "P02", true, "datetime", "First X-axis node timestamp.");
   FP_HookP10AddSchema(schema, "x0_price", "P02", true, "price", "First X-axis node price.");
   FP_HookP10AddSchema(schema, "x1_time", "P02", false, "datetime", "Second X-axis node timestamp when available.");
   FP_HookP10AddSchema(schema, "x1_price", "P02", false, "price", "Second X-axis node price when available.");
   FP_HookP10AddSchema(schema, "x2_time", "P02", false, "datetime", "Third X-axis node timestamp when available.");
   FP_HookP10AddSchema(schema, "x2_price", "P02", false, "price", "Third X-axis node price when available.");
   FP_HookP10AddSchema(schema, "x3_time", "P02", false, "datetime", "Fourth X-axis node timestamp when available.");
   FP_HookP10AddSchema(schema, "x3_price", "P02", false, "price", "Fourth X-axis node price when available.");
   FP_HookP10AddSchema(schema, "y_state", "P06", true, "categorical", "Internal Y-sequence closure state.");
   FP_HookP10AddSchema(schema, "xy_state", "P06", true, "categorical", "Combined X/Y closure state.");
   FP_HookP10AddSchema(schema, "hook_type", "P05", true, "categorical", "Hook Type A/B/C classifier output.");
   FP_HookP10AddSchema(schema, "quality_bucket", "P06", true, "categorical", "ELITE/HIGH/MEDIUM/LOW/INVALID Hook quality bucket.");
   FP_HookP10AddSchema(schema, "quality_score", "P06", true, "float", "Composite structural quality score.");
   FP_HookP10AddSchema(schema, "x_strength", "P06", true, "float", "X closure strength component.");
   FP_HookP10AddSchema(schema, "y_strength", "P06", true, "float", "Y closure strength component.");
   FP_HookP10AddSchema(schema, "type_strength", "P06", true, "float", "Hook Type A/B/C strength component.");
   FP_HookP10AddSchema(schema, "lifecycle_strength", "P06", true, "float", "Lifecycle/ND/death consistency strength component.");
   FP_HookP10AddSchema(schema, "dead_by_origin_return", "P04-P06", true, "boolean", "Whether the sequence died by origin-return logic.");
   FP_HookP10AddSchema(schema, "anchor_time", "P06", false, "datetime", "Quality anchor timestamp.");
   FP_HookP10AddSchema(schema, "anchor_price", "P06", false, "price", "Quality anchor price.");
   FP_HookP10AddSchema(schema, "record_reason", "P06", false, "text", "Human-readable reason attached to the record.");

   report.training_schema_columns = ArraySize(schema);
}

void FP_HookP10EvaluateContract(const FP_HookPhase10Config &cfg,
                                const FP_HookPhase07Config &p07_cfg,
                                const FP_HookPhase08Report &p08_report,
                                const FP_HookPhase09Report &p09_report,
                                const FP_HookPhase06Report &p06_report,
                                FP_HookPhase10ContractRow &contracts[],
                                FP_HookPhase10Report &report)
{
   ArrayResize(contracts, 0);

   report.phase08_ok = p08_report.ok;
   report.phase08_status = p08_report.status;
   report.phase08_reason = p08_report.reason;
   report.phase09_ok = p09_report.ok;
   report.phase09_status = p09_report.status;
   report.phase09_reason = p09_report.reason;

   report.p06_records_total = p06_report.records_total;
   report.p06_xy_closed_count = p06_report.xy_closed_count;
   report.p06_elite_count = p06_report.elite_count;
   report.p06_high_count = p06_report.high_count;
   report.p06_medium_count = p06_report.medium_count;
   report.p06_low_count = p06_report.low_count;
   report.p06_invalid_count = p06_report.invalid_count;
   report.p06_high_or_elite_count = p06_report.elite_count + p06_report.high_count;

   bool display_ok = (cfg.display_family == FP_NDS_HOOK_DISPLAY_HOOK_ONLY ||
                      cfg.display_family == FP_NDS_HOOK_DISPLAY_RALLY_AND_HOOK ||
                      cfg.allow_rally_only_freeze);
   FP_HookP10AddContract(contracts, report,
                         "DISPLAY_FAMILY_VISIBLE_FIRST_INPUT",
                         FP_HOOK_P10_SEVERITY_BLOCKER,
                         true,
                         display_ok,
                         "display_family=" + FP_HookP01DisplayFamilyName(cfg.display_family),
                         "Use HOOK_ONLY to inspect Hook cleanly or RALLY_AND_HOOK to inspect Rally and Hook together. RALLY_ONLY is legacy-safe and skipped unless explicitly allowed.");

   FP_HookP10AddContract(contracts, report,
                         "PHASE08_AUDIT_RECONCILED",
                         FP_HOOK_P10_SEVERITY_BLOCKER,
                         cfg.require_phase08_ok,
                         (!cfg.require_phase08_ok || p08_report.ok),
                         "p08_ok=" + FP_HookP10BoolName(p08_report.ok) + " status=" + p08_report.status + " reason=" + p08_report.reason,
                         "Phase 08 must pass before freezing the Hook object contract.");

   FP_HookP10AddContract(contracts, report,
                         "PHASE09_VISUAL_SMOKE_RECONCILED",
                         FP_HOOK_P10_SEVERITY_BLOCKER,
                         cfg.require_phase09_ok,
                         (!cfg.require_phase09_ok || p09_report.ok),
                         "p09_ok=" + FP_HookP10BoolName(p09_report.ok) + " status=" + p09_report.status + " reason=" + p09_report.reason,
                         "Phase 09 must pass before freezing the Hook visual/data contract.");

   FP_HookP10AddContract(contracts, report,
                         "HOOK_RECORDS_EXIST",
                         FP_HOOK_P10_SEVERITY_BLOCKER,
                         cfg.require_hook_records,
                         (!cfg.require_hook_records || p06_report.records_total >= cfg.min_p06_records_total),
                         "p06_records_total=" + IntegerToString(p06_report.records_total) + " min=" + IntegerToString(cfg.min_p06_records_total),
                         "Run in HOOK_ONLY or RALLY_AND_HOOK and select enough bars/scales so Phase 06 has records.");

   FP_HookP10AddContract(contracts, report,
                         "XY_QUALITY_RECORDS_EXIST",
                         FP_HOOK_P10_SEVERITY_BLOCKER,
                         cfg.require_xy_quality_records,
                         (!cfg.require_xy_quality_records || p06_report.xy_closed_count >= cfg.min_xy_closed_records),
                         "xy_closed=" + IntegerToString(p06_report.xy_closed_count) + " min=" + IntegerToString(cfg.min_xy_closed_records),
                         "For a strict training set, increase bars/scales or lower min_xy_closed_records only after manual inspection.");

   FP_HookP10AddContract(contracts, report,
                         "HIGH_OR_ELITE_QUALITY_AVAILABLE",
                         FP_HOOK_P10_SEVERITY_WARNING,
                         cfg.require_high_quality_records,
                         (!cfg.require_high_quality_records || report.p06_high_or_elite_count >= cfg.min_high_or_elite_records),
                         "high_or_elite=" + IntegerToString(report.p06_high_or_elite_count) + " min=" + IntegerToString(cfg.min_high_or_elite_records),
                         "Keep this optional until quality thresholds are empirically calibrated.");

   FP_HookP10AddContract(contracts, report,
                         "VIEW_PROFILE_EXPLICIT",
                         FP_HOOK_P10_SEVERITY_WARNING,
                         cfg.require_view_profile_not_keep_inputs,
                         (!cfg.require_view_profile_not_keep_inputs || p07_cfg.view_profile != FP_HOOK_P07_VIEW_KEEP_INPUTS),
                         "view_profile=" + FP_HookP07ViewProfileName(p07_cfg.view_profile),
                         "Use QUALITY_FOCUS, TYPE_QUALITY, FULL_DEBUG, or AUDIT_EXPORT_ONLY when producing a reproducible freeze run.");

   bool file_ok = true;
   if(p06_report.file_errors > 0) file_ok = false;
   if(p08_report.file_errors > 0) file_ok = false;
   if(p09_report.file_errors > 0) file_ok = false;
   FP_HookP10AddContract(contracts, report,
                         "NO_UPSTREAM_FILE_ERRORS",
                         FP_HOOK_P10_SEVERITY_BLOCKER,
                         cfg.require_no_file_errors,
                         (!cfg.require_no_file_errors || file_ok),
                         "p06_file_errors=" + IntegerToString(p06_report.file_errors) +
                         " p08_file_errors=" + IntegerToString(p08_report.file_errors) +
                         " p09_file_errors=" + IntegerToString(p09_report.file_errors),
                         "Fix upstream export path, folder permission, or file-handle errors before freezing.");

   bool export_contract_ok = (!cfg.require_export_contract || cfg.export_csv);
   FP_HookP10AddContract(contracts, report,
                         "P10_EXPORT_CONTRACT_ENABLED",
                         FP_HOOK_P10_SEVERITY_BLOCKER,
                         cfg.require_export_contract,
                         export_contract_ok,
                         "p10_export_csv=" + FP_HookP10BoolName(cfg.export_csv),
                         "Enable Phase 10 CSV export when the freeze contract must be reproducible outside the chart.");

   if(cfg.freeze_mode == FP_HOOK_P10_FREEZE_OBSERVE_ONLY)
   {
      FP_HookP10AddSkippedContract(contracts, report,
                                   "STRICT_LOCK_NOT_REQUESTED",
                                   FP_HOOK_P10_SEVERITY_INFO,
                                   false,
                                   "freeze_mode=OBSERVE_ONLY",
                                   "No lock is asserted in observe-only mode.");
   }
   else if(cfg.freeze_mode == FP_HOOK_P10_FREEZE_STRICT_LOCK)
   {
      bool strict_ok = (p08_report.ok && p09_report.ok && p06_report.records_total >= cfg.min_p06_records_total &&
                        p06_report.xy_closed_count >= cfg.min_xy_closed_records && file_ok && display_ok);
      FP_HookP10AddContract(contracts, report,
                            "STRICT_LOCK_GATE",
                            FP_HOOK_P10_SEVERITY_BLOCKER,
                            true,
                            strict_ok,
                            "strict_ok=" + FP_HookP10BoolName(strict_ok),
                            "Strict lock requires clean audit, clean smoke, visible Hook display-family, records, and no upstream file errors.");
   }
}

void FP_HookP10FinalizeReport(const FP_HookPhase10Config &cfg,
                              FP_HookPhase10Report &report)
{
   bool warnings_ok = (report.warning_count <= cfg.max_warnings_allowed);
   bool blockers_ok = (report.failed_required_count <= 0);
   report.freeze_ready = (blockers_ok && warnings_ok && report.file_errors <= 0);
   report.ok = report.freeze_ready;

   if(report.ok)
   {
      report.status = "HOOK_P10_FREEZE_READY";
      report.reason = "FREEZE_CONTRACT_RECONCILED";
   }
   else
   {
      report.status = "HOOK_P10_FREEZE_BLOCKED";
      if(!blockers_ok)
         report.reason = "REQUIRED_CONTRACT_CHECK_FAILED";
      else if(!warnings_ok)
         report.reason = "WARNING_LIMIT_EXCEEDED";
      else
         report.reason = "PHASE10_FILE_ERROR";
   }
}

void FP_PrintHookPhase10Report(const string prefix,
                               const FP_HookPhase10Report &r)
{
   Print(prefix,
         " status=", r.status,
         " ok=", FP_HookP10BoolName(r.ok),
         " ready=", FP_HookP10BoolName(r.freeze_ready),
         " reason=", r.reason,
         " contract_id=", r.contract_id,
         " display_family=", FP_HookP01DisplayFamilyName(r.display_family),
         " view_profile=", FP_HookP07ViewProfileName(r.view_profile),
         " mode=", FP_HookP10FreezeModeName(r.freeze_mode),
         " checks=", r.contract_checks_passed, "/", r.contract_checks_total,
         " failed_required=", r.failed_required_count,
         " warnings=", r.warning_count,
         " blockers=", r.blocker_count,
         " p06_records=", r.p06_records_total,
         " xy_closed=", r.p06_xy_closed_count,
         " high_or_elite=", r.p06_high_or_elite_count,
         " files=", r.files_written,
         " file_errors=", r.file_errors);
}

void FP_PrintHookPhase10Contracts(const string prefix,
                                  const FP_HookPhase10ContractRow &rows[],
                                  const int limit)
{
   int n = ArraySize(rows);
   int m = limit;
   if(m <= 0 || m > n) m = n;
   for(int i=0; i<m; i++)
   {
      Print(prefix,
            " contract[", i, "] code=", rows[i].contract_code,
            " severity=", FP_HookP10SeverityName(rows[i].severity),
            " required=", FP_HookP10BoolName(rows[i].required),
            " state=", FP_HookP10ContractStateName(rows[i].state),
            " passed=", FP_HookP10BoolName(rows[i].passed),
            " evidence=", rows[i].evidence);
   }
}

#endif // __FP_HOOK_PHASE10_RULES_MQH__
