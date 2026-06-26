#ifndef __DAL_IMD_JOURNAL_MQH__
#define __DAL_IMD_JOURNAL_MQH__
#property strict
#include <IntermarketDivergence/DAL_IMDTypes.mqh>

string IMD_CsvEscape(const string s)
{
   string r = s;
   StringReplace(r, "\"", "\"\"");
   if(StringFind(r, ",") >= 0 || StringFind(r, "\"") >= 0)
      r = "\"" + r + "\"";
   return r;
}

void IMD_WriteEventsCsv(const string file_name, const IMD_Event &events[])
{
   int h = FileOpen(file_name, FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("IMD: failed to write events CSV ", file_name, " err=", GetLastError());
      return;
   }
   FileWrite(h,
             "event_id","pair_label","origin_symbol","destination_symbol","bar_index",
             "evaluation_time","valid_from_time","valid_until_time","divergence_side","suggested_bias",
             "level_family","trigger_mode","step_every_bars","step_offset_bars","destination_lag_bars","signal_valid_bars",
             "origin_ref_price","destination_ref_price","origin_ref_time","destination_ref_time","origin_ref_index","destination_ref_index",
             "origin_break_points","destination_break_points","divergence_gap_points","destination_late_confirmed","destination_confirm_time",
             "entry_close","mfe_points","mae_points","return_points","bars_to_mfe","bars_to_mae","note");
   for(int i=0; i<ArraySize(events); i++)
   {
      const IMD_Event e = events[i];
      FileWrite(h,
                e.id,e.pair_label,e.origin_symbol,e.destination_symbol,e.bar_index,
                TimeToString(e.evaluation_time, TIME_DATE|TIME_MINUTES),
                TimeToString(e.valid_from_time, TIME_DATE|TIME_MINUTES),
                TimeToString(e.valid_until_time, TIME_DATE|TIME_MINUTES),
                IMD_SideText(e.side),IMD_BiasText(e.suggested_bias),
                IMD_LevelFamilyText(e.level_family),IMD_TriggerModeText(e.trigger_mode),
                e.step_every_bars,e.step_offset_bars,e.destination_lag_bars,e.signal_valid_bars,
                DoubleToString(e.origin_ref_price, _Digits),DoubleToString(e.destination_ref_price, _Digits),
                TimeToString(e.origin_ref_time, TIME_DATE|TIME_MINUTES),
                TimeToString(e.destination_ref_time, TIME_DATE|TIME_MINUTES),
                e.origin_ref_index,e.destination_ref_index,
                DoubleToString(e.origin_break_points, _Digits),DoubleToString(e.destination_break_points, _Digits),DoubleToString(e.divergence_gap_points, _Digits),
                IMD_BoolText(e.destination_late_confirmed),TimeToString(e.destination_confirm_time, TIME_DATE|TIME_MINUTES),
                DoubleToString(e.entry_close, _Digits),DoubleToString(e.mfe_points, _Digits),DoubleToString(e.mae_points, _Digits),DoubleToString(e.return_points, _Digits),
                e.bars_to_mfe,e.bars_to_mae,e.note);
   }
   FileClose(h);
}

void IMD_WriteSummaryCsv(const string file_name,
                         const string run_id,
                         const string symbol_a,
                         const string symbol_b,
                         const int aligned_bars,
                         const IMD_Event &events[])
{
   int high=0, low=0, buy=0, sell=0, late=0;
   for(int i=0; i<ArraySize(events); i++)
   {
      if(events[i].side == IMD_DIV_HIGH) high++; else low++;
      if(events[i].suggested_bias == IMD_BIAS_BUY) buy++;
      if(events[i].suggested_bias == IMD_BIAS_SELL) sell++;
      if(events[i].destination_late_confirmed) late++;
   }
   int h = FileOpen(file_name, FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("IMD: failed to write summary CSV ", file_name, " err=", GetLastError());
      return;
   }
   FileWrite(h,"run_id","symbol_a","symbol_b","aligned_bars","events","high_divergences","low_divergences","buy_bias","sell_bias","late_destination_confirms");
   FileWrite(h,run_id,symbol_a,symbol_b,aligned_bars,ArraySize(events),high,low,buy,sell,late);
   FileClose(h);
}

#endif
