#ifndef __FP_HOOK_PHASE03_ENGINE_MQH__
#define __FP_HOOK_PHASE03_ENGINE_MQH__
#property strict

#include "FP_HookPhase03Export.mqh"

void FP_RunHookPhase03(const string symbol,
                       const ENUM_TIMEFRAMES period,
                       const MqlRates &rates[],
                       const int copied,
                       const int &scales[],
                       const int scale_count,
                       const FP_HookPhase01Config &node_cfg,
                       const FP_HookPhase02Config &sequence_cfg,
                       const FP_HookPhase03Config &cfg,
                       FP_HookPhase03Report &report)
{
   FP_ResetHookPhase03Report(report);

   if(!FP_HookP03ShouldRun(cfg))
   {
      report.status = "HOOK_P03_SKIPPED";
      report.reason = "DISPLAY_FAMILY_RALLY_ONLY_OR_DISABLED";
      report.ok = true;
      return;
   }

   report.attempted = true;
   report.bars_seen = copied;
   report.scales_seen = scale_count;

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

   FP_HookPhase03Record records[];
   FP_HookP03BuildRecords(rates, copied, sequences, cfg, records, report);
   FP_HookP03FinalizeReport(report);

   if(cfg.draw_y_extremes || cfg.draw_y_lines || cfg.draw_x_reference)
      FP_HookP03DrawRecords(cfg, records, report);

   if(cfg.export_csv)
   {
      FP_HookP03ExportYAxis(cfg, records, report);
      FP_HookP03ExportSummary(symbol, period, cfg, report);
   }

   if(cfg.print_summary)
      FP_PrintHookPhase03Report("FP_HOOK_P03", report);

   if(cfg.print_samples)
      FP_PrintHookPhase03Samples("FP_HOOK_P03", records, cfg.sample_limit);
}

#endif // __FP_HOOK_PHASE03_ENGINE_MQH__
