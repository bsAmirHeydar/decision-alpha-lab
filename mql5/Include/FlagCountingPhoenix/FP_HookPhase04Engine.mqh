#ifndef __FP_HOOK_PHASE04_ENGINE_MQH__
#define __FP_HOOK_PHASE04_ENGINE_MQH__
#property strict

#include "FP_HookPhase04Export.mqh"
#include "FP_NDSHook864CycleR1Evidence.mqh"

void FP_RunHookPhase04(const string symbol,
                       const ENUM_TIMEFRAMES period,
                       const MqlRates &rates[],
                       const int copied,
                       const int &scales[],
                       const int scale_count,
                       const FP_HookPhase01Config &node_cfg,
                       const FP_HookPhase02Config &sequence_cfg,
                       const FP_HookPhase03Config &y_cfg,
                       const FP_HookPhase04Config &cfg,
                       FP_HookPhase04Report &report)
{
   FP_ResetHookPhase04Report(report);

   if(!FP_HookP04ShouldRun(cfg))
   {
      FP_NDSClearHook864CycleR1EvidenceSnapshot();
      report.status = "HOOK_P04_SKIPPED";
      report.reason = "DISPLAY_FAMILY_RALLY_ONLY_OR_DISABLED";
      report.ok = true;
      return;
   }

   report.attempted = true;
   report.bars_seen = copied;
   report.scales_seen = scale_count;

   // Phase 01 rebuild: node stream.
   FP_HookPhase01Config p01_cfg = node_cfg;
   p01_cfg.enabled = true;
   p01_cfg.display_family = cfg.display_family;
   p01_cfg.show_peaks = true;
   p01_cfg.show_valleys = true;
   if(cfg.max_bars_to_scan > 0)
      p01_cfg.max_bars_to_scan = cfg.max_bars_to_scan;

   FP_HookPhase01Node nodes[];
   FP_HookPhase01ScaleSummary summaries[];
   FP_HookPhase01Report node_report;
   FP_ResetHookPhase01Report(node_report);

   FP_HookP01BuildNodes(rates, copied, scales, scale_count, p01_cfg,
                        nodes, summaries, node_report);

   report.bars_scanned = node_report.bars_scanned;
   report.nodes_seen = ArraySize(nodes);

   // Phase 02 rebuild: strict X-sequences.
   FP_HookPhase02Config p02_cfg = sequence_cfg;
   p02_cfg.enabled = true;
   p02_cfg.display_family = cfg.display_family;
   p02_cfg.show_positive = cfg.show_positive;
   p02_cfg.show_negative = cfg.show_negative;
   p02_cfg.max_sequences = cfg.max_sequences;
   p02_cfg.max_bars_to_scan = cfg.max_bars_to_scan;
   p02_cfg.min_x_nodes_to_keep = cfg.min_x_nodes_to_keep;
   p02_cfg.max_x_nodes_per_sequence = cfg.max_x_nodes_per_sequence;

   FP_HookPhase02Sequence sequences[];
   FP_HookPhase02Report sequence_report;
   FP_ResetHookPhase02Report(sequence_report);
   sequence_report.nodes_seen = ArraySize(nodes);

   FP_HookP02BuildSequencesWithRates(rates, copied, nodes, p02_cfg, sequences, sequence_report);
   FP_HookP02FinalizeReport(sequence_report);

   report.phase02_sequences_seen = ArraySize(sequences);

   // Phase 03 rebuild: Y-axis opposite extremes.
   FP_HookPhase03Config p03_cfg = y_cfg;
   p03_cfg.enabled = true;
   p03_cfg.display_family = cfg.display_family;
   p03_cfg.show_positive = cfg.show_positive;
   p03_cfg.show_negative = cfg.show_negative;
   p03_cfg.max_sequences = cfg.max_sequences;
   p03_cfg.max_bars_to_scan = cfg.max_bars_to_scan;
   p03_cfg.min_x_nodes_to_keep = cfg.min_x_nodes_to_keep;
   p03_cfg.max_x_nodes_per_sequence = cfg.max_x_nodes_per_sequence;

   FP_HookPhase03Record p03_records[];
   FP_HookPhase03Report p03_report;
   FP_ResetHookPhase03Report(p03_report);
   p03_report.phase02_sequences_seen = ArraySize(sequences);

   FP_HookP03BuildRecords(rates, copied, sequences, p03_cfg, p03_records, p03_report);
   FP_HookP03FinalizeReport(p03_report);

   report.phase03_records_seen = ArraySize(p03_records);

   // Phase 04 lifecycle.
   FP_HookPhase04Record records[];
   FP_HookP04BuildRecords(rates, copied, p03_records, cfg, records, report);
   FP_HookP04FinalizeReport(report);

   // Read-only handoff to the integrated 86.4 execution profile. This uses the
   // exact Phase04 records produced above and scans only the same closed-rate
   // array for first-arrival evidence.
   FP_NDSCaptureHook864CycleR1EvidenceSnapshot(symbol, period,
                                                rates, copied, records);

   if(cfg.draw_nd || cfg.draw_death || cfg.draw_x_closure || cfg.draw_thresholds)
      FP_HookP04DrawRecords(cfg, records, report);

   if(cfg.export_csv)
   {
      FP_HookP04ExportLifecycle(cfg, records, report);
      FP_HookP04ExportSummary(symbol, period, cfg, report);
   }

   if(cfg.print_summary)
      FP_PrintHookPhase04Report("FP_HOOK_P04", report);

   if(cfg.print_samples)
      FP_PrintHookPhase04Samples("FP_HOOK_P04", records, cfg.sample_limit);
}

#endif // __FP_HOOK_PHASE04_ENGINE_MQH__
