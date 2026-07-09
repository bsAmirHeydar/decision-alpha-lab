#ifndef __CGH_HUNT_FIELD_MQH__
#define __CGH_HUNT_FIELD_MQH__

#include <IntermarketDivergenceExecution/CG/CGH_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGR_ReferenceField.mqh>
#include <IntermarketDivergenceExecution/CG/CGT_Time.mqh>

class CCGH_HuntField
{
private:
   SCGHHuntConfig     m_config;
   SCGRReferenceConfig m_ref_config;
   CCGR_ReferenceField m_reference_field;

   datetime NewYorkToBroker(const datetime ny_time,const int ny_utc_offset_hours)
   {
      // ny_time carries New York wall-clock fields in terminal datetime form.
      // UTC = NY - offset. Broker = UTC + broker_offset.
      return ny_time - (ny_utc_offset_hours*3600) + (m_config.broker_utc_offset_hours*3600);
   }

   void ResetCurrentRange(SCGHCurrentSymbolRange &range,const string symbol)
   {
      range.symbol=symbol;
      range.selected=false;
      range.data_ok=false;
      range.copied_bars=0;
      range.high=0.0;
      range.low=0.0;
      range.first_bar_broker=0;
      range.last_bar_broker=0;
      range.error_text="not_calculated";
   }

   bool AggregateCurrentCycleM1Range(const string symbol,const datetime start_broker,const datetime now_broker,SCGHCurrentSymbolRange &out_range)
   {
      ResetCurrentRange(out_range,symbol);
      out_range.selected=SymbolSelect(symbol,true);
      if(!out_range.selected)
      {
         out_range.error_text="symbol_select_failed";
         return false;
      }

      if(now_broker<=start_broker)
      {
         out_range.error_text="invalid_current_cycle_time_range";
         return false;
      }

      MqlRates rates[];
      ArraySetAsSeries(rates,false);

      int copied=CopyRates(symbol,PERIOD_M1,start_broker,now_broker,rates);
      out_range.copied_bars=copied;

      if(copied<=0)
      {
         out_range.error_text=StringFormat("no_current_m1_rates_%s_%s",TimeToString(start_broker,TIME_DATE|TIME_MINUTES),TimeToString(now_broker,TIME_DATE|TIME_MINUTES));
         return false;
      }

      double hi=rates[0].high;
      double lo=rates[0].low;
      out_range.first_bar_broker=rates[0].time;
      out_range.last_bar_broker=rates[copied-1].time;

      for(int i=1;i<copied;i++)
      {
         if(rates[i].high>hi)
            hi=rates[i].high;
         if(rates[i].low<lo)
            lo=rates[i].low;
      }

      out_range.high=hi;
      out_range.low=lo;
      out_range.data_ok=true;
      out_range.error_text="ok";
      return true;
   }

   void ResetSymbolHunt(SCGHSymbolHuntState &state,const string symbol)
   {
      state.symbol=symbol;
      state.reference_ready=false;
      state.current_range_ready=false;
      state.reference_high=0.0;
      state.reference_low=0.0;
      state.current_high=0.0;
      state.current_low=0.0;
      state.high_hunted=false;
      state.low_hunted=false;
      state.any_hunt=false;
      state.status_text="not_calculated";
   }

   void BuildSymbolHunt(const SCGRSymbolReference &reference,const SCGHCurrentSymbolRange &current,SCGHSymbolHuntState &out_state)
   {
      ResetSymbolHunt(out_state,reference.symbol);
      out_state.reference_ready=reference.data_ok;
      out_state.current_range_ready=current.data_ok;
      out_state.reference_high=reference.high;
      out_state.reference_low=reference.low;
      out_state.current_high=current.high;
      out_state.current_low=current.low;

      if(!reference.data_ok)
      {
         out_state.status_text="reference_missing";
         return;
      }
      if(!current.data_ok)
      {
         out_state.status_text="current_range_missing";
         return;
      }

      // Doctrine: hunt is touch-only. Equality counts. No close beyond is required.
      out_state.high_hunted=(current.high>=reference.high);
      out_state.low_hunted=(current.low<=reference.low);
      out_state.any_hunt=(out_state.high_hunted || out_state.low_hunted);

      if(out_state.high_hunted && out_state.low_hunted)
         out_state.status_text="high_and_low_hunted";
      else if(out_state.high_hunted)
         out_state.status_text="high_hunted";
      else if(out_state.low_hunted)
         out_state.status_text="low_hunted";
      else
         out_state.status_text="not_hunted";
   }

