#property strict
#include "H0007_F1_Types.mqh"

void H0007_AddNode(H0007_F1Node &nodes[], const H0007_F1Node &node)
{
   int n = ArraySize(nodes);
   ArrayResize(nodes, n + 1);
   nodes[n] = node;
}

void H0007_DetectLNodes(const MqlRates &rates[], const int total, const int L, H0007_F1Node &nodes[])
{
   ArrayResize(nodes, 0);
   if(total < (2 * L + 1)) return;

   for(int i=L; i<total-L; i++)
   {
      bool high_ok = true;
      bool low_ok  = true;

      for(int j=i-L; j<=i+L; j++)
      {
         if(j == i) continue;
         if(rates[i].high < rates[j].high) high_ok = false;
         if(rates[i].low  > rates[j].low)  low_ok  = false;
         if(!high_ok && !low_ok) break;
      }

      if(high_ok)
      {
         H0007_F1Node node;
         node.index = i;
         node.time  = rates[i].time;
         node.price = rates[i].high;
         node.type  = H0007_NODE_HIGH;
         node.L     = L;
         H0007_AddNode(nodes, node);
      }

      if(low_ok)
      {
         H0007_F1Node node;
         node.index = i;
         node.time  = rates[i].time;
         node.price = rates[i].low;
         node.type  = H0007_NODE_LOW;
         node.L     = L;
         H0007_AddNode(nodes, node);
      }
   }
}

void H0007_CompressAlternatingNodes(const H0007_F1Node &raw[], H0007_F1Node &out[])
{
   ArrayResize(out, 0);
   int n = ArraySize(raw);
   if(n <= 0) return;

   for(int i=0; i<n; i++)
   {
      H0007_F1Node node = raw[i];
      int m = ArraySize(out);
      if(m == 0)
      {
         H0007_AddNode(out, node);
         continue;
      }

      H0007_F1Node last = out[m-1];
      if(node.type != last.type)
      {
         H0007_AddNode(out, node);
         continue;
      }

      if(node.type == H0007_NODE_HIGH && node.price >= last.price)
         out[m-1] = node;

      if(node.type == H0007_NODE_LOW && node.price <= last.price)
         out[m-1] = node;
   }
}
