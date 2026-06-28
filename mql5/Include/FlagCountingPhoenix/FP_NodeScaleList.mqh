#ifndef __FP_NODE_SCALE_LIST_MQH__
#define __FP_NODE_SCALE_LIST_MQH__
#property strict

#include "FP_NodeCanonicalizer.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 02 / Scale List Builder
// ----------------------------------------------------------------------------
// Keeps multi-L view construction outside the EA and outside the renderer.
// ============================================================================

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

#endif // __FP_NODE_SCALE_LIST_MQH__
