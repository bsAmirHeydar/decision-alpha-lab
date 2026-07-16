#ifndef __FP_NDS_HOOK_864_CYCLE_R1_EVIDENCE_ENGINE_MQH__
#define __FP_NDS_HOOK_864_CYCLE_R1_EVIDENCE_ENGINE_MQH__
#property strict

#include "FP_NDSHook864CycleR1Evidence.mqh"
#include "FP_HookPhase03Rules.mqh"
#include "FP_HookPhase04Rules.mqh"

// Lightweight evidence-only bridge used by Strategy Tester. It consumes the
// already-built canonical Phase02 sequences and invokes canonical Phase03/04
// record builders. It does not redraw, export, detect a parallel Hook, or send.
//
// Exact acceleration is candidate-scoped: Phase03/04 are evaluated only for
// sequences that already pass every pre-closure hard gate of the 86.4 profile.
// A sequence excluded here cannot become executable through Phase04, therefore
// the decision set is identical while the expensive lifecycle scan is bounded.

bool FP_NDSHook864CycleR1NeedsClosureEvidence(
   const FP_HookPhase02Sequence &seq,
   const FP_NDSHookTradeConfig &trade_cfg)
{
   if(!seq.valid || seq.hook_failed || !seq.valid_hook_family)
      return false;
   if(!((seq.valid_after_hook && trade_cfg.allow_hook_after_hook) ||
        (seq.valid_after_opposing_f3 && trade_cfg.allow_hook_after_f3)))
      return false;
   if(!FP_HookP02SequenceCycleClosed(seq) || !seq.resolve_confirmed)
      return false;
   if(!seq.cycle_crown_valid || seq.cycle_crown_price <= 0.0)
      return false;
   if(seq.origin_price <= 0.0 || seq.resolve_price <= 0.0)
      return false;
   if(seq.x_count < trade_cfg.hook_entry_min_x_count ||
      seq.x_count > trade_cfg.hook_entry_max_x_count)
      return false;
   if(seq.state != FP_HOOK_P02_STATE_MATURE &&
      seq.state != FP_HOOK_P02_STATE_CAPPED)
      return false;
   if(seq.direction != FP_HOOK_P02_DIRECTION_POSITIVE &&
      seq.direction != FP_HOOK_P02_DIRECTION_NEGATIVE)
      return false;

   double entry = FP_NDSHook864CycleR1RawEntryFromSequence(
      seq, trade_cfg.hook_entry_ratio);
   if(entry <= 0.0)
      return false;
   if(seq.direction == FP_HOOK_P02_DIRECTION_POSITIVE)
      return (seq.origin_price < entry && entry < seq.cycle_crown_price);
   return (seq.cycle_crown_price < entry && entry < seq.origin_price);
}

int FP_NDSHook864CycleR1FilterClosureCandidates(
   const FP_HookPhase02Sequence &sequences[],
   const FP_NDSHookTradeConfig &trade_cfg,
   FP_HookPhase02Sequence &candidates[])
{
   ArrayResize(candidates, 0);
   int total = ArraySize(sequences);
   for(int i=0; i<total; i++)
   {
      if(!FP_NDSHook864CycleR1NeedsClosureEvidence(sequences[i], trade_cfg))
         continue;
      int next = ArraySize(candidates);
      ArrayResize(candidates, next + 1);
      candidates[next] = sequences[i];
   }
   return ArraySize(candidates);
}

