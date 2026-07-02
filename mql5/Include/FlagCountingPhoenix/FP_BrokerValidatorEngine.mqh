#ifndef __FP_BROKER_VALIDATOR_ENGINE_MQH__
#define __FP_BROKER_VALIDATOR_ENGINE_MQH__
#property strict

#include "FP_BrokerValidatorExport.mqh"

void FP_RunLevel26BrokerValidator(const string symbol,
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
                                  const FP_Level26BrokerValidatorConfig &cfg,
                                  FP_Level26BrokerValidatorReport &report)
{
   FP_ResetLevel26BrokerValidatorReport(report);
   report.attempted = cfg.enabled;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "LEVEL26_BROKER_VALIDATOR_DISABLED";
      report.reason = "InpLevel26BrokerValidatorEnabled_false";
      return;
   }

   FP_Level20EntryBridgeRow bridge_row;
   FP_L20BuildEntryBridgeRow(symbol, period, rates, bars, events, hooks,
                             timebase_report, render_report, validation_report,
                             entry_bridge_cfg, bridge_row);

   FP_Level21PaperIntentRow intent_row;
   FP_L21FillFromEntryBridge(intent_cfg, bridge_row, intent_row);

   FP_Level24SafetyGateRow safety_row;
   FP_L24BuildSafetyGateRow(symbol, period, license_ok, safety_cfg, safety_row);

   FP_Level25BrokerDryRunRow dry_run_row;
   FP_L25BuildBrokerDryRunRow(symbol, period, safety_row, intent_row, dry_run_cfg, dry_run_row);

   FP_Level26BrokerValidatorRow row;
   FP_L26BuildBrokerValidatorRow(symbol, period, dry_run_row, cfg, row);

   bool export_ok = FP_L26ExportBrokerValidator(cfg, row, report);

   report.ok = (export_ok && report.file_errors == 0);
   report.status = row.validator_status;
   report.reason = row.validator_block_reason;
}

void FP_PrintLevel26BrokerValidatorReport(const string tag,
                                          const FP_Level26BrokerValidatorReport &report)
{
   string line = tag;
   line += " attempted=" + FP_L26Bool(report.attempted);
   line += " ok=" + FP_L26Bool(report.ok);
   line += " status=" + report.status;
   line += " reason=" + report.reason;
   line += " files_written=" + IntegerToString(report.files_written);
   line += " file_errors=" + IntegerToString(report.file_errors);
   line += " validator_written=" + FP_L26Bool(report.validator_written);
   line += " execution=NO";
   Print(line);
}

#endif // __FP_BROKER_VALIDATOR_ENGINE_MQH__
