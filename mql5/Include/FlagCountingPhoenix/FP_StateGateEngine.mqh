#ifndef __FP_STATE_GATE_ENGINE_MQH__
#define __FP_STATE_GATE_ENGINE_MQH__
#property strict

#include "FP_Timebase.mqh"
#include "FP_SequenceEngine.mqh"
#include "FP_StateGatePanel.mqh"
#include "FP_StateGateExport.mqh"
#include "FP_StateGateAudit.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 19 State Gate Engine
// ----------------------------------------------------------------------------
// Phase 6 keeps closed-bar tracking, Rally View projection, Hook View
// projection, dashboard usability, and adds State Contract storage fields. The projection runs the same
// locked Phoenix anatomy pipeline per configured timeframe and maps existing
// facts into State Gate rows. It does not alter Node, Hook/ND, Flag Body,
// Internal Count, lifecycle, ownership, canonicalization, renderer, validation,
// release, or license logic.
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

void FP_StateGateQuietEngineConfig(const string symbol,
                                   const ENUM_TIMEFRAMES tf,
                                   const FP_Config &source,
                                   FP_Config &target)
{
   target = source;
   target.context_symbol = symbol;
   target.context_timeframe = FP_StateGateTimeframeName(tf);
   target.identity_generation_pass = "phoenix_level19_state_gate";
   target.print_node_sanity = false;
   target.print_node_samples = false;
   target.print_identity_sanity = false;
   target.print_identity_samples = false;
   target.print_hook_sanity = false;
   target.print_hook_samples = false;
   target.print_body_sanity = false;
   target.print_body_samples = false;
   target.print_internal_sanity = false;
   target.print_internal_samples = false;
   target.print_f1_sanity = false;
   target.print_f1_samples = false;
   target.print_f2_sanity = false;
   target.print_f2_samples = false;
   target.print_f3_sanity = false;
   target.print_f3_samples = false;
   target.print_ownership_sanity = false;
   target.print_ownership_samples = false;
   target.print_canonical_sanity = false;
   target.print_canonical_samples = false;
   target.verbose_logs = false;
}

bool FP_StateGateRunReadOnlyAnatomy(const string symbol,
                                    const ENUM_TIMEFRAMES tf,
                                    const FP_TimebaseConfig &timebase_template,
                                    const FP_Config &engine_template,
                                    const int &scales[],
                                    const int scale_count,
                                    MqlRates &rates[],
                                    FP_FlagEvent &events[],
                                    FP_HookBranch &hooks[],
                                    FP_DetectResult &detect_result,
                                    string &reason)
{
   ArrayResize(rates, 0);
   ArrayResize(events, 0);
   ArrayResize(hooks, 0);
   FP_ResetDetectResult(detect_result);
   reason = "ok";

   if(scale_count <= 0)
   {
      reason = "no_scales";
      return false;
   }

   FP_TimebaseConfig tf_timebase = timebase_template;
   tf_timebase.symbol = symbol;
   tf_timebase.period = tf;
   tf_timebase.print_sanity = false;
   tf_timebase.print_samples = false;

   FP_TimebaseReport timebase_report;
   int copied = FP_LoadCanonicalRates(tf_timebase, rates, timebase_report);
   if(!timebase_report.ok || copied < tf_timebase.min_closed_bars)
   {
      reason = "timebase_failed:" + timebase_report.reason;
      return false;
   }

   FP_Config tf_engine_cfg;
   FP_StateGateQuietEngineConfig(symbol, tf, engine_template, tf_engine_cfg);
   FP_DetectAllScales(rates, copied, scales, scale_count, tf_engine_cfg, events, hooks, detect_result);
   reason = "events=" + IntegerToString(ArraySize(events)) + ";hooks=" + IntegerToString(ArraySize(hooks));
   return true;
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

   FP_StateGateBuildExtremeCandidateRows(runtime.snapshot, cfg.max_extreme_candidates_per_tf);
   FP_StateGateFinalizeSnapshotContracts(runtime.snapshot);
   FP_StateGateBuildMtfAlignmentRows(runtime.snapshot);
   FP_StateGateFinalizeSnapshotMtfAlignment(runtime.snapshot);
   FP_StateGateFinalizeSnapshotEntryGeometry(runtime.snapshot);
   FP_StateGateBuildEntryIdeaRows(runtime.snapshot);
   FP_StateGateFinalizeSnapshotEntryIdeas(runtime.snapshot);
   FP_StateGateBuildEntryDecisionRows(runtime.snapshot);
   FP_StateGateFinalizeSnapshotEntryDecisions(runtime.snapshot);
   FP_StateGateBuildPaperLedgerRows(runtime.snapshot);
   FP_StateGateFinalizeSnapshotPaperLedger(runtime.snapshot);
   FP_StateGateBuildPaperLifecycleRows(runtime.snapshot);
   FP_StateGateFinalizeSnapshotPaperLifecycle(runtime.snapshot);
   FP_StateGateBuildPaperResultRows(runtime.snapshot);
   FP_StateGateFinalizeSnapshotPaperResults(runtime.snapshot);
   FP_StateGateBuildPaperPortfolioRows(runtime.snapshot);
   FP_StateGateFinalizeSnapshotPaperPortfolio(runtime.snapshot);
   FP_StateGateBuildPaperRegimeRows(runtime.snapshot);
   FP_StateGateFinalizeSnapshotPaperRegime(runtime.snapshot);
   FP_StateGateBuildPaperFilterRows(runtime.snapshot);
   FP_StateGateFinalizeSnapshotPaperFilters(runtime.snapshot);

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
   report.extreme_candidate_rows = runtime.snapshot.extreme_candidate_row_count;
   report.mtf_alignment_rows = runtime.snapshot.mtf_alignment_row_count;
   report.geometry_rows = runtime.snapshot.timeframe_count;
   report.entry_idea_rows = runtime.snapshot.entry_idea_row_count;
   report.entry_decision_rows = runtime.snapshot.entry_decision_row_count;
   report.paper_ledger_rows = runtime.snapshot.paper_ledger_row_count;
   report.paper_lifecycle_rows = runtime.snapshot.paper_lifecycle_row_count;
   report.paper_result_rows = runtime.snapshot.paper_result_row_count;
   report.paper_portfolio_rows = runtime.snapshot.paper_portfolio_row_count;
   report.paper_regime_rows = runtime.snapshot.paper_regime_row_count;
   report.paper_filter_rows = runtime.snapshot.paper_filter_row_count;
   report.contract_rows = runtime.snapshot.timeframe_count;
}