bool FP_RunNDSHook864CycleR1EvidenceEngine(
   const string symbol,
   const ENUM_TIMEFRAMES period,
   const MqlRates &rates[],
   const int copied,
   const FP_HookPhase02Sequence &sequences[],
   const FP_HookPhase02Config &hook_cfg,
   const FP_NDSHookTradeConfig &trade_cfg,
   const bool candidate_scope,
   FP_HookPhase03Report &p03_report,
   FP_HookPhase04Report &p04_report,
   int &candidate_sequence_count)
{
   FP_ResetHookPhase03Report(p03_report);
   FP_ResetHookPhase04Report(p04_report);
   FP_NDSClearHook864CycleR1EvidenceSnapshot();

   FP_HookPhase02Sequence candidates[];
   if(candidate_scope)
   {
      candidate_sequence_count = FP_NDSHook864CycleR1FilterClosureCandidates(
         sequences, trade_cfg, candidates);
   }
   else
   {
      candidate_sequence_count = ArraySize(sequences);
      ArrayResize(candidates, candidate_sequence_count);
      for(int i=0; i<candidate_sequence_count; i++)
         candidates[i] = sequences[i];
   }

   FP_HookPhase03Config p03_cfg;
   FP_ResetHookPhase03Config(p03_cfg);
   p03_cfg.enabled = true;
   p03_cfg.display_family = FP_NDS_HOOK_DISPLAY_HOOK_ONLY;
   p03_cfg.show_positive = hook_cfg.show_positive;
   p03_cfg.show_negative = hook_cfg.show_negative;
   p03_cfg.draw_y_extremes = false;
   p03_cfg.draw_y_lines = false;
   p03_cfg.draw_x_reference = false;
   p03_cfg.draw_labels = false;
   p03_cfg.export_csv = false;
   p03_cfg.print_summary = false;
   p03_cfg.print_samples = false;
   p03_cfg.max_bars_to_scan = hook_cfg.max_bars_to_scan;
   p03_cfg.max_sequences = hook_cfg.max_sequences;
   p03_cfg.max_sequences_to_draw = 0;
   p03_cfg.min_x_nodes_to_keep = hook_cfg.min_x_nodes_to_keep;
   p03_cfg.max_x_nodes_per_sequence = hook_cfg.max_x_nodes_per_sequence;

   FP_HookPhase03Record p03_records[];
   p03_report.phase02_sequences_seen = candidate_sequence_count;
   if(candidate_sequence_count > 0)
      FP_HookP03BuildRecords(rates, copied, candidates, p03_cfg,
                             p03_records, p03_report);
   FP_HookP03FinalizeReport(p03_report);

   FP_HookPhase04Config p04_cfg;
   FP_ResetHookPhase04Config(p04_cfg);
   p04_cfg.enabled = true;
   p04_cfg.display_family = FP_NDS_HOOK_DISPLAY_HOOK_ONLY;
   p04_cfg.show_positive = hook_cfg.show_positive;
   p04_cfg.show_negative = hook_cfg.show_negative;
   p04_cfg.draw_nd = false;
   p04_cfg.draw_death = false;
   p04_cfg.draw_x_closure = false;
   p04_cfg.draw_thresholds = false;
   p04_cfg.draw_labels = false;
   p04_cfg.export_csv = false;
   p04_cfg.print_summary = false;
   p04_cfg.print_samples = false;
   p04_cfg.max_bars_to_scan = hook_cfg.max_bars_to_scan;
   p04_cfg.max_sequences = hook_cfg.max_sequences;
   p04_cfg.max_sequences_to_draw = 0;
   p04_cfg.min_x_nodes_to_keep = hook_cfg.min_x_nodes_to_keep;
   p04_cfg.max_x_nodes_per_sequence = hook_cfg.max_x_nodes_per_sequence;
   p04_cfg.min_x_nodes_for_closure = FP_NDS_HOOK_864_MIN_X_COUNT;
   p04_cfg.closure_retrace_ratio = FP_NDS_HOOK_864_CLOSURE_RATIO;

   FP_HookPhase04Record p04_records[];
   p04_report.bars_seen = copied;
   p04_report.phase02_sequences_seen = candidate_sequence_count;
   p04_report.phase03_records_seen = ArraySize(p03_records);
   if(ArraySize(p03_records) > 0)
      FP_HookP04BuildRecords(rates, copied, p03_records, p04_cfg,
                             p04_records, p04_report);
   FP_HookP04FinalizeReport(p04_report);

   FP_NDSCaptureHook864CycleR1EvidenceSnapshot(symbol, period,
                                                rates, copied, p04_records);
   return (p03_report.ok && p04_report.ok &&
           FP_NDSHook864CycleR1EvidenceSnapshotMatches(symbol, period));
}

#endif // __FP_NDS_HOOK_864_CYCLE_R1_EVIDENCE_ENGINE_MQH__
