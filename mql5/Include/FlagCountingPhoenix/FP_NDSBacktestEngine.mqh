#ifndef __FP_NDS_BACKTEST_ENGINE_MQH__
#define __FP_NDS_BACKTEST_ENGINE_MQH__
#property strict

// Exact-accelerated Strategy Tester pipeline.
// Accuracy contract:
// - identical closed-bar universe, scale list and detector thresholds;
// - identical broker order model and per-bar invocation schedule;
// - only decision-irrelevant engines are skipped;
// - InpBTExactAcceleration=false retains the full reference path.
#include "FP_Timebase.mqh"
#include "FP_NodeScaleList.mqh"
#include "FP_SequenceEngine.mqh"
#include "FP_HookPhase02DetectionCore.mqh"
#include "FP_NDSHookTradeExecutionCore.mqh"
#include "FP_NDSHook864CycleR1EvidenceEngine.mqh"
#include "FP_NDSBacktestTypes.mqh"

void FP_NDSBacktestApplyProfile(FP_NDSBacktestRuntimeConfig &cfg)
{
   if(cfg.profile == FP_NDS_BACKTEST_PROFILE_FAST)
   {
      cfg.requested_bars = 1200;
      cfg.hook_scan_bars = 1200;
      cfg.min_closed_bars = 200;
      cfg.use_multi_scale = true;
      cfg.scale_l1 = 2;
      cfg.scale_l2 = 3;
      cfg.scale_l3 = 5;
      cfg.scale_l4 = 8;
      cfg.scale_l5 = 0;
      cfg.scale_l6 = 0;
      cfg.scale_l7 = 0;
      cfg.scale_l8 = 0;
      cfg.max_events = 2500;
      cfg.max_hooks = 2500;
   }
   else if(cfg.profile == FP_NDS_BACKTEST_PROFILE_PARITY)
   {
      cfg.requested_bars = 5000;
      cfg.hook_scan_bars = 5000;
      cfg.min_closed_bars = 200;
      cfg.use_multi_scale = true;
      cfg.scale_l1 = 2;
      cfg.scale_l2 = 3;
      cfg.scale_l3 = 5;
      cfg.scale_l4 = 8;
      cfg.scale_l5 = 13;
      cfg.scale_l6 = 21;
      cfg.scale_l7 = 34;
      cfg.scale_l8 = 55;
      cfg.max_events = 6000;
      cfg.max_hooks = 6000;
   }

   if(cfg.requested_bars < 200) cfg.requested_bars = 200;
   if(cfg.min_closed_bars < 50) cfg.min_closed_bars = 50;
   if(cfg.hook_scan_bars <= 0 || cfg.hook_scan_bars > cfg.requested_bars)
      cfg.hook_scan_bars = cfg.requested_bars;
   if(cfg.max_events < 100) cfg.max_events = 100;
   if(cfg.max_hooks < 100) cfg.max_hooks = 100;
   if(cfg.print_every_n_runs < 1) cfg.print_every_n_runs = 1;
}

int FP_NDSBacktestBuildScales(const FP_NDSBacktestRuntimeConfig &cfg,
                              int &scales[])
{
   return FP_BuildScaleList(cfg.use_multi_scale,
                            cfg.scale_l1,
                            cfg.scale_l2,
                            cfg.scale_l3,
                            cfg.scale_l4,
                            cfg.scale_l5,
                            cfg.scale_l6,
                            cfg.scale_l7,
                            cfg.scale_l8,
                            scales);
}

void FP_NDSBacktestMarkSkippedHookReports(const string reason,
                                          FP_NDSBacktestRunReport &report)
{
   FP_NDSClearStructureSnapshot();
   FP_NDSClearHook864CycleR1EvidenceSnapshot();

   report.hook_phase02_report.ok = true;
   report.hook_phase02_report.status = "HOOK_P02_SKIPPED_EXACT_FAST_PATH";
   report.hook_phase02_report.reason = reason;
   report.hook_phase03_report.ok = true;
   report.hook_phase03_report.status = "HOOK_P03_SKIPPED_EXACT_FAST_PATH";
   report.hook_phase03_report.reason = reason;
   report.hook_phase04_report.ok = true;
   report.hook_phase04_report.status = "HOOK_P04_SKIPPED_EXACT_FAST_PATH";
   report.hook_phase04_report.reason = reason;
}

