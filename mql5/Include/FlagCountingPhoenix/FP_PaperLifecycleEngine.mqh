#ifndef __FP_PAPER_LIFECYCLE_ENGINE_MQH__
#define __FP_PAPER_LIFECYCLE_ENGINE_MQH__
#property strict

#include "FP_PaperLifecycleExport.mqh"

void FP_RunLevel22PaperLifecycle(const string symbol,
                                 const ENUM_TIMEFRAMES period,
                                 const MqlRates &rates[],
                                 const int bars,
                                 const FP_FlagEvent &events[],
                                 const FP_HookBranch &hooks[],
                                 const FP_TimebaseReport &timebase_report,
                                 const FP_RenderReport &render_report,
                                 const FP_ValidationReport &validation_report,
                                 const FP_Level20EntryBridgeConfig &entry_bridge_cfg,
                                 const FP_Level21PaperIntentConfig &intent_cfg,
                                 const FP_Level22PaperLifecycleConfig &cfg,
                                 FP_Level22PaperLifecycleReport &report)
{
   FP_ResetLevel22PaperLifecycleReport(report);
   report.attempted = cfg.enabled;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "LEVEL22_PAPER_LIFECYCLE_DISABLED";
      report.reason = "InpLevel22PaperLifecycleEnabled_false";
      return;
   }

   FP_Level20EntryBridgeRow bridge_row;
   FP_L20BuildEntryBridgeRow(symbol, period, rates, bars, events, hooks,
                             timebase_report, render_report, validation_report,
                             entry_bridge_cfg, bridge_row);

   FP_Level21PaperIntentRow intent_row;
   FP_L21FillFromEntryBridge(intent_cfg, bridge_row, intent_row);

   FP_Level22PaperLifecycleRow row;
   FP_L22SeedFromIntent(cfg, intent_row, row);
   FP_L22EvaluateCloseOnlyLifecycle(cfg, rates, bars, row);

   bool export_ok = FP_L22ExportPaperLifecycle(cfg, row, report);

   report.ok = (export_ok && report.file_errors == 0);
   report.status = row.lifecycle_status;
   report.reason = row.block_reason;
}

void FP_PrintLevel22PaperLifecycleReport(const string tag,
                                         const FP_Level22PaperLifecycleReport &report)
{
   string line = tag;
   line += " attempted=" + FP_L22Bool(report.attempted);
   line += " ok=" + FP_L22Bool(report.ok);
   line += " status=" + report.status;
   line += " reason=" + report.reason;
   line += " files_written=" + IntegerToString(report.files_written);
   line += " file_errors=" + IntegerToString(report.file_errors);
   line += " lifecycle_written=" + FP_L22Bool(report.lifecycle_written);
   line += " execution=NO";
   Print(line);
}

#endif // __FP_PAPER_LIFECYCLE_ENGINE_MQH__
