#ifndef __FP_NODE_AUDIT_MQH__
#define __FP_NODE_AUDIT_MQH__
#property strict

#include "FP_NodeScaleList.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 02 / Node Audit Printers
// ----------------------------------------------------------------------------
// Standalone node evidence. These logs prove node extraction independently from
// Hook/F/renderer output.
// ============================================================================

string FP_NodeAuditTime(const datetime t)
{
   if(t <= 0) return "none";
   return TimeToString(t, TIME_DATE|TIME_SECONDS);
}

string FP_NodeFullAudit(const FP_Node &n)
{
   if(n.id < 0) return "none";
   return FP_NodeKindName(n.kind) + "#" + IntegerToString(n.id) +
          " L" + IntegerToString(n.L) +
          " src=" + FP_NodeSourceName(n.source) +
          " confirmed=" + FP_BoolName(n.confirmed) +
          " pending=" + FP_BoolName(n.is_live_pending) +
          " anchor=" + IntegerToString(n.index_anchor) +
          " plateau=" + IntegerToString(n.index_start) + "-" + IntegerToString(n.index_end) +
          " time=" + FP_NodeAuditTime(n.time_anchor) +
          " price=" + DoubleToString(n.price, _Digits);
}

void FP_PrintNodeExtractReport(const string tag, const FP_NodeExtractReport &r)
{
   Print(tag,
         " status=", r.status,
         " ok=", FP_BoolName(r.ok),
         " reason=", r.reason,
         " L=", r.L,
         " bars=", r.total_bars,
         " include_pending=", FP_BoolName(r.include_pending),
         " eps_points=", DoubleToString(r.epsilon_points, 2),
         " eps_price=", DoubleToString(r.epsilon_price, _Digits),
         " high_plateaus=", r.candidate_high_plateaus,
         " low_plateaus=", r.candidate_low_plateaus,
         " raw_candidates=", r.raw_candidates,
         " emitted=", r.emitted_nodes,
         " confirmed=", r.confirmed_nodes,
         " pending=", r.pending_nodes,
         " highs=", r.high_nodes,
         " lows=", r.low_nodes,
         " reject_left=", r.rejected_left,
         " reject_right=", r.rejected_right,
         " reject_pending=", r.rejected_pending_not_allowed,
         " left_broken=", r.left_broken,
         " right_broken=", r.right_broken,
         " left_not_enough=", r.left_not_enough,
         " right_pending=", r.right_pending,
         " eq_skips=", r.equality_touches_skipped,
         " max_plateau_width=", r.plateau_max_width,
         " first_anchor=", r.first_anchor_index,
         " last_anchor=", r.last_anchor_index,
         " first_time=", FP_NodeAuditTime(r.first_anchor_time),
         " last_time=", FP_NodeAuditTime(r.last_anchor_time));
}

void FP_PrintNodeCompressReport(const string tag, const FP_NodeCompressReport &r)
{
   Print(tag,
         " status=", r.status,
         " ok=", FP_BoolName(r.ok),
         " reason=", r.reason,
         " L=", r.L,
         " raw=", r.raw_count,
         " compressed=", r.compressed_count,
         " same_side_runs=", r.same_side_runs,
         " replaced_extreme=", r.replaced_by_more_extreme,
         " discarded_less_extreme=", r.discarded_less_extreme,
         " boundaries=", r.alternating_boundaries,
         " confirmed=", r.confirmed_nodes_out,
         " pending=", r.pending_nodes_out,
         " highs=", r.high_nodes_out,
         " lows=", r.low_nodes_out,
         " first_anchor=", r.first_anchor_index,
         " last_anchor=", r.last_anchor_index,
         " first_time=", FP_NodeAuditTime(r.first_anchor_time),
         " last_time=", FP_NodeAuditTime(r.last_anchor_time));
}

void FP_PrintNodeSamples(const string tag, const FP_Node &nodes[], const int node_count, const int sample_limit)
{
   int limit = sample_limit;
   if(limit < 1) limit = 1;
   if(limit > node_count) limit = node_count;

   if(node_count <= 0)
   {
      Print(tag, " no_node_samples total=0");
      return;
   }

   for(int i=0; i<limit; i++)
      Print(tag, " sample[", i, "] ", FP_NodeFullAudit(nodes[i]));

   if(node_count > limit)
      Print(tag, " sample_last ", FP_NodeFullAudit(nodes[node_count - 1]));
}

#endif // __FP_NODE_AUDIT_MQH__
