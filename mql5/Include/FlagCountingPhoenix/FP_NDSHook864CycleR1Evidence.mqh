#ifndef __FP_NDS_HOOK_864_CYCLE_R1_EVIDENCE_MQH__
#define __FP_NDS_HOOK_864_CYCLE_R1_EVIDENCE_MQH__
#property strict

#include "FP_NDSHookTradeTypes.mqh"
#include "FP_HookPhase04Types.mqh"

// ============================================================================
// NDS Hook 86.4 Cycle R1 - canonical closure/first-arrival evidence bridge
// ----------------------------------------------------------------------------
// Owner boundaries:
// - X nodes and Hook identity: Hook Phase 02
// - Y reference and 50% X closure: Hook Phase 03/04
// - first 86.4 touch after closure: this read-only bridge over closed rates
// - order placement, sizing and broker state: NDS Hook Trade execution modules
//
// This module has no order, position, file, network or chart authority.
// ============================================================================

#define FP_NDS_HOOK_864_EVIDENCE_VERSION "NDS-HOOK-864-EVIDENCE-02"

struct FP_NDSHook864CycleR1Evidence
{
   bool valid;
   string status;
   // sequence_id is retained for audit only. Cross-engine matching uses the
   // stable structural identity below because sequence_id is an array-local
   // index and may differ when a caller applies different filtering limits.
   int sequence_id;
   int scale_l;
   int origin_node_id;
   datetime origin_time;
   FP_HookPhase02Direction direction;
   int x_count;
   int x1_node_id;
   int x2_node_id;
   int x3_node_id;
   int x4_node_id;
   int crown_node_id;
   datetime crown_time;

   double origin_price;
   double crown_price;
   double entry_price;

   bool phase04_record_valid;
   bool x_closure_candidate;
   bool x_closed;
   datetime x_closure_time;
   int x_closure_bar_index;
   double x_closure_price;
   double x_closure_threshold_price;
   double x_closure_reference_y_price;
   datetime x_closure_reference_y_time;

   bool origin_return_penetrated;
   datetime death_time;
   int death_bar_index;
   double death_price;

   bool level_touched_after_closure;
   datetime first_touch_time;
   int first_touch_bar_index;
   double first_touch_price;
};

FP_NDSHook864CycleR1Evidence g_fp_nds_hook_864_evidence[];
// Fast hint keyed by the Phase02 sequence id. Identity is always revalidated
// before use, so filtered/reindexed callers fall back to structural matching.
int g_fp_nds_hook_864_evidence_by_sequence_id[];
string g_fp_nds_hook_864_evidence_symbol = "";
ENUM_TIMEFRAMES g_fp_nds_hook_864_evidence_period = PERIOD_CURRENT;
datetime g_fp_nds_hook_864_evidence_captured_at = 0;
bool g_fp_nds_hook_864_evidence_ready = false;

void FP_ResetNDSHook864CycleR1Evidence(FP_NDSHook864CycleR1Evidence &e)
{
   e.valid = false;
   e.status = "RESET";
   e.sequence_id = -1;
   e.scale_l = 0;
   e.origin_node_id = -1;
   e.origin_time = 0;
   e.direction = FP_HOOK_P02_DIRECTION_POSITIVE;
   e.x_count = 0;
   e.x1_node_id = -1;
   e.x2_node_id = -1;
   e.x3_node_id = -1;
   e.x4_node_id = -1;
   e.crown_node_id = -1;
   e.crown_time = 0;
   e.origin_price = 0.0;
   e.crown_price = 0.0;
   e.entry_price = 0.0;
   e.phase04_record_valid = false;
   e.x_closure_candidate = false;
   e.x_closed = false;
   e.x_closure_time = 0;
   e.x_closure_bar_index = -1;
   e.x_closure_price = 0.0;
   e.x_closure_threshold_price = 0.0;
   e.x_closure_reference_y_price = 0.0;
   e.x_closure_reference_y_time = 0;
   e.origin_return_penetrated = false;
   e.death_time = 0;
   e.death_bar_index = -1;
   e.death_price = 0.0;
   e.level_touched_after_closure = false;
   e.first_touch_time = 0;
   e.first_touch_bar_index = -1;
   e.first_touch_price = 0.0;
}

