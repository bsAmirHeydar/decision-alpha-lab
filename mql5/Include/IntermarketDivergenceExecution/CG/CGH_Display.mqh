#ifndef __CGH_DISPLAY_MQH__
#define __CGH_DISPLAY_MQH__

#include <IntermarketDivergenceExecution/CG/CGH_HuntField.mqh>

class CCGH_Display
{
private:
   string BoolText(const bool v)
   {
      return v ? "yes" : "no";
   }

public:
   string BuildHeader(SCGTTimeSnapshot &time_snapshot,SCGHHuntConfig &config)
   {
      string text="";
      text += "EXP0017 Phase 03 - Hunt Anatomy\n";
      text += "No trade | No divergence | No confirmation | Hunt touch/break/equality only\n";
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

   string BuildCurrentRangeText(SCGHGroupHuntState &state,CCGH_HuntField &field)
   {
      string text="";
      text += StringFormat(" | A curr H/L %s/%s bars=%d",
                           field.FormatPrice(state.current_a.high),
                           field.FormatPrice(state.current_a.low),
                           state.current_a.copied_bars);
      text += StringFormat(" | B curr H/L %s/%s bars=%d",
                           field.FormatPrice(state.current_b.high),
                           field.FormatPrice(state.current_b.low),
                           state.current_b.copied_bars);
      return text;
   }

   string BuildGroupLine(SCGHGroupHuntState &state,SCGHHuntConfig &config,CCGH_HuntField &field)
   {
      string text=StringFormat("%s | current #%d %s-%s NY | refs ready=%d missing=%d | hunts any=%d H=%d L=%d | one-side H=%d L=%d | both H=%d L=%d",
                               state.group_name,
                               state.current_cycle_number,
                               TimeToString(state.current_cycle_start_ny,TIME_MINUTES),
                               TimeToString(state.current_cycle_end_ny-60,TIME_MINUTES),
                               state.ready_reference_count,
                               state.missing_reference_count,
                               state.any_hunt_count,
                               state.high_hunt_count,
                               state.low_hunt_count,
                               state.one_symbol_high_hunt_count,
                               state.one_symbol_low_hunt_count,
                               state.both_symbol_high_hunt_count,
                               state.both_symbol_low_hunt_count);
      if(config.show_current_cycle_ranges)
         text += BuildCurrentRangeText(state,field);
      text += "\n";
      return text;
   }

   string BuildHuntLine(SCGHReferenceHuntState &hunt,SCGHHuntConfig &config,CCGH_HuntField &field)
   {
      string text=StringFormat("  ref #%d %s | A=%s B=%s",
                               hunt.reference_cycle_number,
                               field.FormatCycleRangeNY(hunt.reference_cycle_start_ny,hunt.reference_cycle_end_ny),
                               field.HuntMark(hunt.symbol_a.high_hunted,hunt.symbol_a.low_hunted),
                               field.HuntMark(hunt.symbol_b.high_hunted,hunt.symbol_b.low_hunted));

      text += StringFormat(" | one-side H=%s L=%s | both H=%s L=%s",
                           BoolText(hunt.high_hunted_by_one_symbol_only),
                           BoolText(hunt.low_hunted_by_one_symbol_only),
                           BoolText(hunt.high_hunted_by_both_symbols),
                           BoolText(hunt.low_hunted_by_both_symbols));

      if(config.show_reference_prices)
      {
         text += StringFormat(" | A ref H/L %s/%s curr H/L %s/%s | B ref H/L %s/%s curr H/L %s/%s",
                              field.FormatPrice(hunt.symbol_a.reference_high),
                              field.FormatPrice(hunt.symbol_a.reference_low),
                              field.FormatPrice(hunt.symbol_a.current_high),
                              field.FormatPrice(hunt.symbol_a.current_low),
                              field.FormatPrice(hunt.symbol_b.reference_high),
                              field.FormatPrice(hunt.symbol_b.reference_low),
                              field.FormatPrice(hunt.symbol_b.current_high),
                              field.FormatPrice(hunt.symbol_b.current_low));
      }
      text += "\n";
      return text;
   }

   string BuildPanel(SCGTTimeSnapshot &time_snapshot,SCGHHuntConfig &config,SCGHGroupHuntState &states[],SCGHReferenceHuntState &flat_hunts[],int &group_start[],int &group_count[],CCGH_HuntField &field)
   {
      string text=BuildHeader(time_snapshot,config);
      int shown_groups=0;
      int state_count=ArraySize(states);
      for(int g=0;g<state_count;g++)
      {
         if(config.show_only_groups_with_hunts && !states[g].has_any_hunt)
            continue;
         if(shown_groups>=config.max_groups_shown)
         {
            text += StringFormat("... %d more enabled groups hidden by display limit\n",state_count-g);
            break;
         }

         text += BuildGroupLine(states[g],config,field);
         shown_groups++;

         int start=group_start[g];
         int count=group_count[g];
         int shown=0;

         // Show most recent reference checks first, prioritizing actual hunts.
         for(int pass=0;pass<2;pass++)
         {
            for(int i=count-1;i>=0;i--)
            {
               if(shown>=config.max_hunts_per_group_shown)
                  break;
               int idx=start+i;
               if(idx<0 || idx>=ArraySize(flat_hunts))
                  continue;
               bool is_hunt=flat_hunts[idx].any_hunt;
               if((pass==0 && !is_hunt) || (pass==1 && is_hunt))
                  continue;
               text += BuildHuntLine(flat_hunts[idx],config,field);
               shown++;
            }
            if(shown>=config.max_hunts_per_group_shown)
               break;
         }
      }
      return text;
   }

   string BuildPrintSummary(SCGTTimeSnapshot &time_snapshot,SCGHGroupHuntState &states[])
   {
      string text=StringFormat("EXP0017 Phase03 HuntAnatomy | NY=%s | groups=%d",
                               TimeToString(time_snapshot.new_york_now,TIME_DATE|TIME_MINUTES),ArraySize(states));
      for(int i=0;i<ArraySize(states);i++)
      {
         text += StringFormat(" | %s refs=%d hunts=%d H=%d L=%d oneH=%d oneL=%d bothH=%d bothL=%d",
                              states[i].group_name,
                              states[i].ready_reference_count,
                              states[i].any_hunt_count,
                              states[i].high_hunt_count,
                              states[i].low_hunt_count,
                              states[i].one_symbol_high_hunt_count,
                              states[i].one_symbol_low_hunt_count,
                              states[i].both_symbol_high_hunt_count,
                              states[i].both_symbol_low_hunt_count);
      }
      return text;
   }
};

#endif
