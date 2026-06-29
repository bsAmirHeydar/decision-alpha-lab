#ifndef __FP_STATE_GATE_ENGINE_MQH__
#define __FP_STATE_GATE_ENGINE_MQH__
#property strict

#include "FP_StateGatePanel.mqh"
#include "FP_StateGateExport.mqh"
#include "FP_StateGateAudit.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 19 State Gate Engine
// ----------------------------------------------------------------------------
// Phase 2 implements closed-bar tracking for each configured timeframe. It does
// not read, mutate, or reinterpret F-counting, Hook/ND, node, ownership,
// canonicalization, renderer, validation, release, or license engines.
// ============================================================================

void FP_StateGateEnsureRuntime(const FP_StateGateConfig &cfg,
                               FP_StateGateRuntime &runtime)
{
   if(runtime.initialized) return;
   FP_ResetStateGateRuntime(runtime);
   runtime.initialized = true;
   runtime.minimized = cfg.panel_start_minimized;
}

void FP_StateGateReadClosedBarState(const string symbol,
                                    const int slot,
                                    const ENUM_TIMEFRAMES tf,
                                    FP_StateGateRuntime &runtime,
                                    FP_StateGateTimeframeState &state)
{
   state.timeframe = tf;
   state.timeframe_label = FP_StateGateTimeframeName(tf);
   state.initialized = runtime.slot_initialized[slot];
   state.previous_closed_bar_time = runtime.previous_closed_bar_time[slot];
   state.update_count = runtime.slot_update_count[slot];

   if(!FP_StateGateTimeframeIsUsable(tf))
   {
      state.closed_bar_available = false;
      state.dirty = false;
      state.bars_available = 0;
      state.tracker_status = FP_STATE_GATE_STATUS_TF_UNUSABLE;
      state.status = FP_STATE_GATE_STATUS_TF_UNUSABLE;
      state.reason = "PERIOD_CURRENT_is_not_used_by_level19";
      return;
   }

   state.bars_available = Bars(symbol, tf);
   datetime closed_time = iTime(symbol, tf, 1);
   double closed_close = iClose(symbol, tf, 1);
   state.last_closed_bar_time = closed_time;
   state.last_closed_bar_close = closed_close;
   state.closed_bar_available = (closed_time > 0);

   if(!state.closed_bar_available)
   {
      state.dirty = false;
      state.tracker_status = FP_STATE_GATE_STATUS_TF_UNAVAILABLE;
      state.status = FP_STATE_GATE_STATUS_TF_UNAVAILABLE;
      state.reason = "closed_bar_shift_1_not_available";
      return;
   }

   if(!runtime.slot_initialized[slot])
   {
      runtime.slot_initialized[slot] = true;
      runtime.previous_closed_bar_time[slot] = 0;
      runtime.last_processed_closed_bar_time[slot] = closed_time;
      runtime.slot_update_count[slot] = 1;
      state.initialized = true;
      state.previous_closed_bar_time = 0;
      state.update_count = runtime.slot_update_count[slot];
      state.dirty = true;
      state.tracker_status = FP_STATE_GATE_STATUS_FIRST;
      state.status = FP_STATE_GATE_STATUS_TRACKING;
      state.reason = "first_closed_bar_snapshot";
      return;
   }

   if(runtime.last_processed_closed_bar_time[slot] != closed_time)
   {
      runtime.previous_closed_bar_time[slot] = runtime.last_processed_closed_bar_time[slot];
      runtime.last_processed_closed_bar_time[slot] = closed_time;
      runtime.slot_update_count[slot]++;
      state.previous_closed_bar_time = runtime.previous_closed_bar_time[slot];
      state.update_count = runtime.slot_update_count[slot];
      state.dirty = true;
      state.tracker_status = FP_STATE_GATE_STATUS_DIRTY;
      state.status = FP_STATE_GATE_STATUS_TRACKING;
      state.reason = "new_closed_bar_detected";
      return;
   }

   state.previous_closed_bar_time = runtime.previous_closed_bar_time[slot];
   state.update_count = runtime.slot_update_count[slot];
   state.dirty = false;
   state.tracker_status = FP_STATE_GATE_STATUS_UNCHANGED;
   state.status = FP_STATE_GATE_STATUS_TRACKING;
   state.reason = "closed_bar_already_processed";
}