double FP_NDSHook864CycleR1RawEntryFromPrices(const double crown_price,
                                               const double origin_price,
                                               const double ratio)
{
   return crown_price + ratio * (origin_price - crown_price);
}

double FP_NDSHook864CycleR1RawEntryFromSequence(const FP_HookPhase02Sequence &seq,
                                                 const double ratio)
{
   return FP_NDSHook864CycleR1RawEntryFromPrices(seq.cycle_crown_price,
                                                 seq.origin_price,
                                                 ratio);
}

void FP_NDSClearHook864CycleR1EvidenceSnapshot()
{
   ArrayResize(g_fp_nds_hook_864_evidence, 0);
   ArrayResize(g_fp_nds_hook_864_evidence_by_sequence_id, 0);
   g_fp_nds_hook_864_evidence_symbol = "";
   g_fp_nds_hook_864_evidence_period = PERIOD_CURRENT;
   g_fp_nds_hook_864_evidence_captured_at = 0;
   g_fp_nds_hook_864_evidence_ready = false;
}

int FP_NDSHook864CycleR1LowerBoundTime(const MqlRates &rates[],
                                      const int count,
                                      const datetime target)
{
   int left = 0;
   int right = count;
   while(left < right)
   {
      int middle = left + (right - left) / 2;
      if(rates[middle].time < target)
         left = middle + 1;
      else
         right = middle;
   }
   return left;
}

bool FP_NDSHook864CycleR1FindFirstTouch(const MqlRates &rates[],
                                        const int copied,
                                        const FP_HookPhase02Direction direction,
                                        const datetime closure_time,
                                        const double entry_price,
                                        int &bar_index,
                                        datetime &bar_time,
                                        double &touch_price)
{
   bar_index = -1;
   bar_time = 0;
   touch_price = 0.0;
   if(closure_time <= 0 || entry_price <= 0.0)
      return false;

   int n = MathMin(copied, ArraySize(rates));
   int first = FP_NDSHook864CycleR1LowerBoundTime(rates, n, closure_time);
   for(int i=first; i<n; i++)
   {
      // Include the closure candle. If 50% closure and the 86.4 level occur in
      // the same closed candle, the strategy could not have placed the order
      // after observing closure; that arrival is therefore already consumed.
      if(direction == FP_HOOK_P02_DIRECTION_POSITIVE)
      {
         if(rates[i].low <= entry_price)
         {
            bar_index = i;
            bar_time = rates[i].time;
            touch_price = rates[i].low;
            return true;
         }
      }
      else if(direction == FP_HOOK_P02_DIRECTION_NEGATIVE)
      {
         if(rates[i].high >= entry_price)
         {
            bar_index = i;
            bar_time = rates[i].time;
            touch_price = rates[i].high;
            return true;
         }
      }
   }
   return false;
}

