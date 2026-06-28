#ifndef __FP_NODE_PLATEAU_MQH__
#define __FP_NODE_PLATEAU_MQH__
#property strict

#include "FP_NodeExtractTypes.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 02 / Plateau Detection
// ----------------------------------------------------------------------------
// Adjacent equal highs/lows become one candidate plateau. The anchor policy is
// intentionally stable: the last equal touch is the node anchor.
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

int FP_PlateauWidth(const int start, const int end)
{
   if(start < 0 || end < start) return 0;
   return end - start + 1;
}

void FP_NodeReportPlateau(FP_NodeExtractReport &r, const int kind, const int start, const int end)
{
   if(kind == FP_NODE_HIGH) r.candidate_high_plateaus++;
   else if(kind == FP_NODE_LOW) r.candidate_low_plateaus++;
   r.raw_candidates++;

   int w = FP_PlateauWidth(start, end);
   if(w > r.plateau_max_width) r.plateau_max_width = w;
}

#endif // __FP_NODE_PLATEAU_MQH__
