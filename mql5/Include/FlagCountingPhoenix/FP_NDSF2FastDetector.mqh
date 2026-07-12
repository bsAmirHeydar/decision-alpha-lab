#ifndef __FP_NDS_F2_FAST_DETECTOR_MQH__
#define __FP_NDS_F2_FAST_DETECTOR_MQH__
#property strict

#include "FP_SequenceEngine.mqh"

// Execution-only detector. It reuses the canonical Phoenix node/F1/F2 builders,
// but deliberately skips global sorting, ownership, visual duplicate merging,
// Hook seeding and Level-11 canonical rendering passes.
int FP_DetectF2ExecutionScales(const MqlRates &rates[],
                               const int total,
                               const int &scales[],
                               const int scale_count,
                               const FP_Config &cfg,
                               FP_FlagEvent &events[])
{
   ArrayResize(events, 0);
   FP_HookBranch hooks[];
   FP_DetectResult result;
   FP_ResetDetectResult(result);

   for(int s=0; s<scale_count; s++)
   {
      if(scales[s] <= 0) continue;
      FP_DetectScale(rates, total, scales[s], cfg, events, hooks, result);
   }
   return ArraySize(events);
}

#endif // __FP_NDS_F2_FAST_DETECTOR_MQH__
