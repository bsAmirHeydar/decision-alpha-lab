#ifndef __FP_PAPER_INTENT_ENGINE_MQH__
#define __FP_PAPER_INTENT_ENGINE_MQH__
#property strict

#include "FP_PaperIntentExport.mqh"

void FP_RunLevel21PaperIntent(const string symbol,
                              const ENUM_TIMEFRAMES period,
                              const MqlRates &rates[],
                              const int bars,
                              const FP_FlagEvent &events[],
                              const FP_HookBranch &hooks[],
                              const FP_TimebaseReport &timebase_report,
                              const FP_RenderReport &render_report,
                              const FP_ValidationReport &validation_report,
                              const FP_Level20EntryBridgeConfig &entry_bridge_cfg,
                              const FP_Level21PaperIntentConfig &cfg,
                              FP_Level21PaperIntentReport &report)
{
   FP_ResetLevel21PaperIntentReport(report);
   report.attempted = cfg.enabled;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "LEVEL21_PAPER_INTENT_DISABLED";
      report.reason = "InpLevel21PaperIntentEnabled_false";
      return;
   }

   FP_Level20EntryBridgeRow bridge_row;
   FP_L20BuildEntryBridgeRow(symbol, period, rates, bars, events, hooks,
                             timebase_report, render_report, validation_report,
                             entry_bridge_cfg, bridge_row);

   FP_Level21PaperIntentRow row;
   FP_L21FillFromEntryBridge(cfg, bridge_row, row);

   bool export_ok = FP_L21ExportPaperIntent(cfg, row, report);

   report.ok = (export_ok && report.file_errors == 0);
   report.status = row.intent_status;
   report.reason = row.block_reason;
}

void FP_PrintLevel21PaperIntentReport(const string tag,
                                      const FP_Level21PaperIntentReport &report)
{
   string line = tag;
   line += " attempted=" + FP_L21Bool(report.attempted);
   line += " ok=" + FP_L21Bool(report.ok);
   line += " status=" + report.status;
   line += " reason=" + report.reason;
   line += " files_written=" + IntegerToString(report.files_written);
   line += " file_errors=" + IntegerToString(report.file_errors);
   line += " intent_written=" + FP_L21Bool(report.intent_written);
   line += " execution=NO";
   Print(line);
}

#endif // __FP_PAPER_INTENT_ENGINE_MQH__