// Returns true only when the current broker state can be processed exactly
// without canonical rates, Hook snapshots or F events. A same-symbol legacy
// TERMINAL_F123 position is the sole managed-exposure case that still requires
// the F engine because its exit is owned by a post-entry same-direction F3.
bool FP_NDSBacktestExposureFastPathAvailable(
   const string symbol,
   const FP_NDSBacktestRuntimeConfig &runtime_cfg,
   const FP_NDSHookTradeConfig &trade_cfg,
   bool &legacy_position_f_only,
   string &reason)
{
   legacy_position_f_only = false;
   reason = "no_fast_path";
   if(!runtime_cfg.exact_acceleration)
      return false;
   if(!trade_cfg.enabled)
   {
      reason = "trade_disabled_no_structure_required";
      return true;
   }

   ulong first_position = 0;
   ulong first_order = 0;
   int position_count = FP_NDSHookTradeCountManagedPositions(trade_cfg, first_position);
   int pending_count = FP_NDSHookTradeCountManagedOrders(trade_cfg, first_order);

   if(position_count > 1)
   {
      reason = "multiple_managed_positions_invariant_path";
      return true;
   }

   if(position_count == 1)
   {
      if(!runtime_cfg.skip_hook_rebuild_while_position_open)
         return false;

      ulong position_ticket = 0;
      int position_direction = FP_DIR_NONE;
      datetime position_open_time = 0;
      if(!FP_NDSHookTradeFindManagedPositionForSymbol(symbol, trade_cfg,
                                                      position_ticket,
                                                      position_direction,
                                                      position_open_time))
      {
         reason = "managed_position_on_other_symbol";
         return true;
      }

      if(position_ticket == 0 || !PositionSelectByTicket(position_ticket))
      {
         reason = "managed_position_profile_block_path";
         return true;
      }

      FP_NDSHookTradeProfile owned_profile;
      string profile_reason;
      if(!FP_NDSHookTradeProfileFromBrokerComment(
            trade_cfg, PositionGetString(POSITION_COMMENT),
            owned_profile, profile_reason))
      {
         reason = "managed_position_unknown_profile_block_path";
         return true;
      }

      if(owned_profile == FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1)
      {
         reason = "fixed_r_position_broker_sl_tp_owns_exit";
         return true;
      }

      // TERMINAL_F123 needs the full F event graph for its exit decision, but
      // Phase01/02 Hook and Phase03/04 closure rebuilds remain irrelevant.
      legacy_position_f_only = true;
      reason = "terminal_f123_position_requires_f_events_only";
      return false;
   }

   if(pending_count > 0)
   {
      reason = "pending_lifecycle_uses_broker_order_state";
      return true;
   }

   int foreign_count = FP_NDSHookTradeCountForeignPositionsOnSymbol(symbol, trade_cfg);
   if(foreign_count > 0)
   {
      reason = "foreign_symbol_position_guard";
      return true;
   }

   return false;
}

bool FP_NDSBacktestNeedsOpposingF3Context(
   const FP_HookPhase02Sequence &sequences[],
   const FP_NDSHookTradeConfig &trade_cfg)
{
   for(int i=0; i<ArraySize(sequences); i++)
   {
      if(FP_NDSHook864CycleR1PotentialOpposingF3Candidate(sequences[i], trade_cfg))
         return true;
   }
   return false;
}

