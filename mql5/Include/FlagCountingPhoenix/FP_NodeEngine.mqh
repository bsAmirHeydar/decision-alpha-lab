#ifndef __FP_NODE_ENGINE_MQH__
#define __FP_NODE_ENGINE_MQH__
#property strict

#include "FP_NodeAudit.mqh"

// ============================================================================
// Phoenix Node Engine - Level 02 Facade
// ----------------------------------------------------------------------------
// Public contract:
// - rates[] must already be canonical Level 01 bars: oldest -> newest.
// - Structural inputs are high/low only.
// - L means at least L real non-reaching candles to the left and right.
// - Equal prices are not breaks and do not count as clearance.
// - Adjacent equal highs/lows are one plateau node.
// - Anchor policy is stable: last equal touch in the plateau.
// - Confirmed and live-pending nodes are explicitly tagged and auditable.
// ============================================================================

void FP_NodeRejectLeft(FP_NodeExtractReport &report, const int status)
{
   report.rejected_left++;
   if(status == FP_NODE_CLEARANCE_BROKEN) report.left_broken++;
   else if(status == FP_NODE_CLEARANCE_NOT_ENOUGH) report.left_not_enough++;
}

void FP_NodeRejectRight(FP_NodeExtractReport &report, const int status, const bool include_pending)
{
   if(status == FP_NODE_CLEARANCE_PENDING && !include_pending)
   {
      report.rejected_pending_not_allowed++;
      report.right_pending++;
      return;
   }

   report.rejected_right++;
   if(status == FP_NODE_CLEARANCE_BROKEN) report.right_broken++;
   else if(status == FP_NODE_CLEARANCE_PENDING) report.right_pending++;
}

bool FP_TryEmitNodeFromPlateau(const MqlRates &rates[],
                               const int total,
                               const int L,
                               const int kind,
                               const int start,
                               const int end,
                               const double price,
                               const bool include_pending,
                               const double eps,
                               int &next_id,
                               FP_Node &nodes[],
                               FP_NodeExtractReport &report)
{
   int left_count = 0;
   int left_eq = 0;
   int left_blocked = -1;
   int right_count = 0;
   int right_eq = 0;
   int right_blocked = -1;

   int left_status = FP_NODE_CLEARANCE_NONE;
   int right_status = FP_NODE_CLEARANCE_NONE;

   if(kind == FP_NODE_HIGH)
   {
      left_status = FP_ScanHighLeftClearance(rates, total, start, price, L, eps, left_count, left_eq, left_blocked);
      right_status = FP_ScanHighRightClearance(rates, total, end, price, L, eps, right_count, right_eq, right_blocked);
   }
   else if(kind == FP_NODE_LOW)
   {
      left_status = FP_ScanLowLeftClearance(rates, total, start, price, L, eps, left_count, left_eq, left_blocked);
      right_status = FP_ScanLowRightClearance(rates, total, end, price, L, eps, right_count, right_eq, right_blocked);
   }
   else
   {
      report.rejected_invalid_params++;
      return false;
   }

   report.equality_touches_skipped += left_eq + right_eq;

   if(left_status != FP_NODE_CLEARANCE_OK)
   {
      FP_NodeRejectLeft(report, left_status);
      return false;
   }

   bool right_ok = (right_status == FP_NODE_CLEARANCE_OK);
   bool right_pending = (right_status == FP_NODE_CLEARANCE_PENDING);
   if(!right_ok && !(include_pending && right_pending))
   {
      FP_NodeRejectRight(report, right_status, include_pending);
      return false;
   }

   FP_Node n;
   FP_BuildNodeFromPlateau(rates, L, kind, start, end, price, right_ok, next_id, n);
   FP_AddNode(nodes, n);
   FP_UpdateNodeExtractReportAfterNode(report, n);
   next_id++;
   return true;
}

