#ifndef __FP_PAPER_BROKER_ADAPTER_ENGINE_MQH__
#define __FP_PAPER_BROKER_ADAPTER_ENGINE_MQH__
#property strict

#include "FP_PaperBrokerAdapterExport.mqh"

void FP_RunLevel29PaperBrokerAdapter(const string symbol,
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
                                     const FP_Level28BrokerRequestAuditConfig &audit_cfg,
                                     const FP_Level29PaperBrokerAdapterConfig &cfg,
                                     FP_Level29PaperBrokerAdapterReport &report)
{
   FP_ResetLevel29PaperBrokerAdapterReport(report);
   report.attempted = cfg.enabled;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "LEVEL29_PAPER_BROKER_ADAPTER_DISABLED";
      report.reason = "InpLevel29PaperBrokerAdapterEnabled_false";
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

   FP_Level28BrokerRequestAuditRow audit_row;
   FP_L28BuildBrokerRequestAuditRow(symbol, period, safety_row, intent_row,
                                    dry_run_row, validator_row, audit_cfg, audit_row);

   FP_Level29PaperBrokerAdapterRow row;
   FP_L29BuildPaperBrokerAdapterRow(symbol, period, dry_run_row, validator_row, audit_row, cfg, row);

   bool latest_ok = FP_L29WriteLatestPaperBrokerAdapter(cfg, row, report);
   bool adapter_ok = FP_L29AppendPaperBrokerAdapter(cfg, row, report);

   row.latest_written = report.latest_written;
   row.adapter_written = report.adapter_written;

   report.ok = (latest_ok && adapter_ok && report.file_errors == 0);
   report.status = row.adapter_status;
   report.reason = row.adapter_block_reason;
}

void FP_PrintLevel29PaperBrokerAdapterReport(const string tag,
                                             const FP_Level29PaperBrokerAdapterReport &report)
{
   string line = tag;
   line += " attempted=" + FP_L29Bool(report.attempted);
   line += " ok=" + FP_L29Bool(report.ok);
   line += " status=" + report.status;
   line += " reason=" + report.reason;
   line += " files_written=" + IntegerToString(report.files_written);
   line += " file_errors=" + IntegerToString(report.file_errors);
   line += " adapter_written=" + FP_L29Bool(report.adapter_written);
   line += " latest_written=" + FP_L29Bool(report.latest_written);
   line += " duplicate_skipped=" + FP_L29Bool(report.duplicate_skipped);
   line += " execution=NO";
   Print(line);
}

#endif // __FP_PAPER_BROKER_ADAPTER_ENGINE_MQH__
