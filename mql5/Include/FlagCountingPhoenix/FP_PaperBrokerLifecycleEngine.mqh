#ifndef __FP_PAPER_BROKER_LIFECYCLE_ENGINE_MQH__
#define __FP_PAPER_BROKER_LIFECYCLE_ENGINE_MQH__
#property strict

#include "FP_PaperBrokerLifecycleExport.mqh"

void FP_RunLevel30PaperBrokerLifecycle(const string symbol,
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
                                       const FP_Level29PaperBrokerAdapterConfig &adapter_cfg,
                                       const FP_Level30PaperBrokerLifecycleConfig &cfg,
                                       FP_Level30PaperBrokerLifecycleReport &report)
{
   FP_ResetLevel30PaperBrokerLifecycleReport(report);
   report.attempted = cfg.enabled;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "LEVEL30_PAPER_BROKER_LIFECYCLE_DISABLED";
      report.reason = "InpLevel30PaperBrokerLifecycleEnabled_false";
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

   FP_Level29PaperBrokerAdapterRow adapter_row;
   FP_L29BuildPaperBrokerAdapterRow(symbol, period, dry_run_row, validator_row, audit_row,
                                    adapter_cfg, adapter_row);

   FP_Level30PaperBrokerLifecycleRow row;
   FP_L30SeedFromAdapter(cfg, adapter_row, row);
   FP_L30EvaluateLifecycle(cfg, rates, bars, row);
   FP_L30FinalizeKey(cfg, row);

   bool latest_ok = FP_L30WriteLatestPaperBrokerLifecycle(cfg, row, report);
   bool lifecycle_ok = FP_L30AppendPaperBrokerLifecycle(cfg, row, report);

   row.latest_written = report.latest_written;
   row.lifecycle_written = report.lifecycle_written;

   report.ok = (latest_ok && lifecycle_ok && report.file_errors == 0);
   report.status = row.lifecycle_status;
   report.reason = row.lifecycle_block_reason;
}

void FP_PrintLevel30PaperBrokerLifecycleReport(const string tag,
                                               const FP_Level30PaperBrokerLifecycleReport &report)
{
   string line = tag;
   line += " attempted=" + FP_L30Bool(report.attempted);
   line += " ok=" + FP_L30Bool(report.ok);
   line += " status=" + report.status;
   line += " reason=" + report.reason;
   line += " files_written=" + IntegerToString(report.files_written);
   line += " file_errors=" + IntegerToString(report.file_errors);
   line += " lifecycle_written=" + FP_L30Bool(report.lifecycle_written);
   line += " latest_written=" + FP_L30Bool(report.latest_written);
   line += " duplicate_skipped=" + FP_L30Bool(report.duplicate_skipped);
   line += " execution=NO";
   Print(line);
}

#endif // __FP_PAPER_BROKER_LIFECYCLE_ENGINE_MQH__
