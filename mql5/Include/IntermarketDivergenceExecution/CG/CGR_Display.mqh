#ifndef __CGR_DISPLAY_MQH__
#define __CGR_DISPLAY_MQH__

#include <IntermarketDivergenceExecution/CG/CGR_ReferenceField.mqh>

class CCGR_Display
{
private:
   string BoolText(const bool v)
   {
      return v ? "yes" : "no";
   }

public:
   string BuildHeader(SCGTTimeSnapshot &time_snapshot,SCGRReferenceConfig &config)
   {
      string text="";
      text += "EXP0017 Phase 02 - Reference Field Anatomy\n";
      text += "No trade | No hunt | No divergence | Reference high/low only\n";
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

   string BuildGroupLine(SCGRGroupReferenceState &state)
   {
      return StringFormat("%s | current #%d | prev=%d | ready=%d | missing=%d | current=%s-%s NY\n",
                          state.group_name,
                          state.current_cycle_number,
                          state.previous_cycle_count,
                          state.ready_reference_count,
                          state.missing_reference_count,
                          TimeToString(state.current_cycle_start_ny,TIME_MINUTES),
                          TimeToString(state.current_cycle_end_ny-60,TIME_MINUTES));
   }

   string BuildReferenceLine(SCGRReferencePair &pair,CCGR_ReferenceField &field)
   {
      string status=pair.ready ? "ready" : "missing";
      return StringFormat("  ref #%d %s | %s | A H/L %s / %s bars=%d | B H/L %s / %s bars=%d\n",
                          pair.reference_cycle_number,
                          field.FormatCycleRangeNY(pair),
                          status,
                          field.FormatPrice(pair.symbol_a.high),
                          field.FormatPrice(pair.symbol_a.low),
                          pair.symbol_a.copied_bars,
                          field.FormatPrice(pair.symbol_b.high),
                          field.FormatPrice(pair.symbol_b.low),
                          pair.symbol_b.copied_bars);
   }

   string BuildPanel(SCGTTimeSnapshot &time_snapshot,SCGRReferenceConfig &config,SCGRGroupReferenceState &states[],SCGRReferencePair &flat_refs[],int &group_start[],int &group_count[],CCGR_ReferenceField &field)
   {
      string text=BuildHeader(time_snapshot,config);
      int shown_groups=0;
      int state_count=ArraySize(states);
      for(int g=0;g<state_count;g++)
      {
         if(config.show_only_groups_with_ready_references && !states[g].has_ready_reference)
            continue;
         if(shown_groups>=config.max_groups_shown)
         {
            text += StringFormat("... %d more enabled groups hidden by display limit\n",state_count-g);
            break;
         }

         text += BuildGroupLine(states[g]);
         int start=group_start[g];
         int count=group_count[g];
         int shown_refs=0;

         // Show the most recent completed reference cycles first.
         for(int i=count-1;i>=0;i--)
         {
            if(shown_refs>=config.max_references_per_group_shown)
               break;
            int idx=start+i;
            if(idx>=0 && idx<ArraySize(flat_refs))
            {
               text += BuildReferenceLine(flat_refs[idx],field);
               shown_refs++;
            }
         }
      }
      return text;
   }

   string BuildPrintSummary(SCGTTimeSnapshot &time_snapshot,SCGRGroupReferenceState &states[])
   {
      string text=StringFormat("EXP0017 Phase02 ReferenceField | NY=%s | groups=%d",
                               TimeToString(time_snapshot.new_york_now,TIME_DATE|TIME_MINUTES),ArraySize(states));
      for(int i=0;i<ArraySize(states);i++)
      {
         text += StringFormat(" | %s prev=%d ready=%d missing=%d",
                              states[i].group_name,
                              states[i].previous_cycle_count,
                              states[i].ready_reference_count,
                              states[i].missing_reference_count);
      }
      return text;
   }
};

#endif
