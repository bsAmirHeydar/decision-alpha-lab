#ifndef __FP_NODE_CANONICALIZER_MQH__
#define __FP_NODE_CANONICALIZER_MQH__
#property strict

#include "FP_NodeClearance.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 02 / Node Canonicalization
// ----------------------------------------------------------------------------
// Owns stable chronological ordering, identity re-numbering, and same-side run
// compression. Later layers consume only this canonical node stream.
// ============================================================================

void FP_BuildNodeFromPlateau(const MqlRates &rates[],
                             const int L,
                             const int kind,
                             const int start,
                             const int end,
                             const double price,
                             const bool confirmed,
                             const int id,
                             FP_Node &n)
{
   FP_ResetNode(n);
   n.id = id;
   n.L = L;
   n.kind = kind;
   n.index_start = start;
   n.index_end = end;
   // Stable anchor policy: last equal touch of the contiguous plateau.
   n.index_anchor = end;
   n.time_start = rates[start].time;
   n.time_end = rates[end].time;
   n.time_anchor = rates[end].time;
   n.price = price;
   n.confirmed = confirmed;
   n.is_confirmed = confirmed;
   n.is_live_pending = !confirmed;
   n.source = (confirmed ? FP_NODE_SOURCE_CONFIRMED_HISTORY : FP_NODE_SOURCE_LIVE_CANDIDATE);
   n.plateau_start_index = start;
   n.plateau_end_index = end;
}

void FP_SortNodes(FP_Node &nodes[])
{
   int n = ArraySize(nodes);
   for(int i=0; i<n-1; i++)
   {
      int best = i;
      for(int j=i+1; j<n; j++)
      {
         if(nodes[j].index_anchor < nodes[best].index_anchor) best = j;
         else if(nodes[j].index_anchor == nodes[best].index_anchor && nodes[j].kind > nodes[best].kind) best = j;
         else if(nodes[j].index_anchor == nodes[best].index_anchor && nodes[j].kind == nodes[best].kind && nodes[j].price > nodes[best].price) best = j;
      }
      if(best != i)
      {
         FP_Node tmp = nodes[i];
         nodes[i] = nodes[best];
         nodes[best] = tmp;
      }
   }
   for(int k=0; k<n; k++) nodes[k].id = k;
}

bool FP_NodeIsMoreExtreme(const FP_Node &candidate, const FP_Node &current)
{
   if(candidate.kind == FP_NODE_HIGH) return (candidate.price > current.price);
   if(candidate.kind == FP_NODE_LOW)  return (candidate.price < current.price);
   return false;
}

void FP_UpdateNodeExtractReportAfterNode(FP_NodeExtractReport &r, const FP_Node &n)
{
   r.emitted_nodes++;
   if(n.confirmed) r.confirmed_nodes++;
   else r.pending_nodes++;
   if(n.kind == FP_NODE_HIGH) r.high_nodes++;
   else if(n.kind == FP_NODE_LOW) r.low_nodes++;

   if(r.first_anchor_index < 0 || n.index_anchor < r.first_anchor_index)
   {
      r.first_anchor_index = n.index_anchor;
      r.first_anchor_time = n.time_anchor;
   }
   if(r.last_anchor_index < 0 || n.index_anchor > r.last_anchor_index)
   {
      r.last_anchor_index = n.index_anchor;
      r.last_anchor_time = n.time_anchor;
   }
}

void FP_UpdateNodeCompressReportAfterNode(FP_NodeCompressReport &r, const FP_Node &n)
{
   if(n.confirmed) r.confirmed_nodes_out++;
   else r.pending_nodes_out++;
   if(n.kind == FP_NODE_HIGH) r.high_nodes_out++;
   else if(n.kind == FP_NODE_LOW) r.low_nodes_out++;

   if(r.first_anchor_index < 0 || n.index_anchor < r.first_anchor_index)
   {
      r.first_anchor_index = n.index_anchor;
      r.first_anchor_time = n.time_anchor;
   }
   if(r.last_anchor_index < 0 || n.index_anchor > r.last_anchor_index)
   {
      r.last_anchor_index = n.index_anchor;
      r.last_anchor_time = n.time_anchor;
   }
}

int FP_CompressAlternatingExtremeWithReport(const FP_Node &nodes[],
                                            const int node_count,
                                            FP_Node &out_nodes[],
                                            FP_NodeCompressReport &report)
{
   ArrayResize(out_nodes, 0);
   FP_ResetNodeCompressReport(report);
   report.raw_count = node_count;
   if(node_count <= 0)
   {
      report.ok = true;
      report.status = "empty";
      report.reason = "no_nodes_to_compress";
      return 0;
   }

   report.L = nodes[0].L;
   FP_Node current = nodes[0];
   bool has_current = true;

   for(int i=1; i<node_count; i++)
   {
      if(!has_current)
      {
         current = nodes[i];
         has_current = true;
         continue;
      }

      if(nodes[i].kind == current.kind)
      {
         report.same_side_runs++;
         if(FP_NodeIsMoreExtreme(nodes[i], current))
         {
            current = nodes[i];
            report.replaced_by_more_extreme++;
         }
         else
         {
            report.discarded_less_extreme++;
         }
      }
      else
      {
         FP_AddNode(out_nodes, current);
         FP_UpdateNodeCompressReportAfterNode(report, current);
         report.alternating_boundaries++;
         current = nodes[i];
      }
   }

   if(has_current)
   {
      FP_AddNode(out_nodes, current);
      FP_UpdateNodeCompressReportAfterNode(report, current);
   }

   for(int k=0; k<ArraySize(out_nodes); k++) out_nodes[k].id = k;
   report.compressed_count = ArraySize(out_nodes);
   report.ok = true;
   report.status = "ok";
   report.reason = "canonical_alternating_nodes_ready";
   return report.compressed_count;
}

int FP_CompressAlternatingExtreme(const FP_Node &nodes[], const int node_count, FP_Node &out_nodes[])
{
   FP_NodeCompressReport report;
   return FP_CompressAlternatingExtremeWithReport(nodes, node_count, out_nodes, report);
}

bool FP_NodeArrayIsChronological(const FP_Node &nodes[], const int node_count, int &bad_index)
{
   bad_index = -1;
   for(int i=1; i<node_count; i++)
   {
      if(nodes[i].index_anchor < nodes[i - 1].index_anchor)
      {
         bad_index = i;
         return false;
      }
   }
   return true;
}

int FP_FindNodePositionById(const FP_Node &nodes[], const int node_count, const int id)
{
   for(int i=0; i<node_count; i++)
      if(nodes[i].id == id) return i;
   return -1;
}

int FP_FindNodePositionByAnchor(const FP_Node &nodes[], const int node_count, const int anchor_index, const int kind)
{
   for(int i=0; i<node_count; i++)
      if(nodes[i].index_anchor == anchor_index && nodes[i].kind == kind) return i;
   return -1;
}

#endif // __FP_NODE_CANONICALIZER_MQH__
