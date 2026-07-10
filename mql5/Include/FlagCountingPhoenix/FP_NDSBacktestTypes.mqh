#ifndef __FP_NDS_BACKTEST_TYPES_MQH__
#define __FP_NDS_BACKTEST_TYPES_MQH__
#property strict

#include "FP_NDSHookTradeTypes.mqh"
#include "FP_HookPhase02Types.mqh"

#define FP_NDS_BACKTEST_VERSION "NDS-BACKTEST-01"
#define FP_NDS_BACKTEST_SCHEMA_VERSION "nds_lightweight_backtest_v1"

enum FP_NDSBacktestProfile
{
   FP_NDS_BACKTEST_PROFILE_FAST = 0,
   FP_NDS_BACKTEST_PROFILE_PARITY = 1,
   FP_NDS_BACKTEST_PROFILE_CUSTOM = 2
};

struct FP_NDSBacktestRuntimeConfig
{
   FP_NDSBacktestProfile profile;

   int requested_bars;
   int min_closed_bars;
   bool use_closed_bars_only;
   bool strict_timebase;

   bool use_multi_scale;
   int scale_l1;
   int scale_l2;
   int scale_l3;
   int scale_l4;
   int scale_l5;
   int scale_l6;
   int scale_l7;
   int scale_l8;

   int max_events;
   int max_hooks;
   int hook_scan_bars;

   bool run_on_first_tick;
   bool skip_hook_rebuild_while_position_open;
   bool print_run_summary;
   int print_every_n_runs;
};

struct FP_NDSBacktestRunReport
{
   datetime generated_at;
   string version;
   string schema_version;
   string symbol;
   ENUM_TIMEFRAMES period;

   bool attempted;
   bool ok;
   string status;
   string reason;

   int copied_bars;
   int scale_count;
   int event_count;
   int hook_count;
   bool hook_snapshot_rebuilt;
   bool hook_snapshot_skipped_for_open_position;

   ulong elapsed_microseconds;
   FP_HookPhase02Report hook_phase02_report;
   FP_NDSHookTradeReport trade_report;
};

struct FP_NDSBacktestSessionStats
{
   ulong runs;
   ulong successful_runs;
   ulong failed_runs;
   ulong hook_rebuild_runs;
   ulong position_fast_path_runs;
   ulong total_microseconds;
   ulong max_microseconds;
   ulong last_microseconds;
   datetime first_run_time;
   datetime last_run_time;
};

void FP_ResetNDSBacktestRuntimeConfig(FP_NDSBacktestRuntimeConfig &cfg)
{
   cfg.profile = FP_NDS_BACKTEST_PROFILE_FAST;
   cfg.requested_bars = 1200;
   cfg.min_closed_bars = 200;
   cfg.use_closed_bars_only = true;
   cfg.strict_timebase = true;

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
   cfg.hook_scan_bars = 1200;

   cfg.run_on_first_tick = true;
   cfg.skip_hook_rebuild_while_position_open = true;
   cfg.print_run_summary = false;
   cfg.print_every_n_runs = 250;
}

void FP_ResetNDSBacktestRunReport(FP_NDSBacktestRunReport &report)
{
   report.generated_at = TimeCurrent();
   report.version = FP_NDS_BACKTEST_VERSION;
   report.schema_version = FP_NDS_BACKTEST_SCHEMA_VERSION;
   report.symbol = "";
   report.period = PERIOD_CURRENT;
   report.attempted = false;
   report.ok = false;
   report.status = "RESET";
   report.reason = "reset";
   report.copied_bars = 0;
   report.scale_count = 0;
   report.event_count = 0;
   report.hook_count = 0;
   report.hook_snapshot_rebuilt = false;
   report.hook_snapshot_skipped_for_open_position = false;
   report.elapsed_microseconds = 0;
   FP_ResetHookPhase02Report(report.hook_phase02_report);
   FP_ResetNDSHookTradeReport(report.trade_report);
}

void FP_ResetNDSBacktestSessionStats(FP_NDSBacktestSessionStats &stats)
{
   stats.runs = 0;
   stats.successful_runs = 0;
   stats.failed_runs = 0;
   stats.hook_rebuild_runs = 0;
   stats.position_fast_path_runs = 0;
   stats.total_microseconds = 0;
   stats.max_microseconds = 0;
   stats.last_microseconds = 0;
   stats.first_run_time = 0;
   stats.last_run_time = 0;
}

string FP_NDSBacktestProfileName(const FP_NDSBacktestProfile profile)
{
   if(profile == FP_NDS_BACKTEST_PROFILE_FAST) return "FAST";
   if(profile == FP_NDS_BACKTEST_PROFILE_PARITY) return "PARITY";
   if(profile == FP_NDS_BACKTEST_PROFILE_CUSTOM) return "CUSTOM";
   return "UNKNOWN";
}

#endif // __FP_NDS_BACKTEST_TYPES_MQH__