   void ResetGroupState(SCGHGroupHuntState &state)
   {
      state.group_name="";
      state.group_minutes=0;
      state.enabled=false;
      state.inside_trading_day=false;
      state.current_cycle_index=-1;
      state.current_cycle_number=0;
      state.previous_cycle_count=0;
      state.ready_reference_count=0;
      state.missing_reference_count=0;
      state.ready_current_range_count=0;
      state.hunt_state_count=0;
      state.any_hunt_count=0;
      state.high_hunt_count=0;
      state.low_hunt_count=0;
      state.symbol_a_hunt_count=0;
      state.symbol_b_hunt_count=0;
      state.one_symbol_high_hunt_count=0;
      state.one_symbol_low_hunt_count=0;
      state.both_symbol_high_hunt_count=0;
      state.both_symbol_low_hunt_count=0;
      state.has_any_hunt=false;
      state.current_cycle_start_ny=0;
      state.current_cycle_end_ny=0;
      ResetCurrentRange(state.current_a,m_config.symbol_a);
      ResetCurrentRange(state.current_b,m_config.symbol_b);
   }

public:
   void Configure(SCGHHuntConfig &config)
   {
      m_config=config;
      if(m_config.max_groups_shown<1)
         m_config.max_groups_shown=1;
      if(m_config.max_hunts_per_group_shown<0)
         m_config.max_hunts_per_group_shown=0;

      m_ref_config.symbol_a=m_config.symbol_a;
      m_ref_config.symbol_b=m_config.symbol_b;
      m_ref_config.broker_utc_offset_hours=m_config.broker_utc_offset_hours;
      m_ref_config.max_groups_shown=m_config.max_groups_shown;
      m_ref_config.max_references_per_group_shown=m_config.max_hunts_per_group_shown;
      m_ref_config.require_m1_history=m_config.require_m1_history;
      m_ref_config.show_only_groups_with_ready_references=false;
      m_reference_field.Configure(m_ref_config);
   }

   bool BuildGroupState(SCGTTimeSnapshot &time_snapshot,SCGTCycleSnapshot &cycle,SCGHGroupHuntState &state)
   {
      ResetGroupState(state);
      state.group_name=cycle.group_name;
      state.group_minutes=cycle.group_minutes;
      state.enabled=cycle.enabled;
      state.inside_trading_day=cycle.inside_trading_day;
      state.current_cycle_index=cycle.current_cycle_index;
      state.current_cycle_number=cycle.current_cycle_number;
      state.previous_cycle_count=cycle.previous_cycle_count;
      state.current_cycle_start_ny=cycle.cycle_start_ny;
      state.current_cycle_end_ny=cycle.cycle_end_ny;

      if(!cycle.enabled || !cycle.inside_trading_day)
         return false;

      datetime current_start_broker=NewYorkToBroker(cycle.cycle_start_ny,time_snapshot.new_york_utc_offset_hours);
      bool a_ok=AggregateCurrentCycleM1Range(m_config.symbol_a,current_start_broker,time_snapshot.broker_now,state.current_a);
      bool b_ok=AggregateCurrentCycleM1Range(m_config.symbol_b,current_start_broker,time_snapshot.broker_now,state.current_b);
      state.ready_current_range_count=(a_ok ? 1 : 0) + (b_ok ? 1 : 0);
      return true;
   }

