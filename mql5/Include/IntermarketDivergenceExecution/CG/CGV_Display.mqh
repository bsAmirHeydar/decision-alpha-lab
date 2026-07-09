#ifndef __CGV_DISPLAY_MQH__
#define __CGV_DISPLAY_MQH__

#include <IntermarketDivergenceExecution/CG/CGV_Ledger.mqh>

class CCGV_Display
{
private:
   string BoolText(const bool v) { return v ? "yes" : "no"; }

   string DirectionText(SCGCFinalSignal &signal)
   {
      if(signal.direction==CGC_DIRECTION_BUY) return "BUY";
      if(signal.direction==CGC_DIRECTION_SELL) return "SELL";
      return "NONE";
   }

   string StatusText(SCGCFinalSignal &signal)
   {
      if(signal.status==CGC_STATUS_CONFIRMED_TRADEABLE) return "CONFIRMED";
      if(signal.status==CGC_STATUS_INVALIDATED_DOUBLE_HUNT) return "INVALIDATED";
      if(signal.status==CGC_STATUS_MISSING_DATA) return "MISSING";
      return "NONE";
   }

   string AnchorTimeText(const ECGVAnchorTimeMode mode)
   {
      if(mode==CGV_ANCHOR_TIME_REFERENCE_CYCLE_START) return "ref_start";
      if(mode==CGV_ANCHOR_TIME_REFERENCE_CYCLE_MIDDLE) return "ref_mid";
      if(mode==CGV_ANCHOR_TIME_REFERENCE_CYCLE_END) return "ref_end";
      if(mode==CGV_ANCHOR_TIME_EXACT_REFERENCE_EXTREME) return "exact_ref_extreme";
      if(mode==CGV_ANCHOR_TIME_CURRENT_CYCLE_START) return "current_start";
      if(mode==CGV_ANCHOR_TIME_CURRENT_CYCLE_END) return "current_end";
      if(mode==CGV_ANCHOR_TIME_EXACT_CURRENT_EXTREME) return "exact_current_extreme";
      if(mode==CGV_ANCHOR_TIME_CONFIRMATION_CLOSE) return "confirmation_close";
      return "unknown";
   }

public:
   string BuildHeader(SCGTTimeSnapshot &time_snapshot,SCGVVisualLedgerConfig &config,const datetime live_broker_now)
   {
      string text="";
      text += "EXP0017 Phase 06 - Dual-Symbol Full Visual Language & Signal Audit Ledger\n";
      text += "No order | No risk | No target | No outcome study | Drawing + raw ledger only\n";
      text += StringFormat("Symbols: %s / %s | chart: %s | TF: %s | closed-boundary: %s\n",config.symbol_a,config.symbol_b,_Symbol,EnumToString(config.confirmation_timeframe),BoolText(config.use_last_closed_candle_boundary));
      text += StringFormat("Drawing: %s | dual-symbol charts: %s | open missing charts: %s | comments/panel: manual input\n",BoolText(config.enable_drawing),BoolText(config.draw_on_both_input_symbol_charts),BoolText(config.open_missing_input_symbol_charts));
      text += StringFormat("Visual ON: main=%s origin=%s dest=%s originV=%s destV=%s confirmV=%s refAnchor=%s labels=%s\n",
                           BoolText(config.draw_divergence_origin_destination_line),BoolText(config.draw_origin_marker),BoolText(config.draw_destination_marker),BoolText(config.draw_origin_vertical),BoolText(config.draw_destination_vertical),BoolText(config.draw_confirmation_marker),BoolText(config.draw_reference_cycle_anchor),BoolText(config.draw_text_label));
      text += StringFormat("Guides ON: hunterRef=%s hunterExt=%s cleanRef=%s cleanStop=%s cleanLine=%s | ledger=%s file=%s\n",
                           BoolText(config.draw_hunter_reference_guide),BoolText(config.draw_hunter_current_extreme_guide),BoolText(config.draw_clean_reference_guide),BoolText(config.draw_clean_stop_reference_guide),BoolText(config.draw_clean_comparison_line),BoolText(config.enable_ledger),config.ledger_file_name);
      text += StringFormat("Visual anchors: origin_time=%s | destination_time=%s\n",AnchorTimeText(config.divergence_origin_time_mode),AnchorTimeText(config.divergence_destination_time_mode));
      text += StringFormat("Live broker: %s | Observation broker: %s | UTC: %s | NY: %s | NY offset: %d\n",
                           TimeToString(live_broker_now,TIME_DATE|TIME_SECONDS),TimeToString(time_snapshot.broker_now,TIME_DATE|TIME_SECONDS),TimeToString(time_snapshot.utc_now,TIME_DATE|TIME_SECONDS),TimeToString(time_snapshot.new_york_now,TIME_DATE|TIME_SECONDS),time_snapshot.new_york_utc_offset_hours);
      text += StringFormat("Trading day: %s -> %s | inside: %s | elapsed: %d / %d min\n",
                           TimeToString(time_snapshot.trading_day_start_ny,TIME_DATE|TIME_MINUTES),TimeToString(time_snapshot.trading_day_end_ny,TIME_DATE|TIME_MINUTES),BoolText(time_snapshot.inside_trading_day),time_snapshot.elapsed_minutes_from_day_start,CGT_TRADING_DAY_MINUTES);
      return text;
   }