void FP_NDSBacktestUpdateStats(const FP_NDSBacktestRunReport &report,
                               FP_NDSBacktestSessionStats &stats)
{
   stats.runs++;
   if(report.ok) stats.successful_runs++;
   else stats.failed_runs++;
   if(report.hook_snapshot_rebuilt) stats.hook_rebuild_runs++;
   if(report.hook_snapshot_skipped_for_open_position) stats.position_fast_path_runs++;
   if(report.exposure_fast_path) stats.exposure_fast_path_runs++;
   if(report.f_context_built) stats.f_context_built_runs++;
   if(report.f_context_deferred) stats.f_context_deferred_runs++;
   if(report.phase04_candidate_sequences > 0)
      stats.phase04_candidate_sequences_total += (ulong)report.phase04_candidate_sequences;

   if(report.hook_phase04_report.x_closed_count > 0)
      stats.phase04_closed_total += (ulong)report.hook_phase04_report.x_closed_count;
   if(report.trade_report.funnel.phase04_evidence_found > 0)
      stats.phase04_evidence_total += (ulong)report.trade_report.funnel.phase04_evidence_found;
   if(report.trade_report.funnel.first_864_untouched > 0)
      stats.first_864_untouched_total += (ulong)report.trade_report.funnel.first_864_untouched;
   if(report.trade_report.funnel.execution_ready > 0)
      stats.execution_ready_runs++;
   else if(report.trade_report.action == FP_NDS_HOOK_TRADE_ACTION_NONE)
      stats.no_candidate_runs++;

   if(report.trade_report.action == FP_NDS_HOOK_TRADE_ACTION_PAPER_LIMIT)
      stats.paper_limit_ready_runs++;
   else if(report.trade_report.action == FP_NDS_HOOK_TRADE_ACTION_LIMIT_SENT)
      stats.limit_sent_runs++;
   else if(report.trade_report.action == FP_NDS_HOOK_TRADE_ACTION_PENDING_HELD)
      stats.pending_held_runs++;
   else if(report.trade_report.action == FP_NDS_HOOK_TRADE_ACTION_POSITION_HELD)
      stats.position_held_runs++;
   else if(report.trade_report.action == FP_NDS_HOOK_TRADE_ACTION_PENDING_CANCELLED)
      stats.pending_cancelled_runs++;
   else if(report.trade_report.action == FP_NDS_HOOK_TRADE_ACTION_POSITION_CLOSED_F3)
      stats.position_closed_runs++;
   else if(report.trade_report.action == FP_NDS_HOOK_TRADE_ACTION_BLOCKED)
      stats.blocked_runs++;

   stats.last_microseconds = report.elapsed_microseconds;
   stats.total_microseconds += report.elapsed_microseconds;
   if(report.elapsed_microseconds > stats.max_microseconds)
      stats.max_microseconds = report.elapsed_microseconds;
   if(stats.first_run_time <= 0)
      stats.first_run_time = report.generated_at;
   stats.last_run_time = report.generated_at;
}

void FP_NDSBacktestFinalizeTiming(const ulong started,
                                  FP_NDSBacktestRunReport &report)
{
   ulong finished = GetMicrosecondCount();
   report.elapsed_microseconds = (finished >= started ? finished - started : 0);
}

