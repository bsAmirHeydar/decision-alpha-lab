#ifndef __FP_NODE_CLEARANCE_MQH__
#define __FP_NODE_CLEARANCE_MQH__
#property strict

#include "FP_NodePlateau.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 02 / L-Clearance Scans
// ----------------------------------------------------------------------------
// L means real non-reaching candles. Equal-price touches do not count as breaks
// and do not count as clearance. This preserves strict-pass semantics while
// preventing equal highs/lows from artificially confirming a node.
// ============================================================================

int FP_ScanHighLeftClearance(const MqlRates &rates[],
                             const int total,
                             const int start,
                             const double price,
                             const int L,
                             const double eps,
                             int &clearance_count,
                             int &equality_skips,
                             int &blocked_index)
{
   clearance_count = 0;
   equality_skips = 0;
   blocked_index = -1;

   for(int i=start - 1; i>=0 && clearance_count < L; i--)
   {
      if(FP_BreaksAbove(rates[i].high, price, eps))
      {
         blocked_index = i;
         return FP_NODE_CLEARANCE_BROKEN;
      }
      if(FP_AlmostEqual(rates[i].high, price, eps))
      {
         equality_skips++;
         continue;
      }
      clearance_count++;
   }
   if(clearance_count >= L) return FP_NODE_CLEARANCE_OK;
   return FP_NODE_CLEARANCE_NOT_ENOUGH;
}

int FP_ScanHighRightClearance(const MqlRates &rates[],
                              const int total,
                              const int end,
                              const double price,
                              const int L,
                              const double eps,
                              int &clearance_count,
                              int &equality_skips,
                              int &blocked_index)
{
   clearance_count = 0;
   equality_skips = 0;
   blocked_index = -1;

   for(int i=end + 1; i<total && clearance_count < L; i++)
   {
      if(FP_BreaksAbove(rates[i].high, price, eps))
      {
         blocked_index = i;
         return FP_NODE_CLEARANCE_BROKEN;
      }
      if(FP_AlmostEqual(rates[i].high, price, eps))
      {
         equality_skips++;
         continue;
      }
      clearance_count++;
   }
   if(clearance_count >= L) return FP_NODE_CLEARANCE_OK;
   return FP_NODE_CLEARANCE_PENDING;
}

int FP_ScanLowLeftClearance(const MqlRates &rates[],
                            const int total,
                            const int start,
                            const double price,
                            const int L,
                            const double eps,
                            int &clearance_count,
                            int &equality_skips,
                            int &blocked_index)
{
   clearance_count = 0;
   equality_skips = 0;
   blocked_index = -1;

   for(int i=start - 1; i>=0 && clearance_count < L; i--)
   {
      if(FP_BreaksBelow(rates[i].low, price, eps))
      {
         blocked_index = i;
         return FP_NODE_CLEARANCE_BROKEN;
      }
      if(FP_AlmostEqual(rates[i].low, price, eps))
      {
         equality_skips++;
         continue;
      }
      clearance_count++;
   }
   if(clearance_count >= L) return FP_NODE_CLEARANCE_OK;
   return FP_NODE_CLEARANCE_NOT_ENOUGH;
}

int FP_ScanLowRightClearance(const MqlRates &rates[],
                             const int total,
                             const int end,
                             const double price,
                             const int L,
                             const double eps,
                             int &clearance_count,
                             int &equality_skips,
                             int &blocked_index)
{
   clearance_count = 0;
   equality_skips = 0;
   blocked_index = -1;

   for(int i=end + 1; i<total && clearance_count < L; i++)
   {
      if(FP_BreaksBelow(rates[i].low, price, eps))
      {
         blocked_index = i;
         return FP_NODE_CLEARANCE_BROKEN;
      }
      if(FP_AlmostEqual(rates[i].low, price, eps))
      {
         equality_skips++;
         continue;
      }
      clearance_count++;
   }
   if(clearance_count >= L) return FP_NODE_CLEARANCE_OK;
   return FP_NODE_CLEARANCE_PENDING;
}

bool FP_HighHasLeftL(const MqlRates &rates[], const int total, const int start, const double price, const int L, const double eps)
{
   int c = 0;
   int eq = 0;
   int blocked = -1;
   return (FP_ScanHighLeftClearance(rates, total, start, price, L, eps, c, eq, blocked) == FP_NODE_CLEARANCE_OK);
}

bool FP_HighHasRightL(const MqlRates &rates[], const int total, const int end, const double price, const int L, const double eps, bool &pending)
{
   int c = 0;
   int eq = 0;
   int blocked = -1;
   int s = FP_ScanHighRightClearance(rates, total, end, price, L, eps, c, eq, blocked);
   pending = (s == FP_NODE_CLEARANCE_PENDING);
   return (s == FP_NODE_CLEARANCE_OK);
}

bool FP_LowHasLeftL(const MqlRates &rates[], const int total, const int start, const double price, const int L, const double eps)
{
   int c = 0;
   int eq = 0;
   int blocked = -1;
   return (FP_ScanLowLeftClearance(rates, total, start, price, L, eps, c, eq, blocked) == FP_NODE_CLEARANCE_OK);
}

bool FP_LowHasRightL(const MqlRates &rates[], const int total, const int end, const double price, const int L, const double eps, bool &pending)
{
   int c = 0;
   int eq = 0;
   int blocked = -1;
   int s = FP_ScanLowRightClearance(rates, total, end, price, L, eps, c, eq, blocked);
   pending = (s == FP_NODE_CLEARANCE_PENDING);
   return (s == FP_NODE_CLEARANCE_OK);
}

#endif // __FP_NODE_CLEARANCE_MQH__
