#ifndef __FP_STATE_GATE_ENGINE_MQH__
#define __FP_STATE_GATE_ENGINE_MQH__
#property strict

#include "FP_StateGateExport.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 19 State Gate Engine
// ----------------------------------------------------------------------------
// Phase 1 builds a read-only shell snapshot from configured timeframes and
// renders/export/audits explicit placeholder rows.  It does not read, mutate, or
// reinterpret F-counting, Hook/ND, node, ownership, canonicalization, renderer,
// validation, release, or license engines.
// ============================================================================

void FP_StateGateEnsureRuntime(const FP_StateGateConfig &cfg,
                               FP_StateGateRuntime &runtime)
{
   if(runtime.initialized) return;
   FP_ResetStateGateRuntime(runtime);
   runtime.initialized = true;
   runtime.minimized = cfg.panel_start_minimized;
}

void FP_StateGateBuildPhase1Snapshot(const string symbol,
                                     const ENUM_TIMEFRAMES chart_period,
                                     const FP_StateGateConfig &cfg,
                                     FP_StateGateRuntime &runtime,
                                     FP_StateGateReport &report)
{
   FP_StateGateEnsureRuntime(cfg, runtime);
   FP_ResetStateGateSnapshot(runtime.snapshot);
   runtime.snapshot.initialized = true;
   runtime.snapshot.symbol = symbol;
   runtime.snapshot.chart_timeframe = chart_period;
   runtime.snapshot.generated_at = TimeCurrent();
   runtime.snapshot.timeframe_count = FP_STATE_GATE_TF_SLOTS;
   runtime.snapshot.status = "phase1_shell";
   runtime.snapshot.reason = "input_shell_and_module_skeleton";

   for(int i=0; i<FP_STATE_GATE_TF_SLOTS; i++)
   {
      FP_ResetStateGateTimeframeState(runtime.snapshot.tf_states[i]);
      ENUM_TIMEFRAMES tf = FP_StateGateConfigTimeframeAt(cfg, i);
      runtime.snapshot.tf_states[i].timeframe = tf;
      runtime.snapshot.tf_states[i].timeframe_label = FP_StateGateTimeframeName(tf);
      runtime.snapshot.tf_states[i].status = "phase1_shell";
      runtime.snapshot.tf_states[i].reason = "projection_pending";
      if(FP_StateGateTimeframeIsUsable(tf))
      {
         runtime.snapshot.tf_states[i].last_closed_bar_time = iTime(symbol, tf, 1);
         runtime.snapshot.tf_states[i].last_closed_bar_close = iClose(symbol, tf, 1);
         runtime.snapshot.tf_states[i].closed_bar_available = (runtime.snapshot.tf_states[i].last_closed_bar_time > 0);
         runtime.snapshot.tf_states[i].dirty = (runtime.last_processed_closed_bar_time[i] != runtime.snapshot.tf_states[i].last_closed_bar_time);
         runtime.last_processed_closed_bar_time[i] = runtime.snapshot.tf_states[i].last_closed_bar_time;
         if(runtime.snapshot.tf_states[i].dirty) report.dirty_timeframes++;
      }
      else
      {
         runtime.snapshot.tf_states[i].closed_bar_available = false;
         runtime.snapshot.tf_states[i].reason = "period_current_disabled_in_phase1";
      }

      FP_StateGateSeedPlaceholderRowsForSlot(i, runtime.snapshot.tf_states[i], runtime.snapshot);
   }

   report.attempted = true;
   report.ok = true;
   report.status = "phase1_shell";
   report.reason = "placeholder_rows_only";
   report.version = FP_STATE_GATE_VERSION;
   report.symbol = symbol;
   report.timeframe_count = runtime.snapshot.timeframe_count;
   report.rally_rows = runtime.snapshot.rally_row_count;
   report.hook_rows = runtime.snapshot.hook_row_count;
}

void FP_RunStateGatePhase1(const string symbol,
                           const ENUM_TIMEFRAMES chart_period,
                           const FP_StateGateConfig &cfg,
                           FP_StateGateRuntime &runtime,
                           FP_StateGateReport &report)
{
   FP_ResetStateGateReport(report);
   if(!cfg.enabled)
   {
      report.status = "disabled";
      report.reason = "InpStateGateEnabled_false";
      report.ok = true;
      return;
   }

   FP_StateGateBuildPhase1Snapshot(symbol, chart_period, cfg, runtime, report);
   if(cfg.panel_enabled)
      FP_StateGatePanelDraw(cfg, runtime.snapshot, runtime.minimized, report);
   FP_StateGateExportPhase1Stub(cfg, runtime.snapshot, report);
}

#endif // __FP_STATE_GATE_ENGINE_MQH__
