#ifndef __DAL_IMD_JOURNAL_MQH__
#define __DAL_IMD_JOURNAL_MQH__

#include <IntermarketDivergence/DAL_IMDTypes.mqh>

void DAL_IMD_EnsureFolder(const string folder, const bool common_files)
{
   if(folder == "") return;
   if(common_files)
      FolderCreate(folder, FILE_COMMON);
   else
      FolderCreate(folder);
}

bool DAL_IMD_WriteEventsCsv(
   const string file_name,
   const bool common_files,
   const string run_id,
   const DAL_IMDDivergenceEvent &events[],
   const int events_count
)
{
   int flags = FILE_WRITE | FILE_CSV | FILE_ANSI | FILE_SHARE_READ;
   if(common_files) flags |= FILE_COMMON;
   int handle = FileOpen(file_name, flags, ',');
   if(handle == INVALID_HANDLE)
   {
      Print("DAL IMD: failed to open events CSV: ", file_name, " err=", GetLastError());
      return false;
   }

   FileWrite(handle,
      "run_id",
      "event_id",
      "pair_label",
      "origin_symbol",
      "destination_symbol",
      "timeframe",
      "step_every_bars",
      "step_offset_bars",
      "bar_index",
      "evaluation_time",
      "valid_from_time",
      "valid_until_time",
      "valid_until_exclusive_time",
      "window_end_reason",
      "divergence_side",
      "suggested_bias",
      "origin_level_source",
      "destination_level_source",
      "trigger_mode",
      "destination_lag_bars",
      "signal_valid_bars",
      "origin_ref_price",
      "destination_ref_price",
      "origin_ref_time",
      "destination_ref_time",
      "origin_ref_index",
      "destination_ref_index",
      "origin_node_id",
      "destination_node_id",
      "origin_open",
      "origin_high",
      "origin_low",
      "origin_close",
      "destination_open",
      "destination_high",
      "destination_low",
      "destination_close",
      "origin_break_points",
      "destination_break_points",
      "divergence_gap_points",
      "normalized_gap_ratio",
      "destination_confirm_time",
      "note"
   );

   for(int i=0; i<events_count; i++)
   {
      FileWrite(handle,
         run_id,
         events[i].id,
         events[i].pair_label,
         events[i].origin_symbol,
         events[i].destination_symbol,
         EnumToString(events[i].timeframe),
         events[i].step_every_bars,
         events[i].step_offset_bars,
         events[i].index,
         DAL_IMD_TimeStr(events[i].evaluation_time),
         DAL_IMD_TimeStr(events[i].valid_from_time),
         DAL_IMD_TimeStr(events[i].valid_until_time),
         DAL_IMD_TimeStr(events[i].valid_until_exclusive_time),
         DAL_IMD_WindowEndReasonToString(events[i].window_end_reason),
         DAL_IMD_DivergenceSideToString(events[i].divergence_side),
         DAL_IMD_BiasToString(events[i].suggested_bias),
         DAL_IMD_LevelSourceToString(events[i].origin_level_source),
         DAL_IMD_LevelSourceToString(events[i].destination_level_source),
         DAL_IMD_TriggerModeToString(events[i].trigger_mode),
         events[i].destination_lag_bars,
         events[i].signal_valid_bars,
         DoubleToString(events[i].origin_ref_price, 8),
         DoubleToString(events[i].destination_ref_price, 8),
         DAL_IMD_TimeStr(events[i].origin_ref_time),
         DAL_IMD_TimeStr(events[i].destination_ref_time),
         events[i].origin_ref_index,
         events[i].destination_ref_index,
         events[i].origin_node_id,
         events[i].destination_node_id,
         DoubleToString(events[i].origin_open, 8),
         DoubleToString(events[i].origin_high, 8),
         DoubleToString(events[i].origin_low, 8),
         DoubleToString(events[i].origin_close, 8),
         DoubleToString(events[i].destination_open, 8),
         DoubleToString(events[i].destination_high, 8),
         DoubleToString(events[i].destination_low, 8),
         DoubleToString(events[i].destination_close, 8),
         DoubleToString(events[i].origin_break_points, 4),
         DoubleToString(events[i].destination_break_points, 4),
         DoubleToString(events[i].divergence_gap_points, 4),
         DoubleToString(events[i].normalized_gap_ratio, 6),
         DAL_IMD_TimeStr(events[i].destination_confirm_time),
         events[i].note
      );
   }

   FileClose(handle);
   return true;
}