void FP_StateGateBuildPhase4Snapshot(const string symbol,
                                     const ENUM_TIMEFRAMES chart_period,
                                     const FP_StateGateConfig &cfg,
                                     const FP_TimebaseConfig &timebase_template,
                                     const FP_Config &engine_template,
                                     const int &scales[],
                                     const int scale_count,
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
   runtime.snapshot.status = "phase4_rally_hook_projection";
   runtime.snapshot.reason = FP_STATE_GATE_REASON_PHASE4;
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

      if(!runtime.snapshot.tf_states[i].closed_bar_available)
      {
         FP_StateGateAddNoRallyRowsForSlot(i, runtime.snapshot.tf_states[i], runtime.snapshot, FP_STATE_GATE_STATUS_TF_UNAVAILABLE);
         FP_StateGateAddNoHookRowsForSlot(i, runtime.snapshot.tf_states[i], runtime.snapshot, FP_STATE_GATE_STATUS_TF_UNAVAILABLE);
         continue;
      }

      MqlRates tf_rates[];
      FP_FlagEvent tf_events[];
      FP_HookBranch tf_hooks[];
      FP_DetectResult tf_result;
      string anatomy_reason = "";
      bool anatomy_ok = FP_StateGateRunReadOnlyAnatomy(symbol, tf, timebase_template, engine_template, scales, scale_count, tf_rates, tf_events, tf_hooks, tf_result, anatomy_reason);
      if(!anatomy_ok)
      {
         FP_StateGateAddNoRallyRowsForSlot(i, runtime.snapshot.tf_states[i], runtime.snapshot, anatomy_reason);
         FP_StateGateAddNoHookRowsForSlot(i, runtime.snapshot.tf_states[i], runtime.snapshot, anatomy_reason);
      }
      else
      {
         FP_StateGateBuildRallyRowsForSlot(i, runtime.snapshot.tf_states[i], tf_events, cfg.max_rally_rows_per_tf, runtime.snapshot);
         FP_StateGateBuildHookRowsForSlot(i, runtime.snapshot.tf_states[i], tf_hooks, cfg.max_hook_rows_per_tf, runtime.snapshot);
      }
   }

   FP_StateGateBuildExtremeCandidateRows(runtime.snapshot, cfg.max_extreme_candidates_per_tf);
   FP_StateGateFinalizeSnapshotContracts(runtime.snapshot);
   FP_StateGateBuildMtfAlignmentRows(runtime.snapshot);
   FP_StateGateFinalizeSnapshotMtfAlignment(runtime.snapshot);
   FP_StateGateFinalizeSnapshotEntryGeometry(runtime.snapshot);
   FP_StateGateBuildEntryIdeaRows(runtime.snapshot);
   FP_StateGateFinalizeSnapshotEntryIdeas(runtime.snapshot);
   FP_StateGateBuildEntryDecisionRows(runtime.snapshot);
   FP_StateGateFinalizeSnapshotEntryDecisions(runtime.snapshot);
   FP_StateGateBuildPaperLedgerRows(runtime.snapshot);
   FP_StateGateFinalizeSnapshotPaperLedger(runtime.snapshot);
   FP_StateGateBuildPaperLifecycleRows(runtime.snapshot);
   FP_StateGateFinalizeSnapshotPaperLifecycle(runtime.snapshot);
   FP_StateGateBuildPaperResultRows(runtime.snapshot);
   FP_StateGateFinalizeSnapshotPaperResults(runtime.snapshot);
   FP_StateGateBuildPaperPortfolioRows(runtime.snapshot);
   FP_StateGateFinalizeSnapshotPaperPortfolio(runtime.snapshot);
   FP_StateGateBuildPaperRegimeRows(runtime.snapshot);
   FP_StateGateFinalizeSnapshotPaperRegime(runtime.snapshot);
   FP_StateGateBuildPaperFilterRows(runtime.snapshot);
   FP_StateGateFinalizeSnapshotPaperFilters(runtime.snapshot);

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
   report.extreme_candidate_rows = runtime.snapshot.extreme_candidate_row_count;
   report.mtf_alignment_rows = runtime.snapshot.mtf_alignment_row_count;
   report.geometry_rows = runtime.snapshot.timeframe_count;
   report.entry_idea_rows = runtime.snapshot.entry_idea_row_count;
   report.entry_decision_rows = runtime.snapshot.entry_decision_row_count;
   report.paper_ledger_rows = runtime.snapshot.paper_ledger_row_count;
   report.paper_lifecycle_rows = runtime.snapshot.paper_lifecycle_row_count;
   report.paper_result_rows = runtime.snapshot.paper_result_row_count;
   report.paper_portfolio_rows = runtime.snapshot.paper_portfolio_row_count;
   report.paper_regime_rows = runtime.snapshot.paper_regime_row_count;
   report.paper_filter_rows = runtime.snapshot.paper_filter_row_count;
   report.contract_rows = runtime.snapshot.timeframe_count;
}

