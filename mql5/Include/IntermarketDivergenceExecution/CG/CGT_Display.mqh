#ifndef __CGT_DISPLAY_MQH__
#define __CGT_DISPLAY_MQH__

#include <IntermarketDivergenceExecution/CG/CGT_Time.mqh>

class CCGT_Display
{
private:
   string BoolText(const bool value)
   {
      return value ? "YES" : "NO";
   }

public:
   string BuildPanel(SCGTTimeSnapshot &time_snapshot,SCGTCycleSnapshot &cycles[],CCGT_TimeAnatomy &time)
   {
      string out="";
      out+="EXP0017 | Phase 01 | CG Time Anatomy\n";
      out+="No trade | No hunt | No divergence | Time anatomy only\n";
      out+="────────────────────────────────────────\n";
      out+=StringFormat("Broker Now: %s\n",TimeToString(time_snapshot.broker_now,TIME_DATE|TIME_MINUTES|TIME_SECONDS));
      out+=StringFormat("UTC Now:    %s\n",TimeToString(time_snapshot.utc_now,TIME_DATE|TIME_MINUTES|TIME_SECONDS));
      out+=StringFormat("NY Now:     %s | NY UTC Offset: %+d\n",TimeToString(time_snapshot.new_york_now,TIME_DATE|TIME_MINUTES|TIME_SECONDS),time_snapshot.new_york_utc_offset_hours);
      out+=StringFormat("Trading Day: %s | %s -> %s | Inside: %s\n",
                        time_snapshot.trading_day_label,
                        time.FormatNY(time_snapshot.trading_day_start_ny),
                        time.FormatNY(time_snapshot.trading_day_end_ny),
                        BoolText(time_snapshot.inside_trading_day));
      if(time_snapshot.inside_trading_day)
         out+=StringFormat("Elapsed: %d min | Remaining: %d min\n",time_snapshot.elapsed_minutes_from_day_start,time_snapshot.remaining_minutes_to_day_end);
      else
         out+="Outside active 18:00-17:00 NY trading-day field.\n";
      out+="────────────────────────────────────────\n";

      int n=ArraySize(cycles);
      for(int i=0;i<n;i++)
      {
         SCGTCycleSnapshot c=cycles[i];
         if(!c.enabled)
            continue;

         if(!c.inside_trading_day)
         {
            out+=StringFormat("%-8s | outside trading day\n",c.group_name);
            continue;
         }

         string partial=c.is_partial_last_cycle ? " | partial-last" : "";
         out+=StringFormat("%-8s | C%02d/%02d | %s | prev=%d | remain=%d min%s\n",
                           c.group_name,
                           c.current_cycle_number,
                           c.total_cycle_count,
                           time.FormatMinuteRange(c.cycle_start_minute,c.cycle_end_minute),
                           c.previous_cycle_count,
                           c.minutes_remaining_in_cycle,
                           partial);

         int max_prev=time.MaxPreviousCyclesShown();
         if(max_prev>0 && c.previous_cycle_count>0)
         {
            int first_prev=c.previous_cycle_count-max_prev;
            if(first_prev<0)
               first_prev=0;
            out+="         prev: ";
            for(int p=first_prev;p<c.previous_cycle_count;p++)
            {
               int ps=p*c.group_minutes;
               int pe=ps+c.group_minutes;
               if(pe>CGT_TRADING_DAY_MINUTES)
                  pe=CGT_TRADING_DAY_MINUTES;
               out+=StringFormat("C%02d[%s] ",p+1,time.FormatMinuteRange(ps,pe));
            }
            out+="\n";
         }
      }
      return out;
   }

   string BuildPrintLine(SCGTTimeSnapshot &time_snapshot,SCGTCycleSnapshot &cycles[],CCGT_TimeAnatomy &time)
   {
      string out=StringFormat("EXP0017 Phase01 | NY=%s | TD=%s | inside=%s",
                              TimeToString(time_snapshot.new_york_now,TIME_DATE|TIME_MINUTES),
                              time_snapshot.trading_day_label,
                              BoolText(time_snapshot.inside_trading_day));
      int n=ArraySize(cycles);
      for(int i=0;i<n;i++)
      {
         SCGTCycleSnapshot c=cycles[i];
         if(c.enabled && c.inside_trading_day)
            out+=StringFormat(" | %s:C%d/%d",c.group_name,c.current_cycle_number,c.total_cycle_count);
      }
      return out;
   }
};

#endif
