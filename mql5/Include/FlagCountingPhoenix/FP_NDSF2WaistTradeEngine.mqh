#ifndef __FP_NDS_F2_WAIST_TRADE_ENGINE_MQH__
#define __FP_NDS_F2_WAIST_TRADE_ENGINE_MQH__
#property strict

#include "FP_NDSF2WaistTradeRules.mqh"

FP_NDSF2WaistRunResult FP_RunNDSF2WaistTradeCore(const string symbol,
                                                  const ENUM_TIMEFRAMES period,
                                                  const MqlRates &rates[],
                                                  const int rates_total,
                                                  const FP_FlagEvent &events[],
                                                  const int event_count,
                                                  const double epsilon_points,
                                                  const FP_NDSF2WaistTradeConfig &cfg)
{
   if(!cfg.enabled) return FP_NDS_F2_RUN_IDLE;

   int f1_indices[];
   int f2_indices[];
   int available_indices[];
   int pair_count = FP_NDSF2CollectWaistBreakPairs(events, event_count,
                                                   rates, rates_total,
                                                   cfg, epsilon_points,
                                                   f1_indices, f2_indices,
                                                   available_indices);

   int sent_count = 0;
   int paper_count = 0;
   int blocked_count = 0;
   int error_count = 0;

   // Build all executable candidates before any order is sent. This prevents
   // iteration order from deciding which near-identical context survives.
   FP_NDSF2WaistTradeSetup candidates[];
   ArrayResize(candidates, 0);
   for(int i=0; i<pair_count; i++)
   {
      int f1_index = f1_indices[i];
      int f2_index = f2_indices[i];
      if(f1_index < 0 || f1_index >= event_count ||
         f2_index < 0 || f2_index >= event_count)
      {
         error_count++;
         continue;
      }

      FP_NDSF2WaistTradeSetup setup;
      if(!FP_NDSF2BuildWaistBreakSetup(symbol, period,
                                       rates, rates_total,
                                       events[f1_index], events[f2_index],
                                       available_indices[i],
                                       cfg, setup))
      {
         blocked_count++;
         continue;
      }
      if(FP_NDSF2SetupUsed(cfg, setup.setup_hash)) continue;

      int n = ArraySize(candidates);
      if(ArrayResize(candidates, n + 1) != n + 1)
      {
         error_count++;
         break;
      }
      candidates[n] = setup;
   }

   int candidate_count = ArraySize(candidates);
   bool suppressed[];
   ArrayResize(suppressed, candidate_count);
   for(int i=0; i<candidate_count; i++) suppressed[i] = false;

   // Same-direction candidates whose final executable stop corridors overlap
   // above the configured percentage represent one opportunity. Keep the wider
   // corridor. Equal-width ties keep the earlier deterministic candidate.
   double tick = FP_NDSHookTradeTickSize(symbol);
   double width_tolerance = MathMax(1e-12, tick * 0.25);
   for(int i=0; i<candidate_count; i++)
   {
      if(suppressed[i]) continue;
      for(int j=i+1; j<candidate_count; j++)
      {
         if(suppressed[j]) continue;
         if(!FP_NDSF2SameDirectionNearDuplicate(cfg, candidates[i], candidates[j]))
            continue;

         if(FP_NDSF2SetupIsWider(candidates[j], candidates[i], width_tolerance))
         {
            suppressed[i] = true;
            blocked_count++;
            break;
         }

         suppressed[j] = true;
         blocked_count++;
      }
   }

   for(int i=0; i<candidate_count; i++)
   {
      if(suppressed[i]) continue;
      FP_NDSF2WaistTradeSetup setup = candidates[i];

      if(!cfg.send_tester_orders)
      {
         ulong replace_tickets[];
         string overlap_reason;
         if(!FP_NDSF2InspectCandidateAgainstExistingOverlap(symbol, cfg, setup,
                                                             replace_tickets,
                                                             overlap_reason))
         {
            blocked_count++;
            continue;
         }

         string exposure_reason;
         if(!FP_NDSF2ExposurePolicyAllowsAfterReplacement(symbol, cfg, setup,
                                                            ArraySize(replace_tickets),
                                                            exposure_reason))
         {
            blocked_count++;
            continue;
         }

         if(FP_NDSF2MarkSetupUsed(cfg, setup.setup_hash)) paper_count++;
         else error_count++;
         continue;
      }

      ulong ticket = 0;
      if(FP_NDSF2SendLimit(symbol, cfg, setup, ticket)) sent_count++;
      else error_count++;
   }

   if(sent_count > 1) return FP_NDS_F2_RUN_MULTI_ORDER_SENT;
   if(sent_count == 1) return FP_NDS_F2_RUN_ORDER_SENT;
   if(paper_count > 0) return FP_NDS_F2_RUN_PAPER;
   if(error_count > 0) return FP_NDS_F2_RUN_ERROR;

   int orders = FP_NDSF2CountManagedOrdersOnSymbol(symbol, cfg, FP_DIR_NONE);
   int positions = FP_NDSF2CountManagedPositionsOnSymbol(symbol, cfg, FP_DIR_NONE);
   if(orders > 0) return FP_NDS_F2_RUN_PENDING_HELD;
   if(positions > 0) return FP_NDS_F2_RUN_POSITION_HELD;
   if(blocked_count > 0) return FP_NDS_F2_RUN_BLOCKED;
   return FP_NDS_F2_RUN_IDLE;
}

#endif // __FP_NDS_F2_WAIST_TRADE_ENGINE_MQH__