void FP_StateGateFinalizeRun(const FP_StateGateConfig &cfg,
                             FP_StateGateRuntime &runtime,
                             FP_StateGateReport &report,
                             const string default_reason)
{
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
      if(report.reason == default_reason)
         report.reason = default_reason + "_no_closed_bar_change";
   }

   report.ok = (report.object_errors == 0 && report.file_errors == 0);
   if(!report.ok && report.reason == default_reason)
      report.reason = default_reason + "_errors";
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
   FP_StateGateFinalizeRun(cfg, runtime, report, FP_STATE_GATE_REASON_PHASE2);
}

void FP_RunStateGatePhase4(const string symbol,
                           const ENUM_TIMEFRAMES chart_period,
                           const FP_StateGateConfig &cfg,
                           const FP_TimebaseConfig &timebase_template,
                           const FP_Config &engine_template,
                           const int &scales[],
                           const int scale_count,
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

   FP_StateGateBuildPhase4Snapshot(symbol, chart_period, cfg, timebase_template, engine_template, scales, scale_count, runtime, report);
   FP_StateGateFinalizeRun(cfg, runtime, report, FP_STATE_GATE_REASON_PHASE4);
}


void FP_RunStateGatePhase5(const string symbol,
                           const ENUM_TIMEFRAMES chart_period,
                           const FP_StateGateConfig &cfg,
                           const FP_TimebaseConfig &timebase_template,
                           const FP_Config &engine_template,
                           const int &scales[],
                           const int scale_count,
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

   FP_RunStateGatePhase6(symbol, chart_period, cfg, timebase_template, engine_template, scales, scale_count, runtime, report);
}


