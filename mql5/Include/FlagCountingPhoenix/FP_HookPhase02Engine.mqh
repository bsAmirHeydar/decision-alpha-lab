#ifndef __FP_HOOK_PHASE02_ENGINE_MQH__
#define __FP_HOOK_PHASE02_ENGINE_MQH__
#property strict

#include "FP_HookPhase02DetectionCore.mqh"
#include "FP_HookPhase02Export.mqh"

void FP_RunHookPhase02Core(const string symbol,
                           const ENUM_TIMEFRAMES period,
                           const MqlRates &rates[],
                           const int copied,
                           const int &scales[],
                           const int scale_count,
                           const FP_HookPhase01Config &node_cfg,
                           const FP_HookPhase02Config &cfg,
                           const FP_FlagEvent &events[],
                           const int event_count,
                           const bool use_f3_validity_context,
                           FP_HookPhase02Report &report)
{
   FP_HookPhase02Sequence sequences[];
   FP_RunHookPhase02DetectionCore(symbol, period,
                                  rates, copied,
                                  scales, scale_count,
                                  node_cfg, cfg,
                                  events, event_count,
                                  use_f3_validity_context,
                                  sequences, report);

   if(!report.attempted)
      return;

   if(cfg.draw_sequences)
      FP_HookP02DrawSequences(cfg, sequences, report);

   if(cfg.export_csv)
   {
      FP_HookP02ExportSequences(cfg, sequences, report);
      FP_HookP02ExportSummary(symbol, period, cfg, report);
   }

   if(cfg.print_summary)
   {
      FP_PrintHookPhase02Config("FP_HOOK_P02", cfg);
      FP_PrintHookPhase02Report("FP_HOOK_P02", report);
   }

   if(cfg.print_samples)
      FP_PrintHookPhase02Samples("FP_HOOK_P02", sequences, cfg.sample_limit);
}

void FP_RunHookPhase02(const string symbol,
                       const ENUM_TIMEFRAMES period,
                       const MqlRates &rates[],
                       const int copied,
                       const int &scales[],
                       const int scale_count,
                       const FP_HookPhase01Config &node_cfg,
                       const FP_HookPhase02Config &cfg,
                       FP_HookPhase02Report &report)
{
   FP_FlagEvent empty_events[];
   ArrayResize(empty_events, 0);
   FP_RunHookPhase02Core(symbol, period, rates, copied, scales, scale_count,
                         node_cfg, cfg, empty_events, 0, false, report);
}

void FP_RunHookPhase02WithEvents(const string symbol,
                                 const ENUM_TIMEFRAMES period,
                                 const MqlRates &rates[],
                                 const int copied,
                                 const int &scales[],
                                 const int scale_count,
                                 const FP_HookPhase01Config &node_cfg,
                                 const FP_HookPhase02Config &cfg,
                                 const FP_FlagEvent &events[],
                                 const int event_count,
                                 FP_HookPhase02Report &report)
{
   FP_RunHookPhase02Core(symbol, period, rates, copied, scales, scale_count,
                         node_cfg, cfg, events, event_count, true, report);
}

#endif // __FP_HOOK_PHASE02_ENGINE_MQH__
