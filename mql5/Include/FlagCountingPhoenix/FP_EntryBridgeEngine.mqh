#ifndef __FP_ENTRY_BRIDGE_ENGINE_MQH__
#define __FP_ENTRY_BRIDGE_ENGINE_MQH__
#property strict

#include "FP_EntryBridgeExport.mqh"

void FP_RunLevel20EntryBridge(const string symbol,
                              const ENUM_TIMEFRAMES period,
                              const MqlRates &rates[],
                              const int bars,
                              const FP_FlagEvent &events[],
                              const FP_HookBranch &hooks[],
                              const FP_TimebaseReport &timebase_report,
                              const FP_RenderReport &render_report,
                              const FP_ValidationReport &validation_report,
                              const FP_Level20EntryBridgeConfig &cfg,
                              FP_Level20EntryBridgeReport &report)
{
   FP_ResetLevel20EntryBridgeReport(report);
   report.attempted = cfg.enabled;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "LEVEL20_ENTRY_BRIDGE_DISABLED";
      report.reason = "InpLevel20EntryBridgeEnabled_false";
      return;
   }

   FP_Level20EntryBridgeRow row;
   FP_L20BuildEntryBridgeRow(symbol, period, rates, bars, events, hooks,
                             timebase_report, render_report, validation_report,
                             cfg, row);

   bool export_ok = FP_L20ExportEntryBridge(cfg, row, report);

   report.ok = (export_ok && report.file_errors == 0);
   report.status = row.bridge_status;
   report.reason = row.block_reason;
}

void FP_PrintLevel20EntryBridgeReport(const string tag,
                                      const FP_Level20EntryBridgeReport &report)
{
   string line = tag;
   line += " attempted=" + FP_L20Bool(report.attempted);
   line += " ok=" + FP_L20Bool(report.ok);
   line += " status=" + report.status;
   line += " reason=" + report.reason;
   line += " files_written=" + IntegerToString(report.files_written);
   line += " file_errors=" + IntegerToString(report.file_errors);
   line += " bridge_written=" + FP_L20Bool(report.bridge_written);
   line += " execution=NO";
   Print(line);
}

#endif // __FP_ENTRY_BRIDGE_ENGINE_MQH__
