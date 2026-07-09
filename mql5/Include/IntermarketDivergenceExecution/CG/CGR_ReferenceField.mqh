#ifndef __CGR_REFERENCE_FIELD_MQH__
#define __CGR_REFERENCE_FIELD_MQH__

#include <IntermarketDivergenceExecution/CG/CGR_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGT_Time.mqh>

class CCGR_ReferenceField
{
private:
   SCGRReferenceConfig m_config;

   datetime NewYorkToBroker(const datetime ny_time,const int ny_utc_offset_hours)
   {
      // ny_time is represented as a terminal datetime value carrying NY wall-clock fields.
      // UTC = NY - offset. Broker = UTC + broker_offset.
      return ny_time - (ny_utc_offset_hours*3600) + (m_config.broker_utc_offset_hours*3600);
   }

   void ResetSymbolReference(SCGRSymbolReference &ref,const string symbol)
   {
      ref.symbol=symbol;
      ref.selected=false;
      ref.data_ok=false;
      ref.copied_bars=0;
      ref.high=0.0;
      ref.low=0.0;
      ref.first_bar_broker=0;
      ref.last_bar_broker=0;
      ref.error_text="not_calculated";
   }

   bool AggregateM1HighLow(const string symbol,const datetime start_broker,const datetime end_broker_exclusive,SCGRSymbolReference &out_ref)
   {
      ResetSymbolReference(out_ref,symbol);
      out_ref.selected=SymbolSelect(symbol,true);
      if(!out_ref.selected)
      {
         out_ref.error_text="symbol_select_failed";
         return false;
      }

      if(end_broker_exclusive<=start_broker)
      {
         out_ref.error_text="invalid_cycle_time_range";
         return false;
      }

      MqlRates rates[];
      ArraySetAsSeries(rates,false);

      datetime stop_inclusive=end_broker_exclusive-1;
      int copied=CopyRates(symbol,PERIOD_M1,start_broker,stop_inclusive,rates);
      out_ref.copied_bars=copied;

      if(copied<=0)
      {
         out_ref.error_text=StringFormat("no_m1_rates_%s_%s",TimeToString(start_broker,TIME_DATE|TIME_MINUTES),TimeToString(end_broker_exclusive,TIME_DATE|TIME_MINUTES));
         return false;
      }

      double hi=rates[0].high;
      double lo=rates[0].low;
      out_ref.first_bar_broker=rates[0].time;
      out_ref.last_bar_broker=rates[copied-1].time;

      for(int i=1;i<copied;i++)
      {
         if(rates[i].high>hi)
            hi=rates[i].high;
         if(rates[i].low<lo)
            lo=rates[i].low;
      }

      out_ref.high=hi;
      out_ref.low=lo;
      out_ref.data_ok=true;
      out_ref.error_text="ok";
      return true;
   }

public:
   void Configure(SCGRReferenceConfig &config)
   {
      m_config=config;
      if(m_config.max_groups_shown<1)
         m_config.max_groups_shown=1;
      if(m_config.max_references_per_group_shown<0)
         m_config.max_references_per_group_shown=0;
   }

   bool BuildGroupState(SCGTTimeSnapshot &time_snapshot,SCGTCycleSnapshot &cycle,SCGRGroupReferenceState &state)
   {
      state.group_name=cycle.group_name;
      state.group_minutes=cycle.group_minutes;
      state.enabled=cycle.enabled;
      state.inside_trading_day=cycle.inside_trading_day;
      state.current_cycle_index=cycle.current_cycle_index;
      state.current_cycle_number=cycle.current_cycle_number;
      state.previous_cycle_count=cycle.previous_cycle_count;
      state.ready_reference_count=0;
      state.missing_reference_count=0;
      state.has_any_reference=(cycle.previous_cycle_count>0);
      state.has_ready_reference=false;
      state.current_cycle_start_ny=cycle.cycle_start_ny;
      state.current_cycle_end_ny=cycle.cycle_end_ny;
      return cycle.enabled && cycle.inside_trading_day;
   }

   bool BuildReferencePair(SCGTTimeSnapshot &time_snapshot,SCGTCycleSnapshot &cycle,const int reference_cycle_index,SCGRReferencePair &pair)
   {
      pair.group_name=cycle.group_name;
      pair.group_minutes=cycle.group_minutes;
      pair.reference_cycle_index=reference_cycle_index;
      pair.reference_cycle_number=reference_cycle_index+1;
      pair.start_minute=reference_cycle_index*cycle.group_minutes;
      pair.end_minute_exclusive=pair.start_minute+cycle.group_minutes;
      if(pair.end_minute_exclusive>CGT_TRADING_DAY_MINUTES)
         pair.end_minute_exclusive=CGT_TRADING_DAY_MINUTES;

      pair.complete_cycle=(pair.end_minute_exclusive<=cycle.cycle_start_minute);
      pair.cycle_start_ny=time_snapshot.trading_day_start_ny+(pair.start_minute*60);
      pair.cycle_end_ny=time_snapshot.trading_day_start_ny+(pair.end_minute_exclusive*60);
      pair.cycle_start_broker=NewYorkToBroker(pair.cycle_start_ny,time_snapshot.new_york_utc_offset_hours);
      pair.cycle_end_broker=NewYorkToBroker(pair.cycle_end_ny,time_snapshot.new_york_utc_offset_hours);

      ResetSymbolReference(pair.symbol_a,m_config.symbol_a);
      ResetSymbolReference(pair.symbol_b,m_config.symbol_b);

      if(!pair.complete_cycle)
      {
         pair.ready=false;
         pair.symbol_a.error_text="reference_cycle_not_complete";
         pair.symbol_b.error_text="reference_cycle_not_complete";
         return false;
      }

      bool a_ok=AggregateM1HighLow(m_config.symbol_a,pair.cycle_start_broker,pair.cycle_end_broker,pair.symbol_a);
      bool b_ok=AggregateM1HighLow(m_config.symbol_b,pair.cycle_start_broker,pair.cycle_end_broker,pair.symbol_b);
      pair.ready=(a_ok && b_ok);
      return pair.ready;
   }

   int BuildReferencesForGroup(SCGTTimeSnapshot &time_snapshot,SCGTCycleSnapshot &cycle,SCGRReferencePair &references[],SCGRGroupReferenceState &state)
   {
      BuildGroupState(time_snapshot,cycle,state);
      ArrayResize(references,0);

      if(!cycle.enabled || !cycle.inside_trading_day || cycle.previous_cycle_count<=0)
         return 0;

      int total=cycle.previous_cycle_count;
      ArrayResize(references,total);

      int ready_count=0;
      int missing_count=0;

      for(int i=0;i<total;i++)
      {
         SCGRReferencePair pair;
         bool ready=BuildReferencePair(time_snapshot,cycle,i,pair);
         references[i]=pair;
         if(ready)
            ready_count++;
         else
            missing_count++;
      }

      state.ready_reference_count=ready_count;
      state.missing_reference_count=missing_count;
      state.has_ready_reference=(ready_count>0);
      return total;
   }

   string FormatPrice(const double price)
   {
      if(price==0.0)
         return "-";
      return DoubleToString(price,CGR_PRICE_DIGITS);
   }

   string FormatBroker(const datetime t)
   {
      if(t<=0)
         return "-";
      return TimeToString(t,TIME_DATE|TIME_MINUTES);
   }

   string FormatCycleRangeNY(const SCGRReferencePair &pair)
   {
      return StringFormat("%s-%s NY",TimeToString(pair.cycle_start_ny,TIME_MINUTES),TimeToString(pair.cycle_end_ny-60,TIME_MINUTES));
   }
};

#endif
