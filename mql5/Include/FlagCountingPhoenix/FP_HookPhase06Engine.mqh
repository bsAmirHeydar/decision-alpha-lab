#ifndef __FP_HOOK_PHASE06_ENGINE_MQH__
#define __FP_HOOK_PHASE06_ENGINE_MQH__
#property strict

#include "FP_HookPhase06Export.mqh"

void FP_RunHookPhase06(const string symbol,
                       const ENUM_TIMEFRAMES period,
                       const MqlRates &rates[],
                       const int copied,
                       const int &scales[],
                       const int scale_count,
                       const FP_HookPhase01Config &node_cfg,
                       const FP_HookPhase02Config &sequence_cfg,
                       const FP_HookPhase03Config &y_cfg,
                       const FP_HookPhase04Config &life_cfg,
                       const FP_HookPhase05Config &type_cfg,
                       const FP_HookPhase06Config &cfg,
                       FP_HookPhase06Report &report)
{
   FP_ResetHookPhase06Report(report);

   if(!FP_HookP06ShouldRun(cfg))
   {
      report.status = "HOOK_P06_SKIPPED";
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

   FP_HookP02BuildSequences(nodes, p02_cfg, sequences, sequence_report);
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

   // Phase 04 rebuild: ND/death/X-closure lifecycle.
   FP_HookPhase04Config p04_cfg = life_cfg;
   p04_cfg.enabled = true;
   p04_cfg.display_family = cfg.display_family;
   p04_cfg.show_positive = cfg.show_positive;
   p04_cfg.show_negative = cfg.show_negative;
   p04_cfg.max_sequences = cfg.max_sequences;
   p04_cfg.max_bars_to_scan = cfg.max_bars_to_scan;
   p04_cfg.min_x_nodes_to_keep = cfg.min_x_nodes_to_keep;
   p04_cfg.max_x_nodes_per_sequence = cfg.max_x_nodes_per_sequence;

   FP_HookPhase04Record p04_records[];
   FP_HookPhase04Report p04_report;
   FP_ResetHookPhase04Report(p04_report);
   p04_report.phase03_records_seen = ArraySize(p03_records);

   FP_HookP04BuildRecords(rates, copied, p03_records, p04_cfg, p04_records, p04_report);
   FP_HookP04FinalizeReport(p04_report);

   report.phase04_records_seen = ArraySize(p04_records);

   // Phase 05 rebuild: Hook Type A/B/C classifier.
   FP_HookPhase05Config p05_cfg = type_cfg;
   p05_cfg.enabled = true;
   p05_cfg.display_family = cfg.display_family;
   p05_cfg.show_positive = cfg.show_positive;
   p05_cfg.show_negative = cfg.show_negative;
   p05_cfg.max_sequences = cfg.max_sequences;
   p05_cfg.max_bars_to_scan = cfg.max_bars_to_scan;
   p05_cfg.min_x_nodes_to_keep = cfg.min_x_nodes_to_keep;
   p05_cfg.max_x_nodes_per_sequence = cfg.max_x_nodes_per_sequence;

   FP_HookPhase05Record p05_records[];
   FP_HookPhase05Report p05_report;
   FP_ResetHookPhase05Report(p05_report);
   p05_report.phase04_records_seen = ArraySize(p04_records);

   FP_HookP05BuildRecords(p04_records, p05_cfg, p05_records, p05_report);
   FP_HookP05FinalizeReport(p05_report);

   report.phase05_records_seen = ArraySize(p05_records);

   // Phase 06 score layer.
   FP_HookPhase06Record records[];
   FP_HookP06BuildRecords(p05_records, cfg, records, report);
   FP_HookP06FinalizeReport(report);

   if(cfg.draw_quality_label || cfg.draw_xy_anchor || cfg.draw_projection_lines)
      FP_HookP06DrawRecords(cfg, records, report);

   if(cfg.export_csv)
   {
      FP_HookP06ExportQuality(cfg, records, report);
      FP_HookP06ExportSummary(symbol, period, cfg, report);
   }

   if(cfg.print_summary)
      FP_PrintHookPhase06Report("FP_HOOK_P06", report);

   if(cfg.print_samples)
      FP_PrintHookPhase06Samples("FP_HOOK_P06", records, cfg.sample_limit);
}

#endif // __FP_HOOK_PHASE06_ENGINE_MQH__