void FP_RunStateGatePhase6(const string symbol,
                           const ENUM_TIMEFRAMES chart_period,
                           const FP_StateGateConfig &cfg,
                           const FP_TimebaseConfig &timebase_template,
                           const FP_Config &engine_template,
                           const int &scales[],
                           const int scale_count,
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

   FP_StateGateBuildPhase4Snapshot(symbol, chart_period, cfg, timebase_template, engine_template, scales, scale_count, runtime, report);
   runtime.snapshot.status = "phase6_state_contract_storage";
   runtime.snapshot.reason = FP_STATE_GATE_REASON_PHASE6;
   report.status = runtime.snapshot.status;
   report.reason = runtime.snapshot.reason;
   report.contract_rows = runtime.snapshot.timeframe_count;
   FP_StateGateFinalizeRun(cfg, runtime, report, FP_STATE_GATE_REASON_PHASE6);
}


void FP_RunStateGatePhase11(const string symbol,
                            const ENUM_TIMEFRAMES chart_period,
                            const FP_StateGateConfig &cfg,
                            const FP_TimebaseConfig &timebase_template,
                            const FP_Config &engine_template,
                            const int &scales[],
                            const int scale_count,
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

   FP_StateGateBuildPhase4Snapshot(symbol, chart_period, cfg, timebase_template, engine_template, scales, scale_count, runtime, report);
   runtime.snapshot.status = "phase11_entry_bridge_readiness";
   runtime.snapshot.reason = FP_STATE_GATE_REASON_PHASE11;
   report.status = runtime.snapshot.status;
   report.reason = runtime.snapshot.reason;
   report.contract_rows = runtime.snapshot.timeframe_count;
   FP_StateGateFinalizeRun(cfg, runtime, report, FP_STATE_GATE_REASON_PHASE11);
}



void FP_RunStateGatePhase12(const string symbol,
                            const ENUM_TIMEFRAMES chart_period,
                            const FP_StateGateConfig &cfg,
                            const FP_TimebaseConfig &timebase_template,
                            const FP_Config &engine_template,
                            const int &scales[],
                            const int scale_count,
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

   FP_StateGateBuildPhase4Snapshot(symbol, chart_period, cfg, timebase_template, engine_template, scales, scale_count, runtime, report);
   runtime.snapshot.status = "phase12_extreme_candidate_map";
   runtime.snapshot.reason = FP_STATE_GATE_REASON_PHASE12;
   report.status = runtime.snapshot.status;
   report.reason = runtime.snapshot.reason;
   report.contract_rows = runtime.snapshot.timeframe_count;
   report.extreme_candidate_rows = runtime.snapshot.extreme_candidate_row_count;
   report.mtf_alignment_rows = runtime.snapshot.mtf_alignment_row_count;
   report.geometry_rows = runtime.snapshot.timeframe_count;
   report.entry_idea_rows = runtime.snapshot.entry_idea_row_count;
   report.entry_decision_rows = runtime.snapshot.entry_decision_row_count;
   report.paper_ledger_rows = runtime.snapshot.paper_ledger_row_count;
   report.paper_lifecycle_rows = runtime.snapshot.paper_lifecycle_row_count;
   report.paper_result_rows = runtime.snapshot.paper_result_row_count;
   report.paper_portfolio_rows = runtime.snapshot.paper_portfolio_row_count;
   report.paper_regime_rows = runtime.snapshot.paper_regime_row_count;
   report.paper_filter_rows = runtime.snapshot.paper_filter_row_count;
   FP_StateGateFinalizeRun(cfg, runtime, report, FP_STATE_GATE_REASON_PHASE12);
}



void FP_RunStateGatePhase13(const string symbol,
                            const ENUM_TIMEFRAMES chart_period,
                            const FP_StateGateConfig &cfg,
                            const FP_TimebaseConfig &timebase_template,
                            const FP_Config &engine_template,
                            const int &scales[],
                            const int scale_count,
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

   FP_StateGateBuildPhase4Snapshot(symbol, chart_period, cfg, timebase_template, engine_template, scales, scale_count, runtime, report);
   runtime.snapshot.status = "phase13_mtf_alignment_map";
   runtime.snapshot.reason = FP_STATE_GATE_REASON_PHASE13;
   report.status = runtime.snapshot.status;
   report.reason = runtime.snapshot.reason;
   report.contract_rows = runtime.snapshot.timeframe_count;
   report.extreme_candidate_rows = runtime.snapshot.extreme_candidate_row_count;
   report.mtf_alignment_rows = runtime.snapshot.mtf_alignment_row_count;
   report.geometry_rows = runtime.snapshot.timeframe_count;
   report.entry_idea_rows = runtime.snapshot.entry_idea_row_count;
   report.entry_decision_rows = runtime.snapshot.entry_decision_row_count;
   report.paper_ledger_rows = runtime.snapshot.paper_ledger_row_count;
   report.paper_lifecycle_rows = runtime.snapshot.paper_lifecycle_row_count;
   report.paper_result_rows = runtime.snapshot.paper_result_row_count;
   report.paper_portfolio_rows = runtime.snapshot.paper_portfolio_row_count;
   report.paper_regime_rows = runtime.snapshot.paper_regime_row_count;
   report.paper_filter_rows = runtime.snapshot.paper_filter_row_count;
   FP_StateGateFinalizeRun(cfg, runtime, report, FP_STATE_GATE_REASON_PHASE13);
}



