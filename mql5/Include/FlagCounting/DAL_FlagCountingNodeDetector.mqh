#ifndef __DAL_FLAG_COUNTING_NODE_DETECTOR_MQH__
#define __DAL_FLAG_COUNTING_NODE_DETECTOR_MQH__
#property strict
#include "DAL_FlagCountingTypes.mqh"

bool FC_IsSwingHigh(const MqlRates &rates[], const int total, const int i, const int L)
{
   if(i < L || i >= total - L) return false;
   double v = rates[i].high;
   for(int k=1; k<=L; k++)
   {
      if(rates[i-k].high >= v) return false;
      if(rates[i+k].high >  v) return false;
   }
   return true;
}

bool FC_IsSwingLow(const MqlRates &rates[], const int total, const int i, const int L)
{
   if(i < L || i >= total - L) return false;
   double v = rates[i].low;
   for(int k=1; k<=L; k++)
   {
      if(rates[i-k].low <= v) return false;
      if(rates[i+k].low <  v) return false;
   }
   return true;
}

void FC_AppendNode(FC_Node &nodes[], FC_Node &node)
{
   int n = ArraySize(nodes);
   ArrayResize(nodes, n + 1);
   nodes[n] = node;
}

int FC_DetectRawNodes(const MqlRates &rates[], const int total, const int L, FC_Node &raw_nodes[])
{
   ArrayResize(raw_nodes, 0);
   if(total <= 2*L + 5) return 0;

   for(int i=L; i<total-L; i++)
   {
      bool hi = FC_IsSwingHigh(rates, total, i, L);
      bool lo = FC_IsSwingLow(rates, total, i, L);

      if(hi)
      {
         FC_Node n = FC_MakeNode(i, rates[i].time, rates[i].high, FC_NODE_HIGH);
         FC_AppendNode(raw_nodes, n);
      }
      if(lo)
      {
         FC_Node n = FC_MakeNode(i, rates[i].time, rates[i].low, FC_NODE_LOW);
         FC_AppendNode(raw_nodes, n);
      }
   }
   return ArraySize(raw_nodes);
}

bool FC_NodeIsMoreExtreme(const FC_Node &candidate, const FC_Node &current)
{
   if(candidate.kind == FC_NODE_HIGH)
      return candidate.price > current.price;
   if(candidate.kind == FC_NODE_LOW)
      return candidate.price < current.price;
   return false;
}

int FC_CompressAlternatingNodes(const FC_Node &raw_nodes[], FC_Node &nodes[])
{
   ArrayResize(nodes, 0);
   int n_raw = ArraySize(raw_nodes);
   if(n_raw <= 0) return 0;

   for(int i=0; i<n_raw; i++)
   {
      FC_Node candidate = raw_nodes[i];
      int n = ArraySize(nodes);
      if(n <= 0)
      {
         FC_AppendNode(nodes, candidate);
         continue;
      }

      if(nodes[n-1].kind == candidate.kind)
      {
         if(FC_NodeIsMoreExtreme(candidate, nodes[n-1]))
            nodes[n-1] = candidate;
      }
      else
      {
         FC_AppendNode(nodes, candidate);
      }
   }
   return ArraySize(nodes);
}

int FC_BuildNodes(const MqlRates &rates[], const int total, const int L, FC_Node &nodes[])
{
   FC_Node raw[];
   FC_DetectRawNodes(rates, total, L, raw);
   return FC_CompressAlternatingNodes(raw, nodes);
}

int FC_FindNodePositionByIndex(const FC_Node &nodes[], const int bar_index)
{
   int n = ArraySize(nodes);
   for(int i=0; i<n; i++)
   {
      if(nodes[i].index == bar_index)
         return i;
   }
   return -1;
}

#endif