int FP_ExtractNodesForLWithReport(const MqlRates &rates[],
                                  const int total,
                                  const FP_NodeExtractConfig &cfg,
                                  FP_Node &nodes[],
                                  FP_NodeExtractReport &report)
{
   ArrayResize(nodes, 0);
   FP_ResetNodeExtractReport(report);
   report.L = cfg.L;
   report.total_bars = total;
   report.include_pending = cfg.include_pending;
   report.epsilon_points = cfg.epsilon_points;
   report.epsilon_price = FP_EpsilonPrice(cfg.epsilon_points);

   if(cfg.L < 1)
   {
      report.ok = false;
      report.status = "invalid_L";
      report.reason = "L_must_be_positive";
      report.rejected_invalid_params++;
      return 0;
   }

   if(total <= (2 * cfg.L + 1))
   {
      report.ok = true;
      report.status = "not_enough_bars_for_L";
      report.reason = "total_bars_below_minimum_for_left_right_clearance";
      return 0;
   }

   double eps = report.epsilon_price;
   int next_id = 0;

   for(int i=0; i<total; i++)
   {
      int hs = 0;
      int he = 0;
      FP_FindHighPlateau(rates, total, i, eps, hs, he);
      if(i == hs)
      {
         FP_NodeReportPlateau(report, FP_NODE_HIGH, hs, he);
         FP_TryEmitNodeFromPlateau(rates,
                                   total,
                                   cfg.L,
                                   FP_NODE_HIGH,
                                   hs,
                                   he,
                                   rates[i].high,
                                   cfg.include_pending,
                                   eps,
                                   next_id,
                                   nodes,
                                   report);
      }

      int ls = 0;
      int le = 0;
      FP_FindLowPlateau(rates, total, i, eps, ls, le);
      if(i == ls)
      {
         FP_NodeReportPlateau(report, FP_NODE_LOW, ls, le);
         FP_TryEmitNodeFromPlateau(rates,
                                   total,
                                   cfg.L,
                                   FP_NODE_LOW,
                                   ls,
                                   le,
                                   rates[i].low,
                                   cfg.include_pending,
                                   eps,
                                   next_id,
                                   nodes,
                                   report);
      }
   }

   FP_SortNodes(nodes);

   int bad_index = -1;
   if(!FP_NodeArrayIsChronological(nodes, ArraySize(nodes), bad_index))
   {
      report.ok = false;
      report.status = "node_order_failed";
      report.reason = "node_array_not_chronological_after_sort";
      return ArraySize(nodes);
   }

   report.emitted_nodes = ArraySize(nodes);
   report.ok = true;
   report.status = "ok";
   report.reason = "raw_nodes_ready";
   return ArraySize(nodes);
}

int FP_ExtractNodesForL(const MqlRates &rates[],
                        const int total,
                        const int L,
                        const bool include_pending,
                        const double epsilon_points,
                        FP_Node &nodes[])
{
   FP_NodeExtractConfig cfg;
   FP_DefaultNodeExtractConfig(cfg);
   cfg.L = L;
   cfg.include_pending = include_pending;
   cfg.epsilon_points = epsilon_points;

   FP_NodeExtractReport report;
   return FP_ExtractNodesForLWithReport(rates, total, cfg, nodes, report);
}

int FP_BuildCanonicalNodesForScale(const MqlRates &rates[],
                                   const int total,
                                   const int scale_L,
                                   const bool include_pending,
                                   const double epsilon_points,
                                   FP_Node &raw_nodes[],
                                   FP_Node &canonical_nodes[],
                                   FP_NodeExtractReport &extract_report,
                                   FP_NodeCompressReport &compress_report)
{
   FP_NodeExtractConfig cfg;
   FP_DefaultNodeExtractConfig(cfg);
   cfg.L = scale_L;
   cfg.include_pending = include_pending;
   cfg.epsilon_points = epsilon_points;

   int raw_count = FP_ExtractNodesForLWithReport(rates, total, cfg, raw_nodes, extract_report);
   FP_CompressAlternatingExtremeWithReport(raw_nodes, raw_count, canonical_nodes, compress_report);
   return ArraySize(canonical_nodes);
}

#endif // __FP_NODE_ENGINE_MQH__