void FP_RunStateGatePhase14(const string symbol,
                            const ENUM_TIMEFRAMES chart_period,
                            const FP_StateGateConfig &cfg,
                            const FP_TimebaseConfig &timebase_template,
                            const FP_Config &engine_template,
                            const int &scales[],
                            const int scale_count,
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

   FP_StateGateBuildPhase4Snapshot(symbol, chart_period, cfg, timebase_template, engine_template, scales, scale_count, runtime, report);
   runtime.snapshot.status = "phase14_entry_geometry_readiness";
   runtime.snapshot.reason = FP_STATE_GATE_REASON_PHASE14;
   report.status = runtime.snapshot.status;
   report.reason = runtime.snapshot.reason;
   report.contract_rows = runtime.snapshot.timeframe_count;
   report.extreme_candidate_rows = runtime.snapshot.extreme_candidate_row_count;
   report.mtf_alignment_rows = runtime.snapshot.mtf_alignment_row_count;
   report.geometry_rows = runtime.snapshot.timeframe_count;
   report.entry_idea_rows = runtime.snapshot.entry_idea_row_count;
   report.entry_decision_rows = runtime.snapshot.entry_decision_row_count;
   report.paper_ledger_rows = runtime.snapshot.paper_ledger_row_count;
   report.paper_lifecycle_rows = runtime.snapshot.paper_lifecycle_row_count;
   report.paper_result_rows = runtime.snapshot.paper_result_row_count;
   report.paper_portfolio_rows = runtime.snapshot.paper_portfolio_row_count;
   report.paper_regime_rows = runtime.snapshot.paper_regime_row_count;
   report.paper_filter_rows = runtime.snapshot.paper_filter_row_count;
   FP_StateGateFinalizeRun(cfg, runtime, report, FP_STATE_GATE_REASON_PHASE14);
}



void FP_RunStateGatePhase15(const string symbol,
                            const ENUM_TIMEFRAMES chart_period,
                            const FP_StateGateConfig &cfg,
                            const FP_TimebaseConfig &timebase_template,
                            const FP_Config &engine_template,
                            const int &scales[],
                            const int scale_count,
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

   FP_StateGateBuildPhase4Snapshot(symbol, chart_period, cfg, timebase_template, engine_template, scales, scale_count, runtime, report);
   runtime.snapshot.status = "phase15_entry_idea_layer";
   runtime.snapshot.reason = FP_STATE_GATE_REASON_PHASE15;
   report.status = runtime.snapshot.status;
   report.reason = runtime.snapshot.reason;
   report.contract_rows = runtime.snapshot.timeframe_count;
   report.extreme_candidate_rows = runtime.snapshot.extreme_candidate_row_count;
   report.mtf_alignment_rows = runtime.snapshot.mtf_alignment_row_count;
   report.geometry_rows = runtime.snapshot.timeframe_count;
   report.entry_idea_rows = runtime.snapshot.entry_idea_row_count;
   report.entry_decision_rows = runtime.snapshot.entry_decision_row_count;
   report.paper_ledger_rows = runtime.snapshot.paper_ledger_row_count;
   report.paper_lifecycle_rows = runtime.snapshot.paper_lifecycle_row_count;
   report.paper_result_rows = runtime.snapshot.paper_result_row_count;
   report.paper_portfolio_rows = runtime.snapshot.paper_portfolio_row_count;
   report.paper_regime_rows = runtime.snapshot.paper_regime_row_count;
   report.paper_filter_rows = runtime.snapshot.paper_filter_row_count;
   FP_StateGateFinalizeRun(cfg, runtime, report, FP_STATE_GATE_REASON_PHASE15);
}



