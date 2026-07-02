#ifndef __FP_BROKER_REQUEST_AUDIT_ENGINE_MQH__
#define __FP_BROKER_REQUEST_AUDIT_ENGINE_MQH__
#property strict

#include "FP_BrokerRequestAuditExport.mqh"

// Consolidation Patch 01 latest-row cache. Read-only diagnostic cache.
bool g_fp_c01_has_l28_audit_row = false;
FP_Level28BrokerRequestAuditRow g_fp_c01_l28_audit_row;

void FP_RunLevel28BrokerRequestAudit(const string symbol,
                                     const ENUM_TIMEFRAMES period,
                                     const MqlRates &rates[],
                                     const int bars,
                                     const FP_FlagEvent &events[],
                                     const FP_HookBranch &hooks[],
                                     const FP_TimebaseReport &timebase_report,
                                     const FP_RenderReport &render_report,
                                     const FP_ValidationReport &validation_report,
                                     const bool license_ok,
                                     const FP_Level20EntryBridgeConfig &entry_bridge_cfg,
                                     const FP_Level21PaperIntentConfig &intent_cfg,
                                     const FP_Level24SafetyGateConfig &safety_cfg,
                                     const FP_Level25BrokerDryRunConfig &dry_run_cfg,
                                     const FP_Level26BrokerValidatorConfig &validator_cfg,
                                     const FP_Level28BrokerRequestAuditConfig &cfg,
                                     FP_Level28BrokerRequestAuditReport &report)
{
   FP_ResetLevel28BrokerRequestAuditReport(report);
   report.attempted = cfg.enabled;
   g_fp_c01_has_l28_audit_row = false;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "LEVEL28_BROKER_REQUEST_AUDIT_DISABLED";
      report.reason = "InpLevel28BrokerRequestAuditEnabled_false";
      return;
   }

   FP_Level21PaperIntentRow intent_row;
   FP_Level24SafetyGateRow safety_row;
   FP_Level25BrokerDryRunRow dry_run_row;
   FP_Level26BrokerValidatorRow validator_row;

   if(g_fp_c01_has_l21_paper_intent_row &&
      g_fp_c01_has_l24_safety_gate_row &&
      g_fp_c01_has_l25_dry_run_row &&
      g_fp_c01_has_l26_validator_row)
   {
      intent_row = g_fp_c01_l21_paper_intent_row;
      safety_row = g_fp_c01_l24_safety_gate_row;
      dry_run_row = g_fp_c01_l25_dry_run_row;
      validator_row = g_fp_c01_l26_validator_row;
   }
   else
   {
      FP_Level20EntryBridgeRow bridge_row;
      FP_L20BuildEntryBridgeRow(symbol, period, rates, bars, events, hooks,
                                timebase_report, render_report, validation_report,
                                entry_bridge_cfg, bridge_row);
      g_fp_c01_l20_entry_bridge_row = bridge_row;
      g_fp_c01_has_l20_entry_bridge_row = true;

      FP_L21FillFromEntryBridge(intent_cfg, bridge_row, intent_row);
      g_fp_c01_l21_paper_intent_row = intent_row;
      g_fp_c01_has_l21_paper_intent_row = true;

      FP_L24BuildSafetyGateRow(symbol, period, license_ok, safety_cfg, safety_row);
      g_fp_c01_l24_safety_gate_row = safety_row;
      g_fp_c01_has_l24_safety_gate_row = true;

      FP_L25BuildBrokerDryRunRow(symbol, period, safety_row, intent_row, dry_run_cfg, dry_run_row);
      g_fp_c01_l25_dry_run_row = dry_run_row;
      g_fp_c01_has_l25_dry_run_row = true;

      FP_L26BuildBrokerValidatorRow(symbol, period, dry_run_row, validator_cfg, validator_row);
      g_fp_c01_l26_validator_row = validator_row;
      g_fp_c01_has_l26_validator_row = true;
   }

   FP_Level28BrokerRequestAuditRow row;
   FP_L28BuildBrokerRequestAuditRow(symbol, period, safety_row, intent_row,
                                    dry_run_row, validator_row, cfg, row);

   row.latest_written = (cfg.export_csv && cfg.write_latest_csv);
   row.audit_written = (cfg.export_csv && cfg.append_audit_csv && !row.duplicate_skipped);

   bool latest_ok = FP_L28WriteLatestBrokerRequestAudit(cfg, row, report);
   bool audit_ok = FP_L28AppendBrokerRequestAudit(cfg, row, report);

   g_fp_c01_l28_audit_row = row;
   g_fp_c01_has_l28_audit_row = true;

   report.ok = (latest_ok && audit_ok && report.file_errors == 0);
   report.status = row.audit_status;
   report.reason = row.audit_block_reason;
}

void FP_PrintLevel28BrokerRequestAuditReport(const string tag,
                                             const FP_Level28BrokerRequestAuditReport &report)
{
   string line = tag;
   line += " attempted=" + FP_L28Bool(report.attempted);
   line += " ok=" + FP_L28Bool(report.ok);
   line += " status=" + report.status;
   line += " reason=" + report.reason;
   line += " files_written=" + IntegerToString(report.files_written);
   line += " file_errors=" + IntegerToString(report.file_errors);
   line += " audit_written=" + FP_L28Bool(report.audit_written);
   line += " latest_written=" + FP_L28Bool(report.latest_written);
   line += " duplicate_skipped=" + FP_L28Bool(report.duplicate_skipped);
   line += " execution=NO";
   Print(line);
}

#endif // __FP_BROKER_REQUEST_AUDIT_ENGINE_MQH__
