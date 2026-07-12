#ifndef __FP_NDS_F2_WAIST_BACKTEST_TYPES_MQH__
#define __FP_NDS_F2_WAIST_BACKTEST_TYPES_MQH__
#property strict

#include "FP_NDSBacktestTypes.mqh"
#include "FP_NDSF2WaistTradeTypes.mqh"

#define FP_NDS_F2_WAIST_BACKTEST_VERSION "NDS-F2-BACKTEST-01"

struct FP_NDSF2WaistBacktestReport
{
   bool ok;
   string status;
   string reason;
   int copied_bars;
   int scale_count;
   int event_count;
   int hook_count;
   bool detector_skipped_for_exposure;
   ulong elapsed_microseconds;
   FP_NDSF2WaistTradeReport trade_report;
};

struct FP_NDSF2WaistBacktestStats
{
   ulong runs;
   ulong successful_runs;
   ulong failed_runs;
   ulong detector_runs;
   ulong exposure_fast_paths;
   ulong total_microseconds;
   ulong max_microseconds;
   ulong last_microseconds;
};

void FP_ResetNDSF2WaistBacktestReport(FP_NDSF2WaistBacktestReport &r)
{
   r.ok = false;
   r.status = "RESET";
   r.reason = "reset";
   r.copied_bars = 0;
   r.scale_count = 0;
   r.event_count = 0;
   r.hook_count = 0;
   r.detector_skipped_for_exposure = false;
   r.elapsed_microseconds = 0;
   FP_ResetNDSF2WaistTradeReport(r.trade_report);
}

void FP_ResetNDSF2WaistBacktestStats(FP_NDSF2WaistBacktestStats &s)
{
   s.runs = 0;
   s.successful_runs = 0;
   s.failed_runs = 0;
   s.detector_runs = 0;
   s.exposure_fast_paths = 0;
   s.total_microseconds = 0;
   s.max_microseconds = 0;
   s.last_microseconds = 0;
}

#endif // __FP_NDS_F2_WAIST_BACKTEST_TYPES_MQH__