void FP_RunStateGatePhase16(const string symbol,
                            const ENUM_TIMEFRAMES chart_period,
                            const FP_StateGateConfig &cfg,
                            const FP_TimebaseConfig &timebase_template,
                            const FP_Config &engine_template,
                            const int &scales[],
                            const int scale_count,
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

   FP_StateGateBuildPhase4Snapshot(symbol, chart_period, cfg, timebase_template, engine_template, scales, scale_count, runtime, report);
   runtime.snapshot.status = "phase16_entry_decision_dry_run";
   runtime.snapshot.reason = FP_STATE_GATE_REASON_PHASE16;
   report.status = runtime.snapshot.status;
   report.reason = runtime.snapshot.reason;
   report.contract_rows = runtime.snapshot.timeframe_count;
   report.extreme_candidate_rows = runtime.snapshot.extreme_candidate_row_count;
   report.mtf_alignment_rows = runtime.snapshot.mtf_alignment_row_count;
   report.geometry_rows = runtime.snapshot.timeframe_count;
   report.entry_idea_rows = runtime.snapshot.entry_idea_row_count;
   report.entry_decision_rows = runtime.snapshot.entry_decision_row_count;
   report.paper_ledger_rows = runtime.snapshot.paper_ledger_row_count;
   report.paper_lifecycle_rows = runtime.snapshot.paper_lifecycle_row_count;
   report.paper_result_rows = runtime.snapshot.paper_result_row_count;
   report.paper_portfolio_rows = runtime.snapshot.paper_portfolio_row_count;
   report.paper_regime_rows = runtime.snapshot.paper_regime_row_count;
   report.paper_filter_rows = runtime.snapshot.paper_filter_row_count;
   FP_StateGateFinalizeRun(cfg, runtime, report, FP_STATE_GATE_REASON_PHASE16);
}



void FP_RunStateGatePhase17(const string symbol,
                            const ENUM_TIMEFRAMES chart_period,
                            const FP_StateGateConfig &cfg,
                            const FP_TimebaseConfig &timebase_template,
                            const FP_Config &engine_template,
                            const int &scales[],
                            const int scale_count,
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

   FP_StateGateBuildPhase4Snapshot(symbol, chart_period, cfg, timebase_template, engine_template, scales, scale_count, runtime, report);
   runtime.snapshot.status = "phase17_paper_execution_ledger";
   runtime.snapshot.reason = FP_STATE_GATE_REASON_PHASE17;
   report.status = runtime.snapshot.status;
   report.reason = runtime.snapshot.reason;
   report.contract_rows = runtime.snapshot.timeframe_count;
   report.extreme_candidate_rows = runtime.snapshot.extreme_candidate_row_count;
   report.mtf_alignment_rows = runtime.snapshot.mtf_alignment_row_count;
   report.geometry_rows = runtime.snapshot.timeframe_count;
   report.entry_idea_rows = runtime.snapshot.entry_idea_row_count;
   report.entry_decision_rows = runtime.snapshot.entry_decision_row_count;
   report.paper_ledger_rows = runtime.snapshot.paper_ledger_row_count;
   report.paper_lifecycle_rows = runtime.snapshot.paper_lifecycle_row_count;
   report.paper_result_rows = runtime.snapshot.paper_result_row_count;
   report.paper_portfolio_rows = runtime.snapshot.paper_portfolio_row_count;
   report.paper_regime_rows = runtime.snapshot.paper_regime_row_count;
   report.paper_filter_rows = runtime.snapshot.paper_filter_row_count;
   FP_StateGateFinalizeRun(cfg, runtime, report, FP_STATE_GATE_REASON_PHASE17);
}



void FP_RunStateGatePhase18(const string symbol,
                            const ENUM_TIMEFRAMES chart_period,
                            const FP_StateGateConfig &cfg,
                            const FP_TimebaseConfig &timebase_template,
                            const FP_Config &engine_template,
                            const int &scales[],
                            const int scale_count,
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

   FP_StateGateBuildPhase4Snapshot(symbol, chart_period, cfg, timebase_template, engine_template, scales, scale_count, runtime, report);
   runtime.snapshot.status = "phase18_paper_ledger_lifecycle_tracking";
   runtime.snapshot.reason = FP_STATE_GATE_REASON_PHASE18;
   report.status = runtime.snapshot.status;
   report.reason = runtime.snapshot.reason;
   report.contract_rows = runtime.snapshot.timeframe_count;
   report.extreme_candidate_rows = runtime.snapshot.extreme_candidate_row_count;
   report.mtf_alignment_rows = runtime.snapshot.mtf_alignment_row_count;
   report.geometry_rows = runtime.snapshot.timeframe_count;
   report.entry_idea_rows = runtime.snapshot.entry_idea_row_count;
   report.entry_decision_rows = runtime.snapshot.entry_decision_row_count;
   report.paper_ledger_rows = runtime.snapshot.paper_ledger_row_count;
   report.paper_lifecycle_rows = runtime.snapshot.paper_lifecycle_row_count;
   report.paper_result_rows = runtime.snapshot.paper_result_row_count;
   report.paper_portfolio_rows = runtime.snapshot.paper_portfolio_row_count;
   report.paper_regime_rows = runtime.snapshot.paper_regime_row_count;
   report.paper_filter_rows = runtime.snapshot.paper_filter_row_count;
   FP_StateGateFinalizeRun(cfg, runtime, report, FP_STATE_GATE_REASON_PHASE18);
}



