#ifndef __FP_BROKER_DRY_RUN_ENGINE_MQH__
#define __FP_BROKER_DRY_RUN_ENGINE_MQH__
#property strict

#include "FP_BrokerDryRunExport.mqh"

// Consolidation Patch 01 latest-row cache. Read-only diagnostic cache.
bool g_fp_c01_has_l20_entry_bridge_row = false;
FP_Level20EntryBridgeRow g_fp_c01_l20_entry_bridge_row;
bool g_fp_c01_has_l21_paper_intent_row = false;
FP_Level21PaperIntentRow g_fp_c01_l21_paper_intent_row;
bool g_fp_c01_has_l24_safety_gate_row = false;
FP_Level24SafetyGateRow g_fp_c01_l24_safety_gate_row;
bool g_fp_c01_has_l25_dry_run_row = false;
FP_Level25BrokerDryRunRow g_fp_c01_l25_dry_run_row;

void FP_RunLevel25BrokerDryRun(const string symbol,
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
                               const FP_Level25BrokerDryRunConfig &cfg,
                               FP_Level25BrokerDryRunReport &report)
{
   FP_ResetLevel25BrokerDryRunReport(report);
   report.attempted = cfg.enabled;
   g_fp_c01_has_l20_entry_bridge_row = false;
   g_fp_c01_has_l21_paper_intent_row = false;
   g_fp_c01_has_l24_safety_gate_row = false;
   g_fp_c01_has_l25_dry_run_row = false;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "LEVEL25_BROKER_DRY_RUN_DISABLED";
      report.reason = "InpLevel25BrokerDryRunEnabled_false";
      return;
   }

   FP_Level20EntryBridgeRow bridge_row;
   FP_L20BuildEntryBridgeRow(symbol, period, rates, bars, events, hooks,
                             timebase_report, render_report, validation_report,
                             entry_bridge_cfg, bridge_row);
   g_fp_c01_l20_entry_bridge_row = bridge_row;
   g_fp_c01_has_l20_entry_bridge_row = true;

   FP_Level21PaperIntentRow intent_row;
   FP_L21FillFromEntryBridge(intent_cfg, bridge_row, intent_row);
   g_fp_c01_l21_paper_intent_row = intent_row;
   g_fp_c01_has_l21_paper_intent_row = true;

   FP_Level24SafetyGateRow safety_row;
   FP_L24BuildSafetyGateRow(symbol, period, license_ok, safety_cfg, safety_row);
   g_fp_c01_l24_safety_gate_row = safety_row;
   g_fp_c01_has_l24_safety_gate_row = true;

   FP_Level25BrokerDryRunRow row;
   FP_L25BuildBrokerDryRunRow(symbol, period, safety_row, intent_row, cfg, row);
   g_fp_c01_l25_dry_run_row = row;
   g_fp_c01_has_l25_dry_run_row = true;

   bool export_ok = FP_L25ExportBrokerDryRun(cfg, row, report);

   report.ok = (export_ok && report.file_errors == 0);
   report.status = row.dry_run_status;
   report.reason = row.block_reason;
}

void FP_PrintLevel25BrokerDryRunReport(const string tag,
                                       const FP_Level25BrokerDryRunReport &report)
{
   string line = tag;
   line += " attempted=" + FP_L25Bool(report.attempted);
   line += " ok=" + FP_L25Bool(report.ok);
   line += " status=" + report.status;
   line += " reason=" + report.reason;
   line += " files_written=" + IntegerToString(report.files_written);
   line += " file_errors=" + IntegerToString(report.file_errors);
   line += " dry_run_written=" + FP_L25Bool(report.dry_run_written);
   line += " execution=NO";
   Print(line);
}

#endif // __FP_BROKER_DRY_RUN_ENGINE_MQH__
