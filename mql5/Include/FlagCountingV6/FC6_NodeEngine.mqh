#ifndef __FC6_NODE_ENGINE_MQH__
#define __FC6_NODE_ENGINE_MQH__
#property strict
#include "FC6_Types.mqh"

// ============================================================================
// V6 Node Engine
// ----------------------------------------------------------------------------
// Implements the project L-rule:
//   - Node candidates are candle HIGH/LOW prices.
//   - A HIGH node is valid when at least L candles to the left and L candles to
//     the right do not reach above it. Equal prices are not a break.
//   - A LOW node is valid when at least L candles to the left and L candles to
//     the right do not reach below it. Equal prices are not a break.
//   - Equal highs/lows are merged into one plateau node. The node anchor for
//     drawing is the last equal touch, while the identity stores the whole
//     plateau time interval.
//   - Nodes do not expire; an unconfirmed/pending node simply waits for enough
//     right-side bars.
// ============================================================================

int FC6_AddNode(FC6_Node &nodes[], FC6_Node &n)
{
   int sz = ArraySize(nodes);
   n.id = sz;
   ArrayResize(nodes, sz + 1);
   nodes[sz] = n;
   return sz;
}

bool FC6_LeftRightOkHigh(const MqlRates &rates[], const int count, const int i, const int L)
{
   if(i < L) return false;
   double p = rates[i].high;
   for(int j=i-L; j<i; j++)
      if(rates[j].high > p) return false;
   int available_right = MathMin(L, count - i - 1);
   for(int j=i+1; j<=i+available_right; j++)
      if(rates[j].high > p) return false;
   return true;
}

bool FC6_LeftRightOkLow(const MqlRates &rates[], const int count, const int i, const int L)
{
   if(i < L) return false;
   double p = rates[i].low;
   for(int j=i-L; j<i; j++)
      if(rates[j].low < p) return false;
   int available_right = MathMin(L, count - i - 1);
   for(int j=i+1; j<=i+available_right; j++)
      if(rates[j].low < p) return false;
   return true;
}

bool FC6_NodeConfirmedByRight(const int count, const int i, const int L)
{
   return (count - i - 1) >= L;
}

void FC6_MergeEqualPlateauNode(FC6_Node &nodes[], FC6_Node &candidate, const double eps)
{
   int sz = ArraySize(nodes);
   if(sz <= 0)
   {
      FC6_AddNode(nodes, candidate);
      return;
   }

   FC6_Node last = nodes[sz - 1];
   if(last.kind == candidate.kind && FC6_PriceEqual(last.price, candidate.price, eps))
   {
      // Same plateau. Preserve the first touch as start and use the latest touch
      // as the drawing anchor. Confirmation only becomes true when the latest
      // representative has enough right bars.
      nodes[sz - 1].index_end = candidate.index_end;
      nodes[sz - 1].index_anchor = candidate.index_anchor;
      nodes[sz - 1].time_end = candidate.time_end;
      nodes[sz - 1].time_anchor = candidate.time_anchor;
      nodes[sz - 1].confirmed = candidate.confirmed;
      return;
   }

   FC6_AddNode(nodes, candidate);
}

int FC6_BuildLRuleNodes(const MqlRates &rates[],
                        const int count,
                        const int L,
                        const bool include_pending,
                        const double eps,
                        FC6_Node &nodes[])
{
   ArrayResize(nodes, 0);
   if(count <= 2 * L + 2) return 0;

   for(int i=L; i<count; i++)
   {
      bool confirmed = FC6_NodeConfirmedByRight(count, i, L);
      if(!confirmed && !include_pending) continue;

      if(FC6_LeftRightOkHigh(rates, count, i, L))
      {
         FC6_Node n = FC6_MakeNode(-1,
                                   L,
                                   FC6_NODE_HIGH,
                                   i,
                                   i,
                                   i,
                                   rates[i].time,
                                   rates[i].time,
                                   rates[i].time,
                                   rates[i].high,
                                   confirmed);
         FC6_MergeEqualPlateauNode(nodes, n, eps);
      }

      if(FC6_LeftRightOkLow(rates, count, i, L))
      {
         FC6_Node n = FC6_MakeNode(-1,
                                   L,
                                   FC6_NODE_LOW,
                                   i,
                                   i,
                                   i,
                                   rates[i].time,
                                   rates[i].time,
                                   rates[i].time,
                                   rates[i].low,
                                   confirmed);
         FC6_MergeEqualPlateauNode(nodes, n, eps);
      }
   }

   // Re-id after plateau merging.
   for(int k=0; k<ArraySize(nodes); k++)
      nodes[k].id = k;

   return ArraySize(nodes);
}