void FP_RunStateGatePhase19(const string symbol,
                            const ENUM_TIMEFRAMES chart_period,
                            const FP_StateGateConfig &cfg,
                            const FP_TimebaseConfig &timebase_template,
                            const FP_Config &engine_template,
                            const int &scales[],
                            const int scale_count,
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

   FP_StateGateBuildPhase4Snapshot(symbol, chart_period, cfg, timebase_template, engine_template, scales, scale_count, runtime, report);
   runtime.snapshot.status = "phase19_paper_result_metrics";
   runtime.snapshot.reason = FP_STATE_GATE_REASON_PHASE19;
   report.status = runtime.snapshot.status;
   report.reason = runtime.snapshot.reason;
   report.contract_rows = runtime.snapshot.timeframe_count;
   report.extreme_candidate_rows = runtime.snapshot.extreme_candidate_row_count;
   report.mtf_alignment_rows = runtime.snapshot.mtf_alignment_row_count;
   report.geometry_rows = runtime.snapshot.timeframe_count;
   report.entry_idea_rows = runtime.snapshot.entry_idea_row_count;
   report.entry_decision_rows = runtime.snapshot.entry_decision_row_count;
   report.paper_ledger_rows = runtime.snapshot.paper_ledger_row_count;
   report.paper_lifecycle_rows = runtime.snapshot.paper_lifecycle_row_count;
   report.paper_result_rows = runtime.snapshot.paper_result_row_count;
   report.paper_portfolio_rows = runtime.snapshot.paper_portfolio_row_count;
   report.paper_regime_rows = runtime.snapshot.paper_regime_row_count;
   report.paper_filter_rows = runtime.snapshot.paper_filter_row_count;
   FP_StateGateFinalizeRun(cfg, runtime, report, FP_STATE_GATE_REASON_PHASE19);
}



void FP_RunStateGatePhase20(const string symbol,
                            const ENUM_TIMEFRAMES chart_period,
                            const FP_StateGateConfig &cfg,
                            const FP_TimebaseConfig &timebase_template,
                            const FP_Config &engine_template,
                            const int &scales[],
                            const int scale_count,
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

   FP_StateGateBuildPhase4Snapshot(symbol, chart_period, cfg, timebase_template, engine_template, scales, scale_count, runtime, report);
   runtime.snapshot.status = "phase20_paper_portfolio_aggregate_metrics";
   runtime.snapshot.reason = FP_STATE_GATE_REASON_PHASE20;
   report.status = runtime.snapshot.status;
   report.reason = runtime.snapshot.reason;
   report.contract_rows = runtime.snapshot.timeframe_count;
   report.extreme_candidate_rows = runtime.snapshot.extreme_candidate_row_count;
   report.mtf_alignment_rows = runtime.snapshot.mtf_alignment_row_count;
   report.geometry_rows = runtime.snapshot.timeframe_count;
   report.entry_idea_rows = runtime.snapshot.entry_idea_row_count;
   report.entry_decision_rows = runtime.snapshot.entry_decision_row_count;
   report.paper_ledger_rows = runtime.snapshot.paper_ledger_row_count;
   report.paper_lifecycle_rows = runtime.snapshot.paper_lifecycle_row_count;
   report.paper_result_rows = runtime.snapshot.paper_result_row_count;
   report.paper_portfolio_rows = runtime.snapshot.paper_portfolio_row_count;
   report.paper_regime_rows = runtime.snapshot.paper_regime_row_count;
   report.paper_filter_rows = runtime.snapshot.paper_filter_row_count;
   FP_StateGateFinalizeRun(cfg, runtime, report, FP_STATE_GATE_REASON_PHASE20);
}