void FP_NDSCaptureHook864CycleR1EvidenceSnapshot(const string symbol,
                                                  const ENUM_TIMEFRAMES period,
                                                  const MqlRates &rates[],
                                                  const int copied,
                                                  const FP_HookPhase04Record &records[])
{
   FP_NDSClearHook864CycleR1EvidenceSnapshot();

   int count = ArraySize(records);
   ArrayResize(g_fp_nds_hook_864_evidence, count);

   int max_sequence_id = -1;
   for(int m=0; m<count; m++)
   {
      int candidate_id = records[m].p03.sequence.sequence_id;
      if(candidate_id > max_sequence_id)
         max_sequence_id = candidate_id;
   }
   if(max_sequence_id >= 0 && max_sequence_id <= 1000000)
   {
      ArrayResize(g_fp_nds_hook_864_evidence_by_sequence_id, max_sequence_id + 1);
      ArrayInitialize(g_fp_nds_hook_864_evidence_by_sequence_id, -1);
   }
   for(int i=0; i<count; i++)
   {
      FP_NDSHook864CycleR1Evidence e;
      FP_ResetNDSHook864CycleR1Evidence(e);

      FP_HookPhase04Record rec = records[i];
      FP_HookPhase02Sequence seq = rec.p03.sequence;
      FP_HookPhase04Lifecycle life = rec.lifecycle;

      e.sequence_id = seq.sequence_id;
      e.scale_l = seq.scale_l;
      e.origin_node_id = seq.origin_node_id;
      e.origin_time = seq.origin_time;
      e.direction = seq.direction;
      e.x_count = seq.x_count;
      e.x1_node_id = seq.x1_node_id;
      e.x2_node_id = seq.x2_node_id;
      e.x3_node_id = seq.x3_node_id;
      e.x4_node_id = seq.x4_node_id;
      e.crown_node_id = seq.cycle_crown_node_id;
      e.crown_time = seq.cycle_crown_time;
      e.origin_price = seq.origin_price;
      e.crown_price = seq.cycle_crown_price;
      e.entry_price = FP_NDSHook864CycleR1RawEntryFromSequence(seq,
                                                               FP_NDS_HOOK_864_ENTRY_RATIO);
      e.phase04_record_valid = rec.valid;
      e.x_closure_candidate = life.x_closure_candidate;
      e.x_closed = life.x_closed;
      e.x_closure_time = life.x_closure_time;
      e.x_closure_bar_index = life.x_closure_bar_index;
      e.x_closure_price = life.x_closure_price;
      e.x_closure_threshold_price = life.x_closure_threshold_price;
      e.x_closure_reference_y_price = life.x_closure_reference_y_price;
      e.x_closure_reference_y_time = life.x_closure_reference_y_time;
      e.origin_return_penetrated = life.origin_return_penetrated;
      e.death_time = life.death_time;
      e.death_bar_index = life.death_bar_index;
      e.death_price = life.death_price;

      // Dominating invalid/death gates are resolved before the historical
      // first-touch scan. A dead or invalid cycle can never own an order, so
      // scanning its remaining history would add cost without decision value.
      if(!e.phase04_record_valid)
         e.status = "PHASE04_RECORD_INVALID";
      else if(e.origin_return_penetrated)
         e.status = "CYCLE_DEAD_BY_ORIGIN_RETURN";
      else if(!e.x_closure_candidate)
         e.status = "PHASE04_NOT_X_CLOSURE_CANDIDATE";
      else if(!e.x_closed)
         e.status = "PHASE04_X_NOT_CLOSED";
      else
      {
         e.level_touched_after_closure = FP_NDSHook864CycleR1FindFirstTouch(
            rates, copied, e.direction, e.x_closure_time, e.entry_price,
            e.first_touch_bar_index, e.first_touch_time, e.first_touch_price);

         if(e.level_touched_after_closure)
            e.status = "HOOK_864_FIRST_ARRIVAL_ALREADY_CONSUMED";
         else
         {
            e.status = "PHASE04_X_CLOSED_BEFORE_FIRST_864_TOUCH";
            e.valid = true;
         }
      }

      g_fp_nds_hook_864_evidence[i] = e;
      if(e.sequence_id >= 0 &&
         e.sequence_id < ArraySize(g_fp_nds_hook_864_evidence_by_sequence_id))
      {
         int prior = g_fp_nds_hook_864_evidence_by_sequence_id[e.sequence_id];
         g_fp_nds_hook_864_evidence_by_sequence_id[e.sequence_id] =
            (prior == -1 ? i : -2);
      }
   }

   g_fp_nds_hook_864_evidence_symbol = symbol;
   g_fp_nds_hook_864_evidence_period = period;
   g_fp_nds_hook_864_evidence_captured_at = TimeCurrent();
   g_fp_nds_hook_864_evidence_ready = true;
}

