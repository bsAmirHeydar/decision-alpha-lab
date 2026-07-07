#ifndef __FP_HOOK_PHASE02_ENGINE_MQH__
#define __FP_HOOK_PHASE02_ENGINE_MQH__
#property strict

#include "FP_HookPhase02Export.mqh"


void FP_RunHookPhase02Core(const string symbol,
                           const ENUM_TIMEFRAMES period,
                           const MqlRates &rates[],
                           const int copied,
                           const int &scales[],
                           const int scale_count,
                           const FP_HookPhase01Config &node_cfg,
                           const FP_HookPhase02Config &cfg,
                           const FP_FlagEvent &events[],
                           const int event_count,
                           const bool use_f3_validity_context,
                           FP_HookPhase02Report &report)
{
   FP_ResetHookPhase02Report(report);

   if(!FP_HookP02ShouldRun(cfg))
   {
      report.status = "HOOK_P02_SKIPPED";
      report.reason = "DISPLAY_FAMILY_RALLY_ONLY_OR_DISABLED";
      report.ok = true;
      return;
   }

   report.attempted = true;
   report.bars_seen = copied;
   report.scales_seen = scale_count;

   FP_HookPhase01Config build_cfg = node_cfg;
   build_cfg.enabled = true;
   build_cfg.display_family = cfg.display_family;
   build_cfg.show_peaks = true;
   build_cfg.show_valleys = true;

   if(cfg.max_bars_to_scan > 0)
      build_cfg.max_bars_to_scan = cfg.max_bars_to_scan;

   FP_HookPhase01Node nodes[];
   FP_HookPhase01ScaleSummary summaries[];
   FP_HookPhase01Report node_report;
   FP_ResetHookPhase01Report(node_report);

   FP_HookP01BuildNodes(rates, copied, scales, scale_count, build_cfg,
                        nodes, summaries, node_report);
   report.bars_scanned = node_report.bars_scanned;

   FP_HookPhase02Sequence sequences[];
   FP_HookP02BuildSequencesWithRates(rates, copied, nodes, cfg, sequences, report);
   if(use_f3_validity_context)
      FP_HookP02AnnotateValidityFamiliesWithF3(sequences, events, event_count, report);
   FP_HookP02FinalizeReport(report);

   if(cfg.draw_sequences)
      FP_HookP02DrawSequences(cfg, sequences, report);

   if(cfg.export_csv)
   {
      FP_HookP02ExportSequences(cfg, sequences, report);
      FP_HookP02ExportSummary(symbol, period, cfg, report);
   }

   if(cfg.print_summary)
      FP_PrintHookPhase02Report("FP_HOOK_P02", report);

   if(cfg.print_samples)
      FP_PrintHookPhase02Samples("FP_HOOK_P02", sequences, cfg.sample_limit);
}

void FP_RunHookPhase02(const string symbol,
                       const ENUM_TIMEFRAMES period,
                       const MqlRates &rates[],
                       const int copied,
                       const int &scales[],
                       const int scale_count,
                       const FP_HookPhase01Config &node_cfg,
                       const FP_HookPhase02Config &cfg,
                       FP_HookPhase02Report &report)
{
   FP_FlagEvent empty_events[];
   ArrayResize(empty_events, 0);
   FP_RunHookPhase02Core(symbol, period, rates, copied, scales, scale_count,
                         node_cfg, cfg, empty_events, 0, false, report);
}

void FP_RunHookPhase02WithEvents(const string symbol,
                                 const ENUM_TIMEFRAMES period,
                                 const MqlRates &rates[],
                                 const int copied,
                                 const int &scales[],
                                 const int scale_count,
                                 const FP_HookPhase01Config &node_cfg,
                                 const FP_HookPhase02Config &cfg,
                                 const FP_FlagEvent &events[],
                                 const int event_count,
                                 FP_HookPhase02Report &report)
{
   FP_RunHookPhase02Core(symbol, period, rates, copied, scales, scale_count,
                         node_cfg, cfg, events, event_count, true, report);
}

#endif // __FP_HOOK_PHASE02_ENGINE_MQH__