void FP_StateGateBuildPhase2Snapshot(const string symbol,
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
   runtime.snapshot.status = "phase2_closed_bar_tracker";
   runtime.snapshot.reason = FP_STATE_GATE_REASON_PHASE2;
   runtime.snapshot.update_serial = runtime.update_serial;

   for(int i=0; i<FP_STATE_GATE_TF_SLOTS; i++)
   {
      ENUM_TIMEFRAMES tf = FP_StateGateConfigTimeframeAt(cfg, i);
      FP_StateGateReadClosedBarState(symbol, i, tf, runtime, runtime.snapshot.tf_states[i]);
      report.slots_checked++;
      if(runtime.snapshot.tf_states[i].closed_bar_available)
      {
         runtime.snapshot.available_timeframes++;
         report.available_timeframes++;
      }
      else
      {
         runtime.snapshot.unavailable_timeframes++;
         report.unavailable_timeframes++;
      }

      if(runtime.snapshot.tf_states[i].dirty)
      {
         runtime.snapshot.dirty_timeframes++;
         runtime.snapshot.any_dirty = true;
         report.dirty_timeframes++;
      }
      else if(runtime.snapshot.tf_states[i].closed_bar_available)
      {
         runtime.snapshot.unchanged_timeframes++;
         report.unchanged_timeframes++;
      }

      FP_StateGateSeedPlaceholderRowsForSlot(i, runtime.snapshot.tf_states[i], runtime.snapshot);
   }

   if(runtime.snapshot.any_dirty)
      runtime.update_serial++;
   runtime.snapshot.update_serial = runtime.update_serial;
   runtime.last_run_had_dirty = runtime.snapshot.any_dirty;
   runtime.last_engine_run_time = TimeCurrent();

   report.attempted = true;
   report.ok = true;
   report.status = runtime.snapshot.status;
   report.reason = runtime.snapshot.reason;
   report.version = FP_STATE_GATE_VERSION;
   report.symbol = symbol;
   report.timeframe_count = runtime.snapshot.timeframe_count;
   report.rally_rows = runtime.snapshot.rally_row_count;
   report.hook_rows = runtime.snapshot.hook_row_count;
}

void FP_RunStateGatePhase2(const string symbol,
                           const ENUM_TIMEFRAMES chart_period,
                           const FP_StateGateConfig &cfg,
                           FP_StateGateRuntime &runtime,
                           FP_StateGateReport &report)
{
   FP_ResetStateGateReport(report);
   if(!cfg.enabled)
   {
      report.attempted = true;
      report.status = FP_STATE_GATE_STATUS_DISABLED;
      report.reason = "InpStateGateEnabled_false";
      report.ok = true;
      return;
   }

   FP_StateGateBuildPhase2Snapshot(symbol, chart_period, cfg, runtime, report);

   bool should_redraw_panel = (cfg.panel_enabled && (runtime.snapshot.any_dirty || !runtime.panel_has_drawn));
   if(should_redraw_panel)
   {
      FP_StateGatePanelDraw(cfg, runtime.snapshot, runtime.minimized, report);
      runtime.panel_has_drawn = true;
      report.panel_redrawn = true;
   }

   bool should_export = (cfg.export_csv && (runtime.snapshot.any_dirty || !runtime.export_has_written));
   if(should_export)
   {
      FP_StateGateExportLatestCsv(cfg, runtime.snapshot, report);
      if(report.file_errors == 0) runtime.export_has_written = true;
   }

   if(!runtime.snapshot.any_dirty && runtime.panel_has_drawn)
   {
      report.skipped_no_dirty = true;
      if(report.reason == FP_STATE_GATE_REASON_PHASE2)
         report.reason = "phase2_no_closed_bar_change";
   }

   report.ok = (report.object_errors == 0 && report.file_errors == 0);
   if(!report.ok && report.reason == FP_STATE_GATE_REASON_PHASE2)
      report.reason = "phase2_errors";
}

// Backward-compatible alias for the Phase 1 integration name.  The underlying
// behavior is now Phase 2 closed-bar tracking.
void FP_RunStateGatePhase1(const string symbol,
                           const ENUM_TIMEFRAMES chart_period,
                           const FP_StateGateConfig &cfg,
                           FP_StateGateRuntime &runtime,
                           FP_StateGateReport &report)
{
   FP_RunStateGatePhase2(symbol, chart_period, cfg, runtime, report);
}

#endif // __FP_STATE_GATE_ENGINE_MQH__