void FP_RunStateGatePhase21(const string symbol,
                            const ENUM_TIMEFRAMES chart_period,
                            const FP_StateGateConfig &cfg,
                            const FP_TimebaseConfig &timebase_template,
                            const FP_Config &engine_template,
                            const int &scales[],
                            const int scale_count,
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

   FP_StateGateBuildPhase4Snapshot(symbol, chart_period, cfg, timebase_template, engine_template, scales, scale_count, runtime, report);
   runtime.snapshot.status = "phase21_paper_regime_attribution";
   runtime.snapshot.reason = FP_STATE_GATE_REASON_PHASE21;
   report.status = runtime.snapshot.status;
   report.reason = runtime.snapshot.reason;
   report.contract_rows = runtime.snapshot.timeframe_count;
   report.extreme_candidate_rows = runtime.snapshot.extreme_candidate_row_count;
   report.mtf_alignment_rows = runtime.snapshot.mtf_alignment_row_count;
   report.geometry_rows = runtime.snapshot.timeframe_count;
   report.entry_idea_rows = runtime.snapshot.entry_idea_row_count;
   report.entry_decision_rows = runtime.snapshot.entry_decision_row_count;
   report.paper_ledger_rows = runtime.snapshot.paper_ledger_row_count;
   report.paper_lifecycle_rows = runtime.snapshot.paper_lifecycle_row_count;
   report.paper_result_rows = runtime.snapshot.paper_result_row_count;
   report.paper_portfolio_rows = runtime.snapshot.paper_portfolio_row_count;
   report.paper_regime_rows = runtime.snapshot.paper_regime_row_count;
   report.paper_filter_rows = runtime.snapshot.paper_filter_row_count;
   FP_StateGateFinalizeRun(cfg, runtime, report, FP_STATE_GATE_REASON_PHASE21);
}



void FP_RunStateGatePhase22(const string symbol,
                            const ENUM_TIMEFRAMES chart_period,
                            const FP_StateGateConfig &cfg,
                            const FP_TimebaseConfig &timebase_template,
                            const FP_Config &engine_template,
                            const int &scales[],
                            const int scale_count,
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

   FP_StateGateBuildPhase4Snapshot(symbol, chart_period, cfg, timebase_template, engine_template, scales, scale_count, runtime, report);
   runtime.snapshot.status = "phase22_paper_filter_diagnostics";
   runtime.snapshot.reason = FP_STATE_GATE_REASON_PHASE22;
   report.status = runtime.snapshot.status;
   report.reason = runtime.snapshot.reason;
   report.contract_rows = runtime.snapshot.timeframe_count;
   report.extreme_candidate_rows = runtime.snapshot.extreme_candidate_row_count;
   report.mtf_alignment_rows = runtime.snapshot.mtf_alignment_row_count;
   report.geometry_rows = runtime.snapshot.timeframe_count;
   report.entry_idea_rows = runtime.snapshot.entry_idea_row_count;
   report.entry_decision_rows = runtime.snapshot.entry_decision_row_count;
   report.paper_ledger_rows = runtime.snapshot.paper_ledger_row_count;
   report.paper_lifecycle_rows = runtime.snapshot.paper_lifecycle_row_count;
   report.paper_result_rows = runtime.snapshot.paper_result_row_count;
   report.paper_portfolio_rows = runtime.snapshot.paper_portfolio_row_count;
   report.paper_regime_rows = runtime.snapshot.paper_regime_row_count;
   report.paper_filter_rows = runtime.snapshot.paper_filter_row_count;
   FP_StateGateFinalizeRun(cfg, runtime, report, FP_STATE_GATE_REASON_PHASE22);
}


void FP_RunStateGatePhase3(const string symbol,
                           const ENUM_TIMEFRAMES chart_period,
                           const FP_StateGateConfig &cfg,
                           const FP_TimebaseConfig &timebase_template,
                           const FP_Config &engine_template,
                           const int &scales[],
                           const int scale_count,
                           FP_StateGateRuntime &runtime,
                           FP_StateGateReport &report)
{
   FP_RunStateGatePhase6(symbol, chart_period, cfg, timebase_template, engine_template, scales, scale_count, runtime, report);
}

// Backward-compatible aliases for older integration names.  Phase 1/2 callers
// still compile, while the main EA now uses Phase 5 explicitly.
void FP_RunStateGatePhase1(const string symbol,
                           const ENUM_TIMEFRAMES chart_period,
                           const FP_StateGateConfig &cfg,
                           FP_StateGateRuntime &runtime,
                           FP_StateGateReport &report)
{
   FP_RunStateGatePhase2(symbol, chart_period, cfg, runtime, report);
}

#endif // __FP_STATE_GATE_ENGINE_MQH__