bool FP_RunNDSLightweightBacktestCycle(const string symbol,
                                       const ENUM_TIMEFRAMES period,
                                       const FP_NDSBacktestRuntimeConfig &runtime_cfg,
                                       const FP_Config &detector_cfg,
                                       const FP_HookPhase01Config &node_cfg,
                                       const FP_HookPhase02Config &hook_cfg,
                                       const FP_NDSHookTradeConfig &trade_cfg,
                                       FP_NDSBacktestRunReport &report)
{
   FP_ResetNDSBacktestRunReport(report);
   report.generated_at = TimeCurrent();
   report.symbol = symbol;
   report.period = period;
   report.attempted = true;

   ulong started = GetMicrosecondCount();

   // Exact exposure lifecycle preflight occurs before CopyRates and every
   // structural engine. Pending orders and fixed-R positions are broker-owned;
   // rebuilding 5000 bars x 8 scales cannot alter their lifecycle decision.
   string exposure_fast_reason;
   bool legacy_position_f_only = false;
   if(FP_NDSBacktestExposureFastPathAvailable(symbol, runtime_cfg, trade_cfg,
                                              legacy_position_f_only,
                                              exposure_fast_reason))
   {
      FP_FlagEvent no_events[];
      ArrayResize(no_events, 0);
      FP_NDSBacktestMarkSkippedHookReports(exposure_fast_reason, report);
      report.exposure_fast_path = true;
      report.exposure_fast_path_reason = exposure_fast_reason;
      report.hook_snapshot_skipped_for_open_position =
         (StringFind(exposure_fast_reason, "position") >= 0);

      FP_RunNDSHookTradeExecutionCore(symbol, period,
                                     no_events, 0,
                                     trade_cfg,
                                     report.trade_report);
      report.ok = report.trade_report.ok;
      report.status = report.trade_report.status;
      report.reason = report.trade_report.reason;
      FP_NDSBacktestFinalizeTiming(started, report);
      return report.ok;
   }

   FP_TimebaseConfig timebase_cfg;
   FP_DefaultTimebaseConfig(timebase_cfg);
   timebase_cfg.symbol = symbol;
   timebase_cfg.period = period;
   timebase_cfg.requested_bars = runtime_cfg.requested_bars;
   timebase_cfg.min_closed_bars = runtime_cfg.min_closed_bars;
   timebase_cfg.exclude_live_bar = runtime_cfg.use_closed_bars_only;
   timebase_cfg.require_ascending_time = true;
   timebase_cfg.strict_contract = runtime_cfg.strict_timebase;
   timebase_cfg.print_sanity = false;
   timebase_cfg.print_samples = false;

   MqlRates rates[];
   FP_TimebaseReport timebase_report;
   int copied = FP_LoadCanonicalRates(timebase_cfg, rates, timebase_report);
   report.copied_bars = copied;

   if(!timebase_report.ok && runtime_cfg.strict_timebase)
   {
      report.ok = false;
      report.status = "TIMEBASE_FAILED";
      report.reason = timebase_report.reason;
      FP_NDSBacktestFinalizeTiming(started, report);
      return false;
   }
   if(copied < runtime_cfg.min_closed_bars)
   {
      report.ok = false;
      report.status = "NOT_ENOUGH_CLOSED_BARS";
      report.reason = "copied_bars_below_minimum";
      FP_NDSBacktestFinalizeTiming(started, report);
      return false;
   }

   int scales[];
   int scale_count = FP_NDSBacktestBuildScales(runtime_cfg, scales);
   report.scale_count = scale_count;
   if(scale_count <= 0)
   {
      report.ok = false;
      report.status = "NO_VALID_SCALES";
      report.reason = "scale_profile_produced_empty_list";
      FP_NDSBacktestFinalizeTiming(started, report);
      return false;
   }

   FP_FlagEvent events[];
   FP_HookBranch hooks[];
   ArrayResize(events, 0);
   ArrayResize(hooks, 0);
   FP_HookPhase02Sequence sequences[];

   if(runtime_cfg.exact_acceleration && legacy_position_f_only)
   {
      FP_DetectResult detect_result;
      FP_DetectAllScales(rates, copied, scales, scale_count,
                         detector_cfg, events, hooks, detect_result);
      report.event_count = ArraySize(events);
      report.hook_count = ArraySize(hooks);
      report.f_context_required = true;
      report.f_context_built = true;
      report.exposure_fast_path = true;
      report.exposure_fast_path_reason = exposure_fast_reason;
      report.hook_snapshot_skipped_for_open_position = true;
      FP_NDSBacktestMarkSkippedHookReports(exposure_fast_reason, report);

      FP_RunNDSHookTradeExecutionCore(symbol, period,
                                     events, ArraySize(events),
                                     trade_cfg,
                                     report.trade_report);
      report.ok = report.trade_report.ok;
      report.status = report.trade_report.status;
      report.reason = report.trade_report.reason;
      FP_NDSBacktestFinalizeTiming(started, report);
      return report.ok;
   }

   bool is_864 = (trade_cfg.profile == FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1);
   if(is_864 && runtime_cfg.exact_acceleration)
   {
      // Build Hook/Node truth first, without F. Phase02 already applies the
      // canonical Hook-after-Hook family. Only an otherwise viable sequence that
      // could gain opposing-F3 ownership can make the F graph decision-relevant.
      FP_RunHookPhase02DetectionCore(symbol, period,
                                     rates, copied,
                                     scales, scale_count,
                                     node_cfg, hook_cfg,
                                     events, 0,
                                     false,
                                     sequences,
                                     report.hook_phase02_report);
      report.hook_snapshot_rebuilt = true;

      report.f_context_required = FP_NDSBacktestNeedsOpposingF3Context(
         sequences, trade_cfg);
      if(report.f_context_required)
      {
         FP_DetectResult detect_result;
         FP_DetectAllScales(rates, copied, scales, scale_count,
                            detector_cfg, events, hooks, detect_result);
         report.event_count = ArraySize(events);
         report.hook_count = ArraySize(hooks);
         report.f_context_built = true;

         FP_HookP02AnnotateValidityFamiliesWithF3(sequences,
                                                 events, ArraySize(events),
                                                 hook_cfg,
                                                 report.hook_phase02_report);
         FP_NDSCaptureStructureSnapshot(symbol, period, sequences);
         FP_HookP02FinalizeReport(report.hook_phase02_report);
      }
      else
      {
         report.f_context_deferred = true;
      }

      report.phase04_candidate_scoped = true;
      FP_RunNDSHook864CycleR1EvidenceEngine(symbol, period,
                                            rates, copied,
                                            sequences, hook_cfg, trade_cfg,
                                            true,
                                            report.hook_phase03_report,
                                            report.hook_phase04_report,
                                            report.phase04_candidate_sequences);
   }
   else
   {
      // Reference path: full F graph first, then F-aware Phase02. This remains
      // available as a parity oracle by setting InpBTExactAcceleration=false.
      FP_DetectResult detect_result;
      FP_DetectAllScales(rates, copied, scales, scale_count,
                         detector_cfg, events, hooks, detect_result);
      report.event_count = ArraySize(events);
      report.hook_count = ArraySize(hooks);
      report.f_context_required = true;
      report.f_context_built = true;

      FP_RunHookPhase02DetectionCore(symbol, period,
                                     rates, copied,
                                     scales, scale_count,
                                     node_cfg, hook_cfg,
                                     events, ArraySize(events),
                                     true,
                                     sequences,
                                     report.hook_phase02_report);
      report.hook_snapshot_rebuilt = true;

      if(is_864)
      {
         report.phase04_candidate_scoped = false;
         FP_RunNDSHook864CycleR1EvidenceEngine(symbol, period,
                                               rates, copied,
                                               sequences, hook_cfg, trade_cfg,
                                               false,
                                               report.hook_phase03_report,
                                               report.hook_phase04_report,
                                               report.phase04_candidate_sequences);
      }
      else
      {
         // TERMINAL_F123 consumes only Phase02 + F events. Phase03/04 are not in
         // its executable contract, so running them cannot change an order.
         FP_NDSClearHook864CycleR1EvidenceSnapshot();
         report.hook_phase03_report.ok = true;
         report.hook_phase03_report.status = "HOOK_P03_NOT_REQUIRED_TERMINAL_F123";
         report.hook_phase03_report.reason = "profile_does_not_consume_phase03";
         report.hook_phase04_report.ok = true;
         report.hook_phase04_report.status = "HOOK_P04_NOT_REQUIRED_TERMINAL_F123";
         report.hook_phase04_report.reason = "profile_does_not_consume_phase04";
      }
   }

   FP_RunNDSHookTradeExecutionCore(symbol, period,
                                   events, ArraySize(events),
                                   trade_cfg,
                                   report.trade_report);

   report.ok = report.trade_report.ok;
   report.status = report.trade_report.status;
   report.reason = report.trade_report.reason;
   FP_NDSBacktestFinalizeTiming(started, report);
   return report.ok;
}

