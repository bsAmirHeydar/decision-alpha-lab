#ifndef __FP_HOOK_PHASE02_DETECTION_CORE_MQH__
#define __FP_HOOK_PHASE02_DETECTION_CORE_MQH__
#property strict

#include "FP_HookPhase02Rules.mqh"
#include "FP_NDSStructureSnapshot.mqh"

// Detection-only Phase 02 contract. No chart objects, files, or log output.
// The production engine wraps this core with optional visual/export sinks.
void FP_RunHookPhase02DetectionCore(const string symbol,
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
                                    FP_HookPhase02Sequence &sequences[],
                                    FP_HookPhase02Report &report)
{
   FP_ResetHookPhase02Report(report);
   FP_NDSClearStructureSnapshot();
   ArrayResize(sequences, 0);

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

   FP_HookP02BuildSequencesWithRates(rates, copied, nodes, cfg, sequences, report);
   if(use_f3_validity_context)
      FP_HookP02AnnotateValidityFamiliesWithF3(sequences, events, event_count, cfg, report);

   FP_NDSCaptureStructureSnapshot(symbol, period, sequences);
   FP_HookP02FinalizeReport(report);
}

#endif // __FP_HOOK_PHASE02_DETECTION_CORE_MQH__