bool DAL_IMD_WriteStepsCsv(
   const string file_name,
   const bool common_files,
   const string run_id,
   const DAL_IMDEvaluatedStep &steps[],
   const int steps_count
)
{
   int flags = FILE_WRITE | FILE_CSV | FILE_ANSI | FILE_SHARE_READ;
   if(common_files) flags |= FILE_COMMON;
   int handle = FileOpen(file_name, flags, ',');
   if(handle == INVALID_HANDLE)
   {
      Print("DAL IMD: failed to open steps CSV: ", file_name, " err=", GetLastError());
      return false;
   }

   FileWrite(handle,
      "run_id",
      "bar_index",
      "time",
      "origin_symbol",
      "destination_symbol",
      "side",
      "origin_triggered",
      "destination_triggered",
      "destination_triggered_in_lag",
      "origin_ref",
      "destination_ref",
      "origin_high",
      "origin_low",
      "destination_high",
      "destination_low"
   );

   for(int i=0; i<steps_count; i++)
   {
      FileWrite(handle,
         run_id,
         steps[i].index,
         DAL_IMD_TimeStr(steps[i].time),
         steps[i].origin_symbol,
         steps[i].destination_symbol,
         steps[i].side,
         DAL_BoolToString(steps[i].origin_triggered),
         DAL_BoolToString(steps[i].destination_triggered),
         DAL_BoolToString(steps[i].destination_triggered_in_lag),
         DoubleToString(steps[i].origin_ref, 8),
         DoubleToString(steps[i].destination_ref, 8),
         DoubleToString(steps[i].origin_high, 8),
         DoubleToString(steps[i].origin_low, 8),
         DoubleToString(steps[i].destination_high, 8),
         DoubleToString(steps[i].destination_low, 8)
      );
   }

   FileClose(handle);
   return true;
}

bool DAL_IMD_WriteSummaryCsv(
   const string file_name,
   const bool common_files,
   const string run_id,
   const string symbol_a,
   const string symbol_b,
   const ENUM_TIMEFRAMES timeframe,
   const int bars_count,
   const int nodes_a_count,
   const int nodes_b_count,
   const int events_count,
   const int steps_count,
   const DAL_IMDDivergenceEvent &events[]
)
{
   int flags = FILE_WRITE | FILE_CSV | FILE_ANSI | FILE_SHARE_READ;
   if(common_files) flags |= FILE_COMMON;
   int handle = FileOpen(file_name, flags, ',');
   if(handle == INVALID_HANDLE)
   {
      Print("DAL IMD: failed to open summary CSV: ", file_name, " err=", GetLastError());
      return false;
   }

   int high_divs=0, low_divs=0, buy_bias=0, sell_bias=0, a_origin=0, b_origin=0;
   int late_confirm=0, fixed_end=0, next_div=0;
   for(int i=0; i<events_count; i++)
   {
      if(events[i].divergence_side == IMD_DIV_HIGH) high_divs++;
      if(events[i].divergence_side == IMD_DIV_LOW) low_divs++;
      if(events[i].suggested_bias == IMD_BIAS_BUY) buy_bias++;
      if(events[i].suggested_bias == IMD_BIAS_SELL) sell_bias++;
      if(events[i].origin_symbol == symbol_a) a_origin++;
      if(events[i].origin_symbol == symbol_b) b_origin++;
      if(events[i].window_end_reason == IMD_WINDOW_DEST_LATE_CONFIRM) late_confirm++;
      if(events[i].window_end_reason == IMD_WINDOW_FIXED_END) fixed_end++;
      if(events[i].window_end_reason == IMD_WINDOW_NEXT_DIVERGENCE) next_div++;
   }

   FileWrite(handle, "metric", "value");
   FileWrite(handle, "run_id", run_id);
   FileWrite(handle, "symbol_a", symbol_a);
   FileWrite(handle, "symbol_b", symbol_b);
   FileWrite(handle, "timeframe", EnumToString(timeframe));
   FileWrite(handle, "aligned_bars", bars_count);
   FileWrite(handle, "nodes_a", nodes_a_count);
   FileWrite(handle, "nodes_b", nodes_b_count);
   FileWrite(handle, "evaluated_steps", steps_count);
   FileWrite(handle, "divergence_events", events_count);
   FileWrite(handle, "high_divergences", high_divs);
   FileWrite(handle, "low_divergences", low_divs);
   FileWrite(handle, "buy_bias_events", buy_bias);
   FileWrite(handle, "sell_bias_events", sell_bias);
   FileWrite(handle, "origin_a_events", a_origin);
   FileWrite(handle, "origin_b_events", b_origin);
   FileWrite(handle, "late_destination_confirm_end", late_confirm);
   FileWrite(handle, "fixed_window_end", fixed_end);
   FileWrite(handle, "next_divergence_end", next_div);
   FileClose(handle);
   return true;
}

#endif
