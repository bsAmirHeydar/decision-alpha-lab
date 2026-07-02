#ifndef __FP_BROKER_REQUEST_LEDGER_ENGINE_MQH__
#define __FP_BROKER_REQUEST_LEDGER_ENGINE_MQH__
#property strict

#include "FP_BrokerRequestLedgerExport.mqh"

void FP_RunLevel27BrokerRequestLedger(const string symbol,
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
                                      const FP_Level27BrokerRequestLedgerConfig &cfg,
                                      FP_Level27BrokerRequestLedgerReport &report)
{
   FP_ResetLevel27BrokerRequestLedgerReport(report);
   report.attempted = cfg.enabled;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "LEVEL27_BROKER_REQUEST_LEDGER_DISABLED";
      report.reason = "InpLevel27BrokerRequestLedgerEnabled_false";
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

   FP_Level26BrokerValidatorRow validator_row;
   FP_L26BuildBrokerValidatorRow(symbol, period, dry_run_row, validator_cfg, validator_row);

   FP_Level27BrokerRequestLedgerRow row;
   FP_L27BuildBrokerRequestLedgerRow(symbol, period, safety_row, intent_row,
                                     dry_run_row, validator_row, cfg, row);

   row.latest_written = (cfg.export_csv && cfg.write_latest_csv);
   row.ledger_written = (cfg.export_csv && cfg.append_ledger_csv && !row.duplicate_skipped);

   bool latest_ok = FP_L27WriteLatestBrokerRequestLedger(cfg, row, report);
   bool ledger_ok = FP_L27AppendBrokerRequestLedger(cfg, row, report);

   report.ok = (latest_ok && ledger_ok && report.file_errors == 0);
   report.status = row.ledger_status;
   report.reason = row.ledger_reason;
}

void FP_PrintLevel27BrokerRequestLedgerReport(const string tag,
                                              const FP_Level27BrokerRequestLedgerReport &report)
{
   string line = tag;
   line += " attempted=" + FP_L27Bool(report.attempted);
   line += " ok=" + FP_L27Bool(report.ok);
   line += " status=" + report.status;
   line += " reason=" + report.reason;
   line += " files_written=" + IntegerToString(report.files_written);
   line += " file_errors=" + IntegerToString(report.file_errors);
   line += " ledger_written=" + FP_L27Bool(report.ledger_written);
   line += " latest_written=" + FP_L27Bool(report.latest_written);
   line += " duplicate_skipped=" + FP_L27Bool(report.duplicate_skipped);
   line += " execution=NO";
   Print(line);
}

#endif // __FP_BROKER_REQUEST_LEDGER_ENGINE_MQH__
