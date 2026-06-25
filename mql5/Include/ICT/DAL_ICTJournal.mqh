#ifndef __DAL_ICT_JOURNAL_MQH__
#define __DAL_ICT_JOURNAL_MQH__

#include <ICT/DAL_ICTTypes.mqh>

void DAL_ICT_EnsureFolder(const string folder, const bool common_files)
{
   if(folder == "")
      return;
   if(common_files)
      FolderCreate(folder, FILE_COMMON);
   else
      FolderCreate(folder);
}

bool DAL_ICT_WriteEntrySignalsCsv(
   const string file_name,
   const bool common_files,
   const DAL_ICTEntrySignal &signals[],
   const int signals_count,
   const string run_id,
   const string sweep_mode,
   const string target_mode
)
{
   int flags = FILE_WRITE | FILE_CSV | FILE_ANSI | FILE_SHARE_READ;
   if(common_files)
      flags |= FILE_COMMON;

   int handle = FileOpen(file_name, flags, ',');
   if(handle == INVALID_HANDLE)
   {
      Print("DAL ICT: failed to open signal CSV: ", file_name, " err=", GetLastError());
      return false;
   }

   FileWrite(handle,
      "run_id",
      "symbol",
      "timeframe",
      "L",
      "sweep_mode",
      "target_mode",
      "signal_id",
      "side",
      "valid_from_sweep_time",
      "valid_until_next_sweep_time",
      "valid_until_exclusive_time",
      "entry_time",
      "entry_price",
      "sl_price",
      "target_price",
      "rr",
      "risk_points",
      "reward_points",
      "exit_time",
      "exit_reason",
      "exit_price",
      "pnl_r",
      "bars_to_exit",
      "sweep_id",
      "sweep_time",
      "next_sweep_time",
      "fvg_id",
      "fvg_time",
      "fvg_low",
      "fvg_high",
      "ifvg_time",
      "cisd_time",
      "leg_start_time",
      "leg_start_open",
      "target_node_id",
      "target_node_time",
      "target_node_price"
   );

   for(int i=0; i<signals_count; i++)
   {
      FileWrite(handle,
         run_id,
         signals[i].symbol,
         EnumToString(signals[i].timeframe),
         signals[i].L,
         sweep_mode,
         target_mode,
         signals[i].id,
         DAL_ICT_DirectionToString(signals[i].direction),
         DAL_ICT_TimeStr(signals[i].valid_from_time),
         DAL_ICT_TimeStr(signals[i].valid_until_time),
         DAL_ICT_TimeStr(signals[i].valid_until_exclusive_time),
         DAL_ICT_TimeStr(signals[i].entry_time),
         DoubleToString(signals[i].entry_price, _Digits),
         DoubleToString(signals[i].sl_price, _Digits),
         DoubleToString(signals[i].target_price, _Digits),
         DoubleToString(signals[i].rr, 4),
         DoubleToString(signals[i].risk_points, 2),
         DoubleToString(signals[i].reward_points, 2),
         DAL_ICT_TimeStr(signals[i].exit_time),
         DAL_ICT_ExitReasonToString(signals[i].exit_reason),
         DoubleToString(signals[i].exit_price, _Digits),
         DoubleToString(signals[i].pnl_r, 4),
         signals[i].bars_to_exit,
         signals[i].sweep_id,
         DAL_ICT_TimeStr(signals[i].sweep_time),
         DAL_ICT_TimeStr(signals[i].next_sweep_time),
         signals[i].fvg_id,
         DAL_ICT_TimeStr(signals[i].fvg_time),
         DoubleToString(signals[i].fvg_low, _Digits),
         DoubleToString(signals[i].fvg_high, _Digits),
         DAL_ICT_TimeStr(signals[i].ifvg_time),
         DAL_ICT_TimeStr(signals[i].cisd_time),
         DAL_ICT_TimeStr(signals[i].leg_start_time),
         DoubleToString(signals[i].leg_start_open, _Digits),
         signals[i].target_node_id,
         DAL_ICT_TimeStr(signals[i].target_node_time),
         DoubleToString(signals[i].target_node_price, _Digits)
      );
   }

   FileClose(handle);
   return true;
}

bool DAL_ICT_WriteSummaryCsv(
   const string file_name,
   const bool common_files,
   const string run_id,
   const string symbol,
   const ENUM_TIMEFRAMES timeframe,
   const int bars_count,
   const int nodes_count,
   const int sweeps_count,
   const int fvgs_count,
   const int signals_count,
   const DAL_ICTEntrySignal &signals[]
)
{
   int flags = FILE_WRITE | FILE_CSV | FILE_ANSI | FILE_SHARE_READ;
   if(common_files)
      flags |= FILE_COMMON;

   int handle = FileOpen(file_name, flags, ',');
   if(handle == INVALID_HANDLE)
   {
      Print("DAL ICT: failed to open summary CSV: ", file_name, " err=", GetLastError());
      return false;
   }

   int buys = 0, sells = 0, tp = 0, sl = 0, next_sweep = 0, csv_end = 0;
   double sum_r = 0.0;
   for(int i=0; i<signals_count; i++)
   {
      if(signals[i].direction == ICT_DIR_BUY) buys++;
      if(signals[i].direction == ICT_DIR_SELL) sells++;
      if(signals[i].exit_reason == ICT_EXIT_TP) tp++;
      if(signals[i].exit_reason == ICT_EXIT_SL) sl++;
      if(signals[i].exit_reason == ICT_EXIT_NEXT_SWEEP) next_sweep++;
      if(signals[i].exit_reason == ICT_EXIT_CSV_END) csv_end++;
      sum_r += signals[i].pnl_r;
   }

   FileWrite(handle, "metric", "value");
   FileWrite(handle, "run_id", run_id);
   FileWrite(handle, "symbol", symbol);
   FileWrite(handle, "timeframe", EnumToString(timeframe));
   FileWrite(handle, "bars", bars_count);
   FileWrite(handle, "nodes", nodes_count);
   FileWrite(handle, "sweeps", sweeps_count);
   FileWrite(handle, "fvgs", fvgs_count);
   FileWrite(handle, "entry_signals", signals_count);
   FileWrite(handle, "buy_signals", buys);
   FileWrite(handle, "sell_signals", sells);
   FileWrite(handle, "tp_exits", tp);
   FileWrite(handle, "sl_exits", sl);
   FileWrite(handle, "next_sweep_exits", next_sweep);
   FileWrite(handle, "csv_end_exits", csv_end);
   FileWrite(handle, "sum_r", DoubleToString(sum_r, 4));
   FileWrite(handle, "avg_r", signals_count > 0 ? DoubleToString(sum_r / signals_count, 4) : "0.0000");

   FileClose(handle);
   return true;
}

#endif