void FP_PrintNDSBacktestRunReport(const string tag,
                                  const FP_NDSBacktestRuntimeConfig &cfg,
                                  const FP_NDSBacktestRunReport &report)
{
   string message = tag;
   message += " profile=" + FP_NDSBacktestProfileName(cfg.profile);
   message += " exact=" + (cfg.exact_acceleration ? "true" : "false");
   message += " ok=" + (report.ok ? "true" : "false");
   message += " status=" + report.status;
   message += " action=" + FP_NDSHookTradeActionName(report.trade_report.action);
   message += " setup_key=" + (report.trade_report.setup.setup_key == "" ? "none" : report.trade_report.setup.setup_key);
   message += " entry=" + DoubleToString(report.trade_report.setup.entry_price, _Digits);
   message += " stop=" + DoubleToString(report.trade_report.setup.stop_price, _Digits);
   message += " target=" + DoubleToString(report.trade_report.setup.target_price, _Digits);
   message += " reason=" + report.reason;
   message += " bars=" + IntegerToString(report.copied_bars);
   message += " scales=" + IntegerToString(report.scale_count);
   message += " events=" + IntegerToString(report.event_count);
   message += " hooks=" + IntegerToString(report.hook_count);
   message += " hook_rebuilt=" + (report.hook_snapshot_rebuilt ? "true" : "false");
   message += " p02_sequences=" + IntegerToString(report.hook_phase02_report.sequences_total);
   message += " p03_records=" + IntegerToString(report.hook_phase03_report.records_total);
   message += " p04_candidates=" + IntegerToString(report.phase04_candidate_sequences);
   message += " p04_closed=" + IntegerToString(report.hook_phase04_report.x_closed_count);
   message += " funnel={" + FP_NDSHook864CycleR1FunnelSummary(report.trade_report.funnel) + "}";
   message += " exposure_fast=" + (report.exposure_fast_path ? "true" : "false");
   if(report.exposure_fast_path)
      message += " exposure_reason=" + report.exposure_fast_path_reason;
   message += " f_required=" + (report.f_context_required ? "true" : "false");
   message += " f_built=" + (report.f_context_built ? "true" : "false");
   message += " f_deferred=" + (report.f_context_deferred ? "true" : "false");
   message += " p04_scoped=" + (report.phase04_candidate_scoped ? "true" : "false");
   message += " elapsed_us=" + IntegerToString((long)report.elapsed_microseconds);
   Print(message);
}

