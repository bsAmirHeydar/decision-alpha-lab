#ifndef __FP_NDS_BACKTEST_ENGINE_MQH__
#define __FP_NDS_BACKTEST_ENGINE_MQH__
#property strict

// Lightweight Strategy Tester pipeline. It intentionally depends only on the
// canonical timebase, the F/Rally detector, Hook Phase 02 ownership snapshot,
// and the executable Hook-limit/F123 trade state machine.
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

bool FP_NDSBacktestManagedPositionExists(const FP_NDSHookTradeConfig &trade_cfg)
{
   ulong ticket = 0;
   return (FP_NDSHookTradeCountManagedPositions(trade_cfg, ticket) > 0);
}

void FP_NDSBacktestUpdateStats(const FP_NDSBacktestRunReport &report,
                               FP_NDSBacktestSessionStats &stats)
{
   stats.runs++;
   if(report.ok) stats.successful_runs++;
   else stats.failed_runs++;
   if(report.hook_snapshot_rebuilt) stats.hook_rebuild_runs++;
   if(report.hook_snapshot_skipped_for_open_position) stats.position_fast_path_runs++;

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

   if(report.trade_report.action == FP_NDS_HOOK_TRADE_ACTION_PAPER_LIMIT_READY)
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
   FP_DetectResult detect_result;
   FP_DetectAllScales(rates, copied, scales, scale_count,
                      detector_cfg, events, hooks, detect_result);
   report.event_count = ArraySize(events);
   report.hook_count = ArraySize(hooks);

   FP_HookPhase02Sequence sequences[];
   bool position_fast_path = (runtime_cfg.skip_hook_rebuild_while_position_open &&
                              FP_NDSBacktestManagedPositionExists(trade_cfg));
   if(position_fast_path)
   {
      // The execution engine handles an open position before consulting Hook
      // and closure snapshots. The fixed-R profile verifies broker SL/TP only.
      FP_NDSClearStructureSnapshot();
      FP_NDSClearHook864CycleR1EvidenceSnapshot();
      report.hook_snapshot_skipped_for_open_position = true;
      report.hook_phase02_report.ok = true;
      report.hook_phase02_report.status = "HOOK_P02_SKIPPED_POSITION_FAST_PATH";
      report.hook_phase02_report.reason = "open_position_uses_existing_exit_ownership";
      report.hook_phase03_report.ok = true;
      report.hook_phase03_report.status = "HOOK_P03_SKIPPED_POSITION_FAST_PATH";
      report.hook_phase03_report.reason = "open_position_no_new_entry_evidence_required";
      report.hook_phase04_report.ok = true;
      report.hook_phase04_report.status = "HOOK_P04_SKIPPED_POSITION_FAST_PATH";
      report.hook_phase04_report.reason = "open_position_no_new_entry_evidence_required";
   }
   else
   {
      FP_RunHookPhase02DetectionCore(symbol, period,
                                     rates, copied,
                                     scales, scale_count,
                                     node_cfg, hook_cfg,
                                     events, ArraySize(events),
                                     true,
                                     sequences,
                                     report.hook_phase02_report);
      report.hook_snapshot_rebuilt = true;

      // The 86.4 profile consumes the canonical Phase03/04 closure engines.
      // The legacy terminal/F123 profile does not require this snapshot, but
      // building it keeps the tester report comparable across profiles.
      FP_RunNDSHook864CycleR1EvidenceEngine(symbol, period,
                                             rates, copied,
                                             sequences, hook_cfg,
                                             report.hook_phase03_report,
                                             report.hook_phase04_report);
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
   message += " ok=" + (report.ok ? "true" : "false");
   message += " status=" + report.status;
   message += " reason=" + report.reason;
   message += " bars=" + IntegerToString(report.copied_bars);
   message += " scales=" + IntegerToString(report.scale_count);
   message += " events=" + IntegerToString(report.event_count);
   message += " hooks=" + IntegerToString(report.hook_count);
   message += " hook_rebuilt=" + (report.hook_snapshot_rebuilt ? "true" : "false");
   message += " p02_sequences=" + IntegerToString(report.hook_phase02_report.sequences_total);
   message += " p03_records=" + IntegerToString(report.hook_phase03_report.records_total);
   message += " p04_closed=" + IntegerToString(report.hook_phase04_report.x_closed_count);
   message += " funnel={" + FP_NDSHook864CycleR1FunnelSummary(report.trade_report.funnel) + "}";
   message += " position_fast_path=" + (report.hook_snapshot_skipped_for_open_position ? "true" : "false");
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
