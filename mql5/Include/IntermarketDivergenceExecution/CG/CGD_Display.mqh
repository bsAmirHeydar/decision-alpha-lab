#ifndef __CGD_DISPLAY_MQH__
#define __CGD_DISPLAY_MQH__

#include <IntermarketDivergenceExecution/CG/CGD_DivergenceField.mqh>

class CCGD_Display
{
private:
   string BoolText(const bool v)
   {
      return v ? "yes" : "no";
   }

public:
   string BuildHeader(SCGTTimeSnapshot &time_snapshot,SCGDDivergenceConfig &config)
   {
      string text="";
      text += "EXP0017 Phase 04 - Divergence Anatomy\n";
      text += "No trade | No candle-close permission | No risk | No target | Raw divergence candidates only\n";
      text += StringFormat("Symbols: %s / %s\n",config.symbol_a,config.symbol_b);
      text += StringFormat("Broker: %s | UTC: %s | NY: %s | NY offset: %d\n",
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

   string BuildGroupLine(SCGDGroupDivergenceState &state,SCGDDivergenceConfig &config)
   {
      string text=StringFormat("%s | current #%d %s-%s NY | refs ready=%d missing=%d | raw hunts=%d | div=%d BUY=%d SELL=%d | clean A=%d clean B=%d",
                               state.group_name,
                               state.current_cycle_number,
                               TimeToString(state.current_cycle_start_ny,TIME_MINUTES),
                               TimeToString(state.current_cycle_end_ny-60,TIME_MINUTES),
                               state.ready_reference_count,
                               state.missing_reference_count,
                               state.raw_hunt_count,
                               state.candidate_count,
                               state.buy_candidate_count,
                               state.sell_candidate_count,
                               state.symbol_a_clean_count,
                               state.symbol_b_clean_count);
      if(config.show_symmetric_no_divergence_counts)
      {
         text += StringFormat(" | both-high no-div=%d both-low no-div=%d",
                              state.symmetric_high_no_divergence_count,
                              state.symmetric_low_no_divergence_count);
      }
      text += "\n";
      return text;
   }

   string BuildCandidateLine(SCGDDivergenceCandidate &candidate,SCGDDivergenceConfig &config,CCGD_DivergenceField &field)
   {
      string text=StringFormat("  %s %s | ref #%d %s | hunter=%s clean=%s | stop-ref=%s",
                               field.DirectionTextPublic(candidate.direction),
                               field.SideTextPublic(candidate.side),
                               candidate.reference_cycle_number,
                               field.FormatCycleRangeNY(candidate.reference_cycle_start_ny,candidate.reference_cycle_end_ny),
                               candidate.hunter_symbol,
                               candidate.clean_symbol,
                               field.FormatPrice(candidate.clean_stop_reference_price));
      if(config.show_prices)
      {
         text += StringFormat(" | hunter ref/ext %s/%s | clean ref/ext %s/%s",
                              field.FormatPrice(candidate.hunter_reference_price),
                              field.FormatPrice(candidate.hunter_current_extreme),
                              field.FormatPrice(candidate.clean_reference_price),
                              field.FormatPrice(candidate.clean_current_extreme));
      }
      text += "\n";
      return text;
   }

   string BuildPanel(SCGTTimeSnapshot &time_snapshot,SCGDDivergenceConfig &config,SCGDGroupDivergenceState &states[],SCGDDivergenceCandidate &flat_candidates[],int &group_start[],int &group_count[],CCGD_DivergenceField &field)
   {
      string text=BuildHeader(time_snapshot,config);
      int shown_groups=0;
      int state_count=ArraySize(states);
      for(int g=0;g<state_count;g++)
      {
         if(config.show_only_groups_with_divergence && !states[g].has_any_candidate)
            continue;
         if(shown_groups>=config.max_groups_shown)
         {
            text += StringFormat("... %d more enabled groups hidden by display limit\n",state_count-g);
            break;
         }
         text += BuildGroupLine(states[g],config);
         shown_groups++;

         int start=group_start[g];
         int count=group_count[g];
         int shown=0;
         for(int i=count-1;i>=0;i--)
         {
            if(shown>=config.max_candidates_per_group_shown)
               break;
            int idx=start+i;
            if(idx<0 || idx>=ArraySize(flat_candidates))
               continue;
            text += BuildCandidateLine(flat_candidates[idx],config,field);
            shown++;
         }
      }
      return text;
   }

   string BuildPrintSummary(SCGTTimeSnapshot &time_snapshot,SCGDGroupDivergenceState &states[])
   {
      string text=StringFormat("EXP0017 Phase04 DivergenceAnatomy | NY=%s | groups=%d",
                               TimeToString(time_snapshot.new_york_now,TIME_DATE|TIME_MINUTES),ArraySize(states));
      for(int i=0;i<ArraySize(states);i++)
      {
         text += StringFormat(" | %s div=%d buy=%d sell=%d cleanA=%d cleanB=%d",
                              states[i].group_name,
                              states[i].candidate_count,
                              states[i].buy_candidate_count,
                              states[i].sell_candidate_count,
                              states[i].symbol_a_clean_count,
                              states[i].symbol_b_clean_count);
      }
      return text;
   }
};

#endif
