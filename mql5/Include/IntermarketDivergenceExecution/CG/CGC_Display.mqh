#ifndef __CGC_DISPLAY_MQH__
#define __CGC_DISPLAY_MQH__

#include <IntermarketDivergenceExecution/CG/CGC_ConfirmationField.mqh>

class CCGC_Display
{
private:
   string BoolText(const bool v)
   {
      return v ? "yes" : "no";
   }

public:
   string BuildHeader(SCGTTimeSnapshot &time_snapshot,SCGCConfirmationConfig &config,const datetime live_broker_now)
   {
      string text="";
      text += "EXP0017 Phase 05 - Confirmation & Invalidation Anatomy\n";
      text += "No order | No risk | No target | Final closed-candle signal states only\n";
      text += StringFormat("Symbols: %s / %s | TF: %s | closed-boundary: %s\n",config.symbol_a,config.symbol_b,EnumToString(config.confirmation_timeframe),BoolText(config.use_last_closed_candle_boundary));
      text += StringFormat("Live broker: %s | Observation broker: %s | UTC: %s | NY: %s | NY offset: %d\n",
                           TimeToString(live_broker_now,TIME_DATE|TIME_SECONDS),
                           TimeToString(time_snapshot.broker_now,TIME_DATE|TIME_SECONDS),
                           TimeToString(time_snapshot.utc_now,TIME_DATE|TIME_SECONDS),
                           TimeToString(time_snapshot.new_york_now,TIME_DATE|TIME_SECONDS),
                           time_snapshot.new_york_utc_offset_hours);
      text += StringFormat("Trading day: %s -> %s | inside: %s | elapsed: %d / %d min\n",
                           TimeToString(time_snapshot.trading_day_start_ny,TIME_DATE|TIME_MINUTES),
                           TimeToString(time_snapshot.trading_day_end_ny,TIME_DATE|TIME_MINUTES),
                           BoolText(time_snapshot.inside_trading_day),
                           time_snapshot.elapsed_minutes_from_day_start,
                           CGT_TRADING_DAY_MINUTES);
      return text;
   }

   string BuildGroupLine(SCGCGroupConfirmationState &state)
   {
      string text=StringFormat("%s | current #%d %s-%s NY | refs ready=%d missing=%d | final=%d confirmed=%d invalidated=%d | BUY=%d SELL=%d | cleanA=%d cleanB=%d",
                               state.group_name,
                               state.current_cycle_number,
                               TimeToString(state.current_cycle_start_ny,TIME_MINUTES),
                               TimeToString(state.current_cycle_end_ny-60,TIME_MINUTES),
                               state.ready_reference_count,
                               state.missing_reference_count,
                               state.final_state_count,
                               state.confirmed_tradeable_count,
                               state.invalidated_double_hunt_count,
                               state.buy_confirmed_count,
                               state.sell_confirmed_count,
                               state.symbol_a_clean_count,
                               state.symbol_b_clean_count);
      text += "\n";
      return text;
   }

   string BuildSignalLine(SCGCFinalSignal &signal,SCGCConfirmationConfig &config,CCGC_ConfirmationField &field)
   {
      string text=StringFormat("  %s %s %s | ref #%d %s | hunter=%s clean=%s | confirm=%s",
                               field.StatusTextPublic(signal.status),
                               field.DirectionTextPublic(signal.direction),
                               field.SideTextPublic(signal.side),
                               signal.reference_cycle_number,
                               field.FormatCycleRangeNY(signal.reference_cycle_start_ny,signal.reference_cycle_end_ny),
                               signal.hunter_symbol,
                               signal.clean_symbol,
                               TimeToString(signal.confirmation_time_ny,TIME_DATE|TIME_MINUTES));
      if(config.show_stop_reference_preview)
         text += StringFormat(" | stop-ref=%s",field.FormatPrice(signal.clean_stop_reference_price));
      if(config.show_prices)
      {
         text += StringFormat(" | hunter ref/ext %s/%s | clean ref/ext %s/%s",
                              field.FormatPrice(signal.hunter_reference_price),
                              field.FormatPrice(signal.hunter_current_extreme),
                              field.FormatPrice(signal.clean_reference_price),
                              field.FormatPrice(signal.clean_current_extreme));
      }
      text += "\n";
      return text;
   }

   string BuildPanel(SCGTTimeSnapshot &time_snapshot,SCGCConfirmationConfig &config,SCGCGroupConfirmationState &states[],SCGCFinalSignal &flat_signals[],int &group_start[],int &group_count[],CCGC_ConfirmationField &field,const datetime live_broker_now)
   {
      string text=BuildHeader(time_snapshot,config,live_broker_now);
      int shown_groups=0;
      int state_count=ArraySize(states);
      for(int g=0;g<state_count;g++)
      {
         if(config.show_only_groups_with_final_states && !states[g].has_any_final_state)
            continue;
         if(shown_groups>=config.max_groups_shown)
         {
            text += StringFormat("... %d more enabled groups hidden by display limit\n",state_count-g);
            break;
         }
         text += BuildGroupLine(states[g]);
         shown_groups++;

         int start=group_start[g];
         int count=group_count[g];
         int shown=0;
         for(int i=count-1;i>=0;i--)
         {
            if(shown>=config.max_signals_per_group_shown)
               break;
            int idx=start+i;
            if(idx<0 || idx>=ArraySize(flat_signals))
               continue;
            text += BuildSignalLine(flat_signals[idx],config,field);
            shown++;
         }
      }
      return text;
   }

   string BuildPrintSummary(SCGTTimeSnapshot &time_snapshot,SCGCGroupConfirmationState &states[])
   {
      string text=StringFormat("EXP0017 Phase05 ConfirmationAnatomy | NY=%s | groups=%d",
                               TimeToString(time_snapshot.new_york_now,TIME_DATE|TIME_MINUTES),ArraySize(states));
      for(int i=0;i<ArraySize(states);i++)
      {
         text += StringFormat(" | %s confirmed=%d invalidated=%d buy=%d sell=%d",
                              states[i].group_name,
                              states[i].confirmed_tradeable_count,
                              states[i].invalidated_double_hunt_count,
                              states[i].buy_confirmed_count,
                              states[i].sell_confirmed_count);
      }
      return text;
   }
};

#endif
