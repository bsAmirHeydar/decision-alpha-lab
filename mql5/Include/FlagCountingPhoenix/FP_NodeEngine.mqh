#ifndef __FP_NODE_ENGINE_MQH__
#define __FP_NODE_ENGINE_MQH__
#property strict

#include "FP_Types.mqh"

// ============================================================================
// Phoenix Node Engine
// ----------------------------------------------------------------------------
// Contract:
// - Nodes are built from candle highs/lows only.
// - L means at least L candles on the left and L candles on the right must NOT
//   reach the node price.
// - Equal high / equal low plateaus are one structural node.
// - Equal prices in the neighbour zone are skipped, not counted as confirming
//   candles and not counted as breaks.
// - Equality is never a break.
// - Node does not expire after confirmation.
// ============================================================================

void FP_FindHighPlateau(const MqlRates &rates[], const int total, const int i, const double eps, int &start, int &end)
{
   start = i;
   end = i;
   double p = rates[i].high;
   while(start > 0 && FP_AlmostEqual(rates[start - 1].high, p, eps)) start--;
   while(end + 1 < total && FP_AlmostEqual(rates[end + 1].high, p, eps)) end++;
}

void FP_FindLowPlateau(const MqlRates &rates[], const int total, const int i, const double eps, int &start, int &end)
{
   start = i;
   end = i;
   double p = rates[i].low;
   while(start > 0 && FP_AlmostEqual(rates[start - 1].low, p, eps)) start--;
   while(end + 1 < total && FP_AlmostEqual(rates[end + 1].low, p, eps)) end++;
}

bool FP_HighHasLeftL(const MqlRates &rates[], const int total, const int start, const double price, const int L, const double eps)
{
   int cnt = 0;
   for(int i = start - 1; i >= 0 && cnt < L; i--)
   {
      if(FP_BreaksAbove(rates[i].high, price, eps)) return false;
      if(FP_AlmostEqual(rates[i].high, price, eps)) continue;
      cnt++;
   }
   return (cnt >= L);
}

bool FP_HighHasRightL(const MqlRates &rates[], const int total, const int end, const double price, const int L, const double eps, bool &pending)
{
   int cnt = 0;
   pending = false;
   for(int i = end + 1; i < total && cnt < L; i++)
   {
      if(FP_BreaksAbove(rates[i].high, price, eps)) return false;
      if(FP_AlmostEqual(rates[i].high, price, eps)) continue;
      cnt++;
   }
   if(cnt >= L) return true;
   pending = true;
   return false;
}

bool FP_LowHasLeftL(const MqlRates &rates[], const int total, const int start, const double price, const int L, const double eps)
{
   int cnt = 0;
   for(int i = start - 1; i >= 0 && cnt < L; i--)
   {
      if(FP_BreaksBelow(rates[i].low, price, eps)) return false;
      if(FP_AlmostEqual(rates[i].low, price, eps)) continue;
      cnt++;
   }
   return (cnt >= L);
}

bool FP_LowHasRightL(const MqlRates &rates[], const int total, const int end, const double price, const int L, const double eps, bool &pending)
{
   int cnt = 0;
   pending = false;
   for(int i = end + 1; i < total && cnt < L; i++)
   {
      if(FP_BreaksBelow(rates[i].low, price, eps)) return false;
      if(FP_AlmostEqual(rates[i].low, price, eps)) continue;
      cnt++;
   }
   if(cnt >= L) return true;
   pending = true;
   return false;
}

void FP_BuildNodeFromPlateau(const MqlRates &rates[], const int L, const int kind, const int start, const int end, const double price, const bool confirmed, const int id, FP_Node &n)
{
   FP_ResetNode(n);
   n.id = id;
   n.L = L;
   n.kind = kind;
   n.index_start = start;
   n.index_end = end;
   // Anchor on the last equal touch. This is the point where price finally leaves
   // the plateau and the structural level becomes visually meaningful.
   n.index_anchor = end;
   n.time_start = rates[start].time;
   n.time_end = rates[end].time;
   n.time_anchor = rates[end].time;
   n.price = price;
   n.confirmed = confirmed;
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
      }
      if(best != i)
      {
         FP_Node tmp = nodes[i];
         nodes[i] = nodes[best];
         nodes[best] = tmp;
      }
   }
   // Re-id after sort so ids are chronological inside each L view.
   for(int k=0; k<n; k++) nodes[k].id = k;
}