bool FC6_NodeMoreExtreme(const FC6_Node &a, const FC6_Node &b)
{
   if(a.kind == FC6_NODE_HIGH) return a.price > b.price;
   if(a.kind == FC6_NODE_LOW)  return a.price < b.price;
   return false;
}

void FC6_MergeSameKindRun(FC6_Node &out[], FC6_Node &candidate, const double eps)
{
   int sz = ArraySize(out);
   if(sz <= 0)
   {
      FC6_AddNode(out, candidate);
      return;
   }

   FC6_Node last = out[sz - 1];
   if(last.kind != candidate.kind)
   {
      FC6_AddNode(out, candidate);
      return;
   }

   // Consecutive same-kind structural nodes are one swing-run at this view.
   // Equal is merged as a plateau; strictly more extreme replaces the anchor.
   if(FC6_PriceEqual(last.price, candidate.price, eps))
   {
      out[sz - 1].index_end = candidate.index_end;
      out[sz - 1].time_end = candidate.time_end;
      out[sz - 1].index_anchor = candidate.index_anchor;
      out[sz - 1].time_anchor = candidate.time_anchor;
      out[sz - 1].confirmed = (last.confirmed && candidate.confirmed);
      return;
   }

   if(FC6_NodeMoreExtreme(candidate, last))
   {
      candidate.index_start = last.index_start;
      candidate.time_start = last.time_start;
      out[sz - 1] = candidate;
      out[sz - 1].id = sz - 1;
   }
}

int FC6_BuildAlternatingView(const FC6_Node &nodes[], const int node_count, const double eps, FC6_Node &view[])
{
   ArrayResize(view, 0);
   for(int i=0; i<node_count; i++)
   {
      FC6_Node n = nodes[i];
      FC6_MergeSameKindRun(view, n, eps);
   }
   for(int k=0; k<ArraySize(view); k++) view[k].id = k;
   return ArraySize(view);
}

int FC6_BuildScaleList(const bool use_multi,
                       const int L1,
                       const int L2,
                       const int L3,
                       const int L4,
                       const int L5,
                       const int L6,
                       const int L7,
                       const int L8,
                       int &scales[])
{
   ArrayResize(scales, 0);
   int raw[8];
   raw[0] = L1; raw[1] = L2; raw[2] = L3; raw[3] = L4;
   raw[4] = L5; raw[5] = L6; raw[6] = L7; raw[7] = L8;
   int limit = use_multi ? 8 : 1;
   for(int i=0; i<limit; i++)
   {
      int L = raw[i];
      if(L <= 0) continue;
      bool exists = false;
      for(int j=0; j<ArraySize(scales); j++)
         if(scales[j] == L) exists = true;
      if(!exists)
      {
         int sz = ArraySize(scales);
         ArrayResize(scales, sz + 1);
         scales[sz] = L;
      }
   }

   // Insertion sort ascending.
   for(int i=1; i<ArraySize(scales); i++)
   {
      int key = scales[i];
      int j = i - 1;
      while(j >= 0 && scales[j] > key)
      {
         scales[j + 1] = scales[j];
         j--;
      }
      scales[j + 1] = key;
   }
   return ArraySize(scales);
}

int FC6_FindNodePositionByAnchor(const FC6_Node &nodes[], const int count, const FC6_Node &needle)
{
   for(int i=0; i<count; i++)
   {
      if(nodes[i].kind == needle.kind &&
         nodes[i].time_anchor == needle.time_anchor &&
         nodes[i].index_anchor == needle.index_anchor &&
         MathAbs(nodes[i].price - needle.price) <= 0.0)
         return i;
   }
   return -1;
}

int FC6_FirstNodeAfterIndex(const FC6_Node &nodes[], const int count, const int anchor_index)
{
   for(int i=0; i<count; i++)
      if(nodes[i].index_anchor > anchor_index)
         return i;
   return -1;
}

#endif // __FC6_NODE_ENGINE_MQH__