bool FP_NDSHook864CycleR1EvidenceSnapshotMatches(const string symbol,
                                                  const ENUM_TIMEFRAMES period)
{
   return (g_fp_nds_hook_864_evidence_ready &&
           g_fp_nds_hook_864_evidence_symbol == symbol &&
           g_fp_nds_hook_864_evidence_period == period);
}

int FP_NDSCopyHook864CycleR1EvidenceSnapshot(FP_NDSHook864CycleR1Evidence &target[])
{
   int count = ArraySize(g_fp_nds_hook_864_evidence);
   ArrayResize(target, count);
   for(int i=0; i<count; i++)
      target[i] = g_fp_nds_hook_864_evidence[i];
   return count;
}

bool FP_NDSHook864CycleR1EvidenceIdentityMatches(
   const FP_NDSHook864CycleR1Evidence &candidate,
   const FP_HookPhase02Sequence &seq)
{
   const double epsilon = 1e-10;
   if(candidate.scale_l != seq.scale_l) return false;
   if(candidate.origin_node_id != seq.origin_node_id) return false;
   if(candidate.origin_time != seq.origin_time) return false;
   if(candidate.direction != seq.direction) return false;
   if(candidate.x_count != seq.x_count) return false;
   if(candidate.x1_node_id != seq.x1_node_id) return false;
   if(candidate.x2_node_id != seq.x2_node_id) return false;
   if(candidate.x3_node_id != seq.x3_node_id) return false;
   if(candidate.x4_node_id != seq.x4_node_id) return false;
   if(candidate.crown_node_id != seq.cycle_crown_node_id) return false;
   if(candidate.crown_time != seq.cycle_crown_time) return false;
   if(MathAbs(candidate.origin_price - seq.origin_price) > epsilon) return false;
   if(MathAbs(candidate.crown_price - seq.cycle_crown_price) > epsilon) return false;
   return true;
}

bool FP_NDSFindHook864CycleR1Evidence(const string symbol,
                                      const ENUM_TIMEFRAMES period,
                                      const FP_HookPhase02Sequence &seq,
                                      FP_NDSHook864CycleR1Evidence &evidence)
{
   FP_ResetNDSHook864CycleR1Evidence(evidence);
   if(!FP_NDSHook864CycleR1EvidenceSnapshotMatches(symbol, period))
   {
      evidence.status = "PHASE04_EVIDENCE_SNAPSHOT_NOT_READY";
      return false;
   }

   if(seq.sequence_id >= 0 &&
      seq.sequence_id < ArraySize(g_fp_nds_hook_864_evidence_by_sequence_id))
   {
      int hinted_index = g_fp_nds_hook_864_evidence_by_sequence_id[seq.sequence_id];
      if(hinted_index >= 0 && hinted_index < ArraySize(g_fp_nds_hook_864_evidence))
      {
         FP_NDSHook864CycleR1Evidence hinted = g_fp_nds_hook_864_evidence[hinted_index];
         if(FP_NDSHook864CycleR1EvidenceIdentityMatches(hinted, seq))
         {
            evidence = hinted;
            return true;
         }
      }
   }

   for(int i=0; i<ArraySize(g_fp_nds_hook_864_evidence); i++)
   {
      FP_NDSHook864CycleR1Evidence candidate = g_fp_nds_hook_864_evidence[i];
      if(!FP_NDSHook864CycleR1EvidenceIdentityMatches(candidate, seq))
         continue;
      evidence = candidate;
      return true;
   }

   evidence.status = "PHASE04_EVIDENCE_NOT_FOUND_FOR_SEQUENCE";
   return false;
}

#endif // __FP_NDS_HOOK_864_CYCLE_R1_EVIDENCE_MQH__
