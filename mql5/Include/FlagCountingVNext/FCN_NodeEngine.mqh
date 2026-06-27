#ifndef __FCN_NODE_ENGINE_MQH__
#define __FCN_NODE_ENGINE_MQH__
#property strict
#include "FCN_Types.mqh"

bool FCN_IsSwingHigh(const MqlRates &rates[], const int total, const int i, const int L)
{
   if(i < L || i >= total - L) return false;
   double h = rates[i].high;
   for(int k=1; k<=L; k++)
   {
      if(rates[i-k].high >= h) return false;
      if(rates[i+k].high >  h) return false;
   }
   return true;
}

bool FCN_IsSwingLow(const MqlRates &rates[], const int total, const int i, const int L)
{
   if(i < L || i >= total - L) return false;
   double l = rates[i].low;
   for(int k=1; k<=L; k++)
   {
      if(rates[i-k].low <= l) return false;
      if(rates[i+k].low <  l) return false;
   }
   return true;
}

void FCN_AppendNode(FCN_Node &nodes[], const FCN_Node &n)
{
   int sz = ArraySize(nodes);
   ArrayResize(nodes, sz + 1);
   nodes[sz] = n;
}

void FCN_DetectRawNodes(const MqlRates &rates[], const int total, const int L, FCN_Node &raw_nodes[])
{
   ArrayResize(raw_nodes, 0);
   if(total <= 2 * L + 4) return;

   for(int i=L; i<total-L; i++)
   {
      bool high = FCN_IsSwingHigh(rates, total, i, L);
      bool low  = FCN_IsSwingLow(rates, total, i, L);
      if(high)
         FCN_AppendNode(raw_nodes, FCN_MakeNode(i, rates[i].time, rates[i].high, FCN_NODE_HIGH));
      if(low)
         FCN_AppendNode(raw_nodes, FCN_MakeNode(i, rates[i].time, rates[i].low, FCN_NODE_LOW));
   }
}

bool FCN_IsMoreExtremeSameKind(const FCN_Node &candidate, const FCN_Node &current)
{
   if(candidate.kind != current.kind) return false;
   if(candidate.kind == FCN_NODE_HIGH) return candidate.price > current.price;
   if(candidate.kind == FCN_NODE_LOW)  return candidate.price < current.price;
   return false;
}

void FCN_CompressAlternatingNodes(const FCN_Node &raw_nodes[], FCN_Node &nodes[])
{
   ArrayResize(nodes, 0);
   int n = ArraySize(raw_nodes);
   if(n <= 0) return;

   for(int i=0; i<n; i++)
   {
      FCN_Node node = raw_nodes[i];
      int sz = ArraySize(nodes);
      if(sz == 0)
      {
         FCN_AppendNode(nodes, node);
         continue;
      }

      if(nodes[sz-1].kind == node.kind)
      {
         if(FCN_IsMoreExtremeSameKind(node, nodes[sz-1]))
            nodes[sz-1] = node;
      }
      else
      {
         FCN_AppendNode(nodes, node);
      }
   }
}

void FCN_BuildNodes(const MqlRates &rates[], const int total, const int L, FCN_Node &nodes[])
{
   FCN_Node raw[];
   FCN_DetectRawNodes(rates, total, L, raw);
   FCN_CompressAlternatingNodes(raw, nodes);
}

int FCN_FindNodePositionByIndex(const FCN_Node &nodes[], const int node_index)
{
   int n = ArraySize(nodes);
   for(int i=0; i<n; i++)
      if(nodes[i].index == node_index)
         return i;
   return -1;
}

#endif