int FP_ExtractNodesForL(const MqlRates &rates[], const int total, const int L, const bool include_pending, const double epsilon_points, FP_Node &nodes[])
{
   ArrayResize(nodes, 0);
   if(total <= (2 * L + 5) || L < 1) return 0;

   double eps = FP_EpsilonPrice(epsilon_points);
   int next_id = 0;

   for(int i=0; i<total; i++)
   {
      int hs, he;
      FP_FindHighPlateau(rates, total, i, eps, hs, he);
      if(i == hs)
      {
         bool pending_high = false;
         bool left_ok = FP_HighHasLeftL(rates, total, hs, rates[i].high, L, eps);
         bool right_ok = FP_HighHasRightL(rates, total, he, rates[i].high, L, eps, pending_high);
         if(left_ok && (right_ok || (include_pending && pending_high)))
         {
            FP_Node n;
            FP_BuildNodeFromPlateau(rates, L, FP_NODE_HIGH, hs, he, rates[i].high, right_ok, next_id, n);
            FP_AddNode(nodes, n);
            next_id++;
         }
      }

      int ls, le;
      FP_FindLowPlateau(rates, total, i, eps, ls, le);
      if(i == ls)
      {
         bool pending_low = false;
         bool left_ok = FP_LowHasLeftL(rates, total, ls, rates[i].low, L, eps);
         bool right_ok = FP_LowHasRightL(rates, total, le, rates[i].low, L, eps, pending_low);
         if(left_ok && (right_ok || (include_pending && pending_low)))
         {
            FP_Node n;
            FP_BuildNodeFromPlateau(rates, L, FP_NODE_LOW, ls, le, rates[i].low, right_ok, next_id, n);
            FP_AddNode(nodes, n);
            next_id++;
         }
      }
   }

   FP_SortNodes(nodes);
   return ArraySize(nodes);
}

bool FP_NodeIsMoreExtreme(const FP_Node &candidate, const FP_Node &current)
{
   if(candidate.kind == FP_NODE_HIGH) return (candidate.price > current.price);
   if(candidate.kind == FP_NODE_LOW)  return (candidate.price < current.price);
   return false;
}

int FP_CompressAlternatingExtreme(const FP_Node &nodes[], const int node_count, FP_Node &out_nodes[])
{
   ArrayResize(out_nodes, 0);
   if(node_count <= 0) return 0;

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
         if(FP_NodeIsMoreExtreme(nodes[i], current)) current = nodes[i];
      }
      else
      {
         FP_AddNode(out_nodes, current);
         current = nodes[i];
      }
   }

   if(has_current) FP_AddNode(out_nodes, current);
   for(int k=0; k<ArraySize(out_nodes); k++) out_nodes[k].id = k;
   return ArraySize(out_nodes);
}

int FP_BuildScaleList(const bool use_multi_scale,
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
   raw[0] = L1;
   raw[1] = (use_multi_scale ? L2 : 0);
   raw[2] = (use_multi_scale ? L3 : 0);
   raw[3] = (use_multi_scale ? L4 : 0);
   raw[4] = (use_multi_scale ? L5 : 0);
   raw[5] = (use_multi_scale ? L6 : 0);
   raw[6] = (use_multi_scale ? L7 : 0);
   raw[7] = (use_multi_scale ? L8 : 0);

   for(int i=0; i<8; i++)
   {
      if(raw[i] <= 0) continue;
      bool exists = false;
      for(int j=0; j<ArraySize(scales); j++)
      {
         if(scales[j] == raw[i]) { exists = true; break; }
      }
      if(!exists)
      {
         int sz = ArraySize(scales);
         ArrayResize(scales, sz + 1);
         scales[sz] = raw[i];
      }
   }

   // ascending order
   int n = ArraySize(scales);
   for(int a=0; a<n-1; a++)
   {
      int best = a;
      for(int b=a+1; b<n; b++) if(scales[b] < scales[best]) best = b;
      if(best != a)
      {
         int tmp = scales[a];
         scales[a] = scales[best];
         scales[best] = tmp;
      }
   }
   return n;
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

#endif // __FP_NODE_ENGINE_MQH__
