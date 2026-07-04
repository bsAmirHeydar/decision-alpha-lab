#ifndef __FP_HOOK_PHASE01_ENGINE_MQH__
#define __FP_HOOK_PHASE01_ENGINE_MQH__
#property strict

#include "FP_HookPhase01Export.mqh"

void FP_RunHookPhase01(const string symbol,
                       const ENUM_TIMEFRAMES period,
                       const MqlRates &rates[],
                       const int copied,
                       const int &scales[],
                       const int scale_count,
                       const FP_HookPhase01Config &cfg,
                       FP_HookPhase01Report &report)
{
   FP_ResetHookPhase01Report(report);

   if(!FP_HookP01ShouldRun(cfg))
   {
      report.status = "HOOK_P01_SKIPPED";
      report.reason = "DISPLAY_FAMILY_RALLY_ONLY_OR_DISABLED";
      report.ok = true;
      return;
   }

   report.attempted = true;

   FP_HookPhase01Node nodes[];
   FP_HookPhase01ScaleSummary summaries[];
   FP_HookP01BuildNodes(rates, copied, scales, scale_count, cfg, nodes, summaries, report);

   FP_HookP01FinalizeReport(report);

   if(cfg.draw_nodes)
      FP_HookP01DrawNodes(cfg, nodes, report);

   if(cfg.export_csv)
   {
      FP_HookP01ExportNodes(cfg, nodes, report);
      FP_HookP01ExportSummary(symbol, period, cfg, report);
   }

   if(cfg.print_summary)
      FP_PrintHookPhase01Report("FP_HOOK_P01", report);

   if(cfg.print_samples)
      FP_PrintHookPhase01Samples("FP_HOOK_P01", nodes, cfg.sample_limit);
}

#endif // __FP_HOOK_PHASE01_ENGINE_MQH__