   string BuildGroupLine(SCGVGroupVisualLedgerState &state)
   {
      return StringFormat("%s | current #%d %s-%s NY | prev=%d | final=%d confirmed=%d invalidated=%d | drawn=%d skipped=%d | ledger=%d dup=%d | BUY=%d SELL=%d\n",
                          state.group_name,state.current_cycle_number,TimeToString(state.current_cycle_start_ny,TIME_MINUTES),TimeToString(state.current_cycle_end_ny-60,TIME_MINUTES),state.previous_cycle_count,state.final_state_count,state.confirmed_count,state.invalidated_count,state.drawn_count,state.skipped_draw_count,state.ledger_written_count,state.ledger_duplicate_count,state.buy_count,state.sell_count);
   }

   string BuildSignalLine(SCGCFinalSignal &signal)
   {
      return StringFormat("  %s %s | %s | ref #%d -> current #%d | hunter=%s clean=%s | confirm=%s | Aref=%s Aext=%s Bref=%s Bext=%s | Href=%s Hext=%s Cref=%s Cext=%s stop=%s\n",
                          StatusText(signal),DirectionText(signal),signal.group_name,signal.reference_cycle_number,signal.current_cycle_number,signal.hunter_symbol,signal.clean_symbol,TimeToString(signal.confirmation_time_ny,TIME_DATE|TIME_MINUTES),
                          DoubleToString(signal.symbol_a_reference_price,CGC_PRICE_DIGITS),DoubleToString(signal.symbol_a_current_extreme,CGC_PRICE_DIGITS),DoubleToString(signal.symbol_b_reference_price,CGC_PRICE_DIGITS),DoubleToString(signal.symbol_b_current_extreme,CGC_PRICE_DIGITS),
                          DoubleToString(signal.hunter_reference_price,CGC_PRICE_DIGITS),DoubleToString(signal.hunter_current_extreme,CGC_PRICE_DIGITS),DoubleToString(signal.clean_reference_price,CGC_PRICE_DIGITS),DoubleToString(signal.clean_current_extreme,CGC_PRICE_DIGITS),DoubleToString(signal.clean_stop_reference_price,CGC_PRICE_DIGITS));
   }

   string BuildPanel(SCGTTimeSnapshot &time_snapshot,SCGVVisualLedgerConfig &config,SCGVGroupVisualLedgerState &visual_states[],SCGCFinalSignal &flat_signals[],int &group_start[],int &group_count[],const datetime live_broker_now)
   {
      string text=BuildHeader(time_snapshot,config,live_broker_now);
      int groups_shown=0;
      for(int i=0;i<ArraySize(visual_states);i++)
      {
         if(groups_shown>=config.max_groups_shown)
            break;
         if(config.show_only_groups_with_final_states && visual_states[i].final_state_count<=0)
            continue;
         text += BuildGroupLine(visual_states[i]);
         int shown=0;
         for(int s=group_start[i];s<group_start[i]+group_count[i] && s<ArraySize(flat_signals);s++)
         {
            if(shown>=config.max_signals_per_group_shown)
               break;
            text += BuildSignalLine(flat_signals[s]);
            shown++;
         }
         groups_shown++;
      }
      return text;
   }

   string BuildPrintSummary(SCGTTimeSnapshot &time_snapshot,SCGVGroupVisualLedgerState &visual_states[])
   {
      int final_count=0;
      int drawn=0;
      int written=0;
      int duplicates=0;
      for(int i=0;i<ArraySize(visual_states);i++)
      {
         final_count+=visual_states[i].final_state_count;
         drawn+=visual_states[i].drawn_count;
         written+=visual_states[i].ledger_written_count;
         duplicates+=visual_states[i].ledger_duplicate_count;
      }
      return StringFormat("EXP0017 Phase06 dual-symbol visual audit | NY=%s | final=%d | drawn=%d | ledger_written=%d | ledger_duplicates=%d",TimeToString(time_snapshot.new_york_now,TIME_DATE|TIME_MINUTES),final_count,drawn,written,duplicates);
   }
};

#endif
