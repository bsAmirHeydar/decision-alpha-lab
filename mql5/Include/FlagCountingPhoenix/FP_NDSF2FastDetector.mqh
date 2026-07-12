#ifndef __FP_NDS_F2_FAST_DETECTOR_MQH__
#define __FP_NDS_F2_FAST_DETECTOR_MQH__
#property strict

#include "FP_SequenceEngine.mqh"

// Execution-only F1/F2 detector.
// Reuses canonical Phoenix node extraction, F1 lifecycle, F2 body/lifecycle and
// parent resolution. It intentionally does not build Hook branches, F3,
// ownership, canonical rendering, chart objects, audit exports or diagnostics.
void FP_DetectF2ExecutionScale(const MqlRates &rates[],
                               const int total,
                               const int scale_L,
                               const FP_Config &cfg,
                               FP_FlagEvent &events[])
{
   FP_Node raw_nodes[];
   FP_Node nodes[];
   FP_NodeExtractReport node_extract_report;
   FP_NodeCompressReport node_compress_report;

   int node_count = FP_BuildCanonicalNodesForScale(rates,
                                                   total,
                                                   scale_L,
                                                   false,
                                                   cfg.boundary_epsilon_points,
                                                   raw_nodes,
                                                   nodes,
                                                   node_extract_report,
                                                   node_compress_report);
   if(node_count < 4) return;

   FP_FlagBodyBuildReport body_report;
   FP_ResetFlagBodyBuildReport(body_report);
   FP_SeedFlagBodyBuildReport(body_report, scale_L, node_count, FP_DIR_NONE, FP_LEVEL_NONE);

   FP_InternalCountBuildReport internal_report;
   FP_ResetInternalCountBuildReport(internal_report);
   FP_SeedInternalCountBuildReport(internal_report, scale_L, node_count);

   FP_F1LifecycleBuildReport f1_report;
   FP_ResetF1LifecycleBuildReport(f1_report);
   FP_SeedF1LifecycleBuildReport(f1_report, scale_L, node_count);

   FP_F2LifecycleBuildReport f2_report;
   FP_ResetF2LifecycleBuildReport(f2_report);
   FP_SeedF2LifecycleBuildReport(f2_report, scale_L, node_count);

   FP_F3LifecycleBuildReport f3_report;
   FP_ResetF3LifecycleBuildReport(f3_report);
   FP_SeedF3LifecycleBuildReport(f3_report, scale_L, node_count);

   for(int d=0; d<2; d++)
   {
      int direction = (d == 0 ? FP_DIR_BULLISH : FP_DIR_BEARISH);
      FP_Node origins[];
      FP_CollectRawOriginNodesForDirection(nodes, node_count, direction, origins);

      int roots_used = 0;
      FP_TryBuildFlagChainsFromOrigins(nodes,
                                       node_count,
                                       origins,
                                       direction,
                                       false,
                                       true,
                                       cfg,
                                       events,
                                       roots_used,
                                       body_report,
                                       internal_report,
                                       f1_report,
                                       f2_report,
                                       f3_report);
   }
}

int FP_DetectF2ExecutionScales(const MqlRates &rates[],
                               const int total,
                               const int &scales[],
                               const int scale_count,
                               const FP_Config &cfg,
                               FP_FlagEvent &events[])
{
   ArrayResize(events, 0);
   for(int s=0; s<scale_count; s++)
   {
      if(scales[s] <= 0) continue;
      FP_DetectF2ExecutionScale(rates, total, scales[s], cfg, events);
      if(cfg.max_events > 0 && ArraySize(events) >= cfg.max_events) break;
   }
   return ArraySize(events);
}

#endif // __FP_NDS_F2_FAST_DETECTOR_MQH__