   bool BuildReferenceHuntState(SCGTTimeSnapshot &time_snapshot,SCGTCycleSnapshot &cycle,const SCGRReferencePair &ref_pair,const SCGHCurrentSymbolRange &current_a,const SCGHCurrentSymbolRange &current_b,SCGHReferenceHuntState &hunt)
   {
      hunt.group_name=ref_pair.group_name;
      hunt.group_minutes=ref_pair.group_minutes;
      hunt.reference_cycle_index=ref_pair.reference_cycle_index;
      hunt.reference_cycle_number=ref_pair.reference_cycle_number;
      hunt.reference_cycle_start_ny=ref_pair.cycle_start_ny;
      hunt.reference_cycle_end_ny=ref_pair.cycle_end_ny;
      hunt.current_cycle_start_ny=cycle.cycle_start_ny;
      hunt.current_cycle_end_ny=cycle.cycle_end_ny;
      hunt.reference_ready=ref_pair.ready;
      hunt.current_range_ready=(current_a.data_ok && current_b.data_ok);
      hunt.any_hunt=false;
      hunt.high_hunted_by_both_symbols=false;
      hunt.low_hunted_by_both_symbols=false;
      hunt.high_hunted_by_one_symbol_only=false;
      hunt.low_hunted_by_one_symbol_only=false;
      ResetSymbolHunt(hunt.symbol_a,m_config.symbol_a);
      ResetSymbolHunt(hunt.symbol_b,m_config.symbol_b);

      if(!ref_pair.ready)
         return false;

      BuildSymbolHunt(ref_pair.symbol_a,current_a,hunt.symbol_a);
      BuildSymbolHunt(ref_pair.symbol_b,current_b,hunt.symbol_b);

      hunt.any_hunt=(hunt.symbol_a.any_hunt || hunt.symbol_b.any_hunt);
      hunt.high_hunted_by_both_symbols=(hunt.symbol_a.high_hunted && hunt.symbol_b.high_hunted);
      hunt.low_hunted_by_both_symbols=(hunt.symbol_a.low_hunted && hunt.symbol_b.low_hunted);
      hunt.high_hunted_by_one_symbol_only=(hunt.symbol_a.high_hunted != hunt.symbol_b.high_hunted);
      hunt.low_hunted_by_one_symbol_only=(hunt.symbol_a.low_hunted != hunt.symbol_b.low_hunted);
      return true;
   }

   int BuildHuntsForGroup(SCGTTimeSnapshot &time_snapshot,SCGTCycleSnapshot &cycle,SCGHReferenceHuntState &hunts[],SCGHGroupHuntState &state)
   {
      ArrayResize(hunts,0);
      BuildGroupState(time_snapshot,cycle,state);

      if(!cycle.enabled || !cycle.inside_trading_day || cycle.previous_cycle_count<=0)
         return 0;

      SCGRReferencePair refs[];
      SCGRGroupReferenceState ref_state;
      int ref_count=m_reference_field.BuildReferencesForGroup(time_snapshot,cycle,refs,ref_state);
      state.ready_reference_count=ref_state.ready_reference_count;
      state.missing_reference_count=ref_state.missing_reference_count;

      if(ref_count<=0)
         return 0;

      ArrayResize(hunts,ref_count);
      int hunt_count=0;

      for(int i=0;i<ref_count;i++)
      {
         SCGHReferenceHuntState h;
         BuildReferenceHuntState(time_snapshot,cycle,refs[i],state.current_a,state.current_b,h);
         hunts[i]=h;
         hunt_count++;

         if(h.any_hunt)
         {
            state.any_hunt_count++;
            state.has_any_hunt=true;
         }
         if(h.symbol_a.high_hunted || h.symbol_b.high_hunted)
            state.high_hunt_count++;
         if(h.symbol_a.low_hunted || h.symbol_b.low_hunted)
            state.low_hunt_count++;
         if(h.symbol_a.any_hunt)
            state.symbol_a_hunt_count++;
         if(h.symbol_b.any_hunt)
            state.symbol_b_hunt_count++;
         if(h.high_hunted_by_one_symbol_only)
            state.one_symbol_high_hunt_count++;
         if(h.low_hunted_by_one_symbol_only)
            state.one_symbol_low_hunt_count++;
         if(h.high_hunted_by_both_symbols)
            state.both_symbol_high_hunt_count++;
         if(h.low_hunted_by_both_symbols)
            state.both_symbol_low_hunt_count++;
      }

      state.hunt_state_count=hunt_count;
      return hunt_count;
   }

   string FormatPrice(const double price)
   {
      if(price==0.0)
         return "-";
      return DoubleToString(price,CGH_PRICE_DIGITS);
   }

   string FormatCycleRangeNY(const datetime start_ny,const datetime end_ny)
   {
      if(start_ny<=0 || end_ny<=0)
         return "-";
      return StringFormat("%s-%s NY",TimeToString(start_ny,TIME_MINUTES),TimeToString(end_ny-60,TIME_MINUTES));
   }

   string HuntMark(const bool high_hunted,const bool low_hunted)
   {
      if(high_hunted && low_hunted)
         return "H+L";
      if(high_hunted)
         return "H";
      if(low_hunted)
         return "L";
      return "-";
   }
};

#endif