void FP_PrintNDSBacktestSessionStats(const string tag,
                                     const FP_NDSBacktestSessionStats &stats)
{
   ulong average = (stats.runs > 0 ? stats.total_microseconds / stats.runs : 0);
   string message = tag;
   message += " runs=" + IntegerToString((long)stats.runs);
   message += " ok=" + IntegerToString((long)stats.successful_runs);
   message += " failed=" + IntegerToString((long)stats.failed_runs);
   message += " hook_rebuilds=" + IntegerToString((long)stats.hook_rebuild_runs);
   message += " position_fast_paths=" + IntegerToString((long)stats.position_fast_path_runs);
   message += " exposure_fast_paths=" + IntegerToString((long)stats.exposure_fast_path_runs);
   message += " f_built_runs=" + IntegerToString((long)stats.f_context_built_runs);
   message += " f_deferred_runs=" + IntegerToString((long)stats.f_context_deferred_runs);
   message += " p04_candidate_total=" + IntegerToString((long)stats.phase04_candidate_sequences_total);
   message += " no_candidate_runs=" + IntegerToString((long)stats.no_candidate_runs);
   message += " ready_runs=" + IntegerToString((long)stats.execution_ready_runs);
   message += " paper_ready=" + IntegerToString((long)stats.paper_limit_ready_runs);
   message += " limits_sent=" + IntegerToString((long)stats.limit_sent_runs);
   message += " pending_held=" + IntegerToString((long)stats.pending_held_runs);
   message += " position_held=" + IntegerToString((long)stats.position_held_runs);
   message += " cancelled=" + IntegerToString((long)stats.pending_cancelled_runs);
   message += " f3_closed=" + IntegerToString((long)stats.position_closed_runs);
   message += " blocked=" + IntegerToString((long)stats.blocked_runs);
   message += " p04_closed_total=" + IntegerToString((long)stats.phase04_closed_total);
   message += " p04_evidence_total=" + IntegerToString((long)stats.phase04_evidence_total);
   message += " untouched864_total=" + IntegerToString((long)stats.first_864_untouched_total);
   message += " avg_us=" + IntegerToString((long)average);
   message += " max_us=" + IntegerToString((long)stats.max_microseconds);
   message += " last_us=" + IntegerToString((long)stats.last_microseconds);
   Print(message);
}

#endif // __FP_NDS_BACKTEST_ENGINE_MQH__
