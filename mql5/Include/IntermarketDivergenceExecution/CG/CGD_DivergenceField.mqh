#ifndef __CGD_DIVERGENCE_FIELD_MQH__
#define __CGD_DIVERGENCE_FIELD_MQH__

#include <IntermarketDivergenceExecution/CG/CGD_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGH_HuntField.mqh>
#include <IntermarketDivergenceExecution/CG/CGT_Time.mqh>

class CCGD_DivergenceField
{
private:
   SCGDDivergenceConfig m_config;
   SCGHHuntConfig       m_hunt_config;
   CCGH_HuntField       m_hunt_field;

   void ResetGroupState(SCGDGroupDivergenceState &state)
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
      state.raw_hunt_count=0;
      state.candidate_count=0;
      state.buy_candidate_count=0;
      state.sell_candidate_count=0;
      state.symbol_a_hunter_count=0;
      state.symbol_b_hunter_count=0;
      state.symbol_a_clean_count=0;
      state.symbol_b_clean_count=0;
      state.symmetric_high_no_divergence_count=0;
      state.symmetric_low_no_divergence_count=0;
      state.missing_data_count=0;
      state.has_any_candidate=false;
      state.trading_day_start_ny=0;
      state.trading_day_end_ny=0;
      state.current_cycle_start_ny=0;
      state.current_cycle_end_ny=0;
   }

   void ResetCandidate(SCGDDivergenceCandidate &candidate)
   {
      candidate.divergence_id="";
      candidate.group_name="";
      candidate.group_minutes=0;
      candidate.current_cycle_index=-1;
      candidate.current_cycle_number=0;
      candidate.reference_cycle_index=-1;
      candidate.reference_cycle_number=0;
      candidate.trading_day_start_ny=0;
      candidate.trading_day_end_ny=0;
      candidate.current_cycle_start_ny=0;
      candidate.current_cycle_end_ny=0;
      candidate.reference_cycle_start_ny=0;
      candidate.reference_cycle_end_ny=0;
      candidate.direction=CGD_DIRECTION_NONE;
      candidate.side=CGD_SIDE_NONE;
      candidate.status=CGD_STATUS_NONE;
      candidate.hunter_symbol="";
      candidate.clean_symbol="";
      candidate.non_hunter_symbol="";
      candidate.symbol_a_is_hunter=false;
      candidate.symbol_b_is_hunter=false;
      candidate.one_sided_hunt=false;
      candidate.both_symbols_hunted_same_side=false;
      candidate.data_ready=false;
      candidate.hunter_reference_price=0.0;
      candidate.clean_reference_price=0.0;
      candidate.hunter_current_extreme=0.0;
      candidate.clean_current_extreme=0.0;
      candidate.clean_stop_reference_price=0.0;
      candidate.note="";
   }

   string DirectionText(const ECGDDivergenceDirection direction)
   {
      if(direction==CGD_DIRECTION_BUY)
         return "BUY";
      if(direction==CGD_DIRECTION_SELL)
         return "SELL";
      return "NONE";
   }

   string SideText(const ECGDDivergenceSide side)
   {
      if(side==CGD_SIDE_HIGH)
         return "HIGH";
      if(side==CGD_SIDE_LOW)
         return "LOW";
      return "NONE";
   }

   string BuildCandidateId(SCGTTimeSnapshot &time_snapshot,SCGHReferenceHuntState &hunt,const ECGDDivergenceDirection direction,const ECGDDivergenceSide side,const string hunter_symbol,const string clean_symbol)
   {
      return StringFormat("EXP0017|%s|TD%s|C%d|R%d|%s|%s|H:%s|C:%s",
                          hunt.group_name,
                          TimeToString(time_snapshot.trading_day_start_ny,TIME_DATE),
                          hunt.current_cycle_start_ny,
                          hunt.reference_cycle_start_ny,
                          DirectionText(direction),
                          SideText(side),
                          hunter_symbol,
                          clean_symbol);
   }

   bool BuildHighSideCandidate(SCGTTimeSnapshot &time_snapshot,SCGTCycleSnapshot &cycle,SCGHReferenceHuntState &hunt,SCGDDivergenceCandidate &candidate)
   {
      ResetCandidate(candidate);
      candidate.group_name=hunt.group_name;
      candidate.group_minutes=hunt.group_minutes;
      candidate.current_cycle_index=cycle.current_cycle_index;
      candidate.current_cycle_number=cycle.current_cycle_number;
      candidate.reference_cycle_index=hunt.reference_cycle_index;
      candidate.reference_cycle_number=hunt.reference_cycle_number;
      candidate.trading_day_start_ny=time_snapshot.trading_day_start_ny;
      candidate.trading_day_end_ny=time_snapshot.trading_day_end_ny;
      candidate.current_cycle_start_ny=hunt.current_cycle_start_ny;
      candidate.current_cycle_end_ny=hunt.current_cycle_end_ny;
      candidate.reference_cycle_start_ny=hunt.reference_cycle_start_ny;
      candidate.reference_cycle_end_ny=hunt.reference_cycle_end_ny;
      candidate.direction=CGD_DIRECTION_SELL;
      candidate.side=CGD_SIDE_HIGH;
      candidate.data_ready=(hunt.reference_ready && hunt.current_range_ready);

      if(!candidate.data_ready)
      {
         candidate.status=CGD_STATUS_MISSING_DATA;
         candidate.note="missing_data_no_divergence_classification";
         return false;
      }

      if(hunt.symbol_a.high_hunted && hunt.symbol_b.high_hunted)
      {
         candidate.status=CGD_STATUS_SYMMETRIC_HUNT_NO_DIVERGENCE;
         candidate.both_symbols_hunted_same_side=true;
         candidate.note="both_symbols_hunted_high_no_sell_divergence";
         return false;
      }

      if(hunt.symbol_a.high_hunted==hunt.symbol_b.high_hunted)
         return false;

      candidate.status=CGD_STATUS_CANDIDATE;
      candidate.one_sided_hunt=true;
      candidate.symbol_a_is_hunter=hunt.symbol_a.high_hunted;
      candidate.symbol_b_is_hunter=hunt.symbol_b.high_hunted;

      if(candidate.symbol_a_is_hunter)
      {
         candidate.hunter_symbol=m_config.symbol_a;
         candidate.clean_symbol=m_config.symbol_b;
         candidate.non_hunter_symbol=m_config.symbol_b;
         candidate.hunter_reference_price=hunt.symbol_a.reference_high;
         candidate.clean_reference_price=hunt.symbol_b.reference_high;
         candidate.hunter_current_extreme=hunt.symbol_a.current_high;
         candidate.clean_current_extreme=hunt.symbol_b.current_high;
         candidate.clean_stop_reference_price=hunt.symbol_b.reference_high;
      }
      else
      {
         candidate.hunter_symbol=m_config.symbol_b;
         candidate.clean_symbol=m_config.symbol_a;
         candidate.non_hunter_symbol=m_config.symbol_a;
         candidate.hunter_reference_price=hunt.symbol_b.reference_high;
         candidate.clean_reference_price=hunt.symbol_a.reference_high;
         candidate.hunter_current_extreme=hunt.symbol_b.current_high;
         candidate.clean_current_extreme=hunt.symbol_a.current_high;
         candidate.clean_stop_reference_price=hunt.symbol_a.reference_high;
      }

      candidate.divergence_id=BuildCandidateId(time_snapshot,hunt,candidate.direction,candidate.side,candidate.hunter_symbol,candidate.clean_symbol);
      candidate.note="one_sided_high_hunt_sell_divergence_candidate_trade_candidate_is_clean_symbol_no_trade_permission_yet";
      return true;
   }

   bool BuildLowSideCandidate(SCGTTimeSnapshot &time_snapshot,SCGTCycleSnapshot &cycle,SCGHReferenceHuntState &hunt,SCGDDivergenceCandidate &candidate)
   {
      ResetCandidate(candidate);
      candidate.group_name=hunt.group_name;
      candidate.group_minutes=hunt.group_minutes;
      candidate.current_cycle_index=cycle.current_cycle_index;
      candidate.current_cycle_number=cycle.current_cycle_number;
      candidate.reference_cycle_index=hunt.reference_cycle_index;
      candidate.reference_cycle_number=hunt.reference_cycle_number;
      candidate.trading_day_start_ny=time_snapshot.trading_day_start_ny;
      candidate.trading_day_end_ny=time_snapshot.trading_day_end_ny;
      candidate.current_cycle_start_ny=hunt.current_cycle_start_ny;
      candidate.current_cycle_end_ny=hunt.current_cycle_end_ny;
      candidate.reference_cycle_start_ny=hunt.reference_cycle_start_ny;
      candidate.reference_cycle_end_ny=hunt.reference_cycle_end_ny;
      candidate.direction=CGD_DIRECTION_BUY;
      candidate.side=CGD_SIDE_LOW;
      candidate.data_ready=(hunt.reference_ready && hunt.current_range_ready);

      if(!candidate.data_ready)
      {
         candidate.status=CGD_STATUS_MISSING_DATA;
         candidate.note="missing_data_no_divergence_classification";
         return false;
      }

      if(hunt.symbol_a.low_hunted && hunt.symbol_b.low_hunted)
      {
         candidate.status=CGD_STATUS_SYMMETRIC_HUNT_NO_DIVERGENCE;
         candidate.both_symbols_hunted_same_side=true;
         candidate.note="both_symbols_hunted_low_no_buy_divergence";
         return false;
      }

      if(hunt.symbol_a.low_hunted==hunt.symbol_b.low_hunted)
         return false;

      candidate.status=CGD_STATUS_CANDIDATE;
      candidate.one_sided_hunt=true;
      candidate.symbol_a_is_hunter=hunt.symbol_a.low_hunted;
      candidate.symbol_b_is_hunter=hunt.symbol_b.low_hunted;

      if(candidate.symbol_a_is_hunter)
      {
         candidate.hunter_symbol=m_config.symbol_a;
         candidate.clean_symbol=m_config.symbol_b;
         candidate.non_hunter_symbol=m_config.symbol_b;
         candidate.hunter_reference_price=hunt.symbol_a.reference_low;
         candidate.clean_reference_price=hunt.symbol_b.reference_low;
         candidate.hunter_current_extreme=hunt.symbol_a.current_low;
         candidate.clean_current_extreme=hunt.symbol_b.current_low;
         candidate.clean_stop_reference_price=hunt.symbol_b.reference_low;
      }
      else
      {
         candidate.hunter_symbol=m_config.symbol_b;
         candidate.clean_symbol=m_config.symbol_a;
         candidate.non_hunter_symbol=m_config.symbol_a;
         candidate.hunter_reference_price=hunt.symbol_b.reference_low;
         candidate.clean_reference_price=hunt.symbol_a.reference_low;
         candidate.hunter_current_extreme=hunt.symbol_b.current_low;
         candidate.clean_current_extreme=hunt.symbol_a.current_low;
         candidate.clean_stop_reference_price=hunt.symbol_a.reference_low;
      }

      candidate.divergence_id=BuildCandidateId(time_snapshot,hunt,candidate.direction,candidate.side,candidate.hunter_symbol,candidate.clean_symbol);
      candidate.note="one_sided_low_hunt_buy_divergence_candidate_trade_candidate_is_clean_symbol_no_trade_permission_yet";
      return true;
   }

public:
   void Configure(SCGDDivergenceConfig &config)
   {
      m_config=config;
      if(m_config.max_groups_shown<1)
         m_config.max_groups_shown=1;
      if(m_config.max_candidates_per_group_shown<0)
         m_config.max_candidates_per_group_shown=0;

      m_hunt_config.symbol_a=m_config.symbol_a;
      m_hunt_config.symbol_b=m_config.symbol_b;
      m_hunt_config.broker_utc_offset_hours=m_config.broker_utc_offset_hours;
      m_hunt_config.max_groups_shown=m_config.max_groups_shown;
      m_hunt_config.max_hunts_per_group_shown=m_config.max_candidates_per_group_shown;
      m_hunt_config.require_m1_history=m_config.require_m1_history;
      m_hunt_config.show_only_groups_with_hunts=false;
      m_hunt_config.show_reference_prices=m_config.show_prices;
      m_hunt_config.show_current_cycle_ranges=false;
      m_hunt_field.Configure(m_hunt_config);
   }

   int BuildDivergencesForGroup(SCGTTimeSnapshot &time_snapshot,SCGTCycleSnapshot &cycle,SCGDDivergenceCandidate &candidates[],SCGDGroupDivergenceState &state)
   {
      ArrayResize(candidates,0);
      ResetGroupState(state);
      state.group_name=cycle.group_name;
      state.group_minutes=cycle.group_minutes;
      state.enabled=cycle.enabled;
      state.inside_trading_day=cycle.inside_trading_day;
      state.current_cycle_index=cycle.current_cycle_index;
      state.current_cycle_number=cycle.current_cycle_number;
      state.previous_cycle_count=cycle.previous_cycle_count;
      state.trading_day_start_ny=time_snapshot.trading_day_start_ny;
      state.trading_day_end_ny=time_snapshot.trading_day_end_ny;
      state.current_cycle_start_ny=cycle.cycle_start_ny;
      state.current_cycle_end_ny=cycle.cycle_end_ny;

      if(!cycle.enabled || !cycle.inside_trading_day || cycle.previous_cycle_count<=0)
         return 0;

      SCGHReferenceHuntState hunts[];
      SCGHGroupHuntState hunt_state;
      int hunt_count=m_hunt_field.BuildHuntsForGroup(time_snapshot,cycle,hunts,hunt_state);
      state.raw_hunt_count=hunt_count;
      state.ready_reference_count=hunt_state.ready_reference_count;
      state.missing_reference_count=hunt_state.missing_reference_count;

      if(hunt_count<=0)
         return 0;

      int candidate_count=0;
      for(int i=0;i<hunt_count;i++)
      {
         if(!hunts[i].reference_ready || !hunts[i].current_range_ready)
         {
            state.missing_data_count++;
            continue;
         }

         if(hunts[i].high_hunted_by_both_symbols)
            state.symmetric_high_no_divergence_count++;
         if(hunts[i].low_hunted_by_both_symbols)
            state.symmetric_low_no_divergence_count++;

         SCGDDivergenceCandidate high_candidate;
         if(BuildHighSideCandidate(time_snapshot,cycle,hunts[i],high_candidate))
         {
            int idx=ArraySize(candidates);
            ArrayResize(candidates,idx+1);
            candidates[idx]=high_candidate;
            candidate_count++;
            state.candidate_count++;
            state.sell_candidate_count++;
            state.has_any_candidate=true;
            if(high_candidate.symbol_a_is_hunter) state.symbol_a_hunter_count++;
            if(high_candidate.symbol_b_is_hunter) state.symbol_b_hunter_count++;
            if(high_candidate.clean_symbol==m_config.symbol_a) state.symbol_a_clean_count++;
            if(high_candidate.clean_symbol==m_config.symbol_b) state.symbol_b_clean_count++;
         }

         SCGDDivergenceCandidate low_candidate;
         if(BuildLowSideCandidate(time_snapshot,cycle,hunts[i],low_candidate))
         {
            int idx=ArraySize(candidates);
            ArrayResize(candidates,idx+1);
            candidates[idx]=low_candidate;
            candidate_count++;
            state.candidate_count++;
            state.buy_candidate_count++;
            state.has_any_candidate=true;
            if(low_candidate.symbol_a_is_hunter) state.symbol_a_hunter_count++;
            if(low_candidate.symbol_b_is_hunter) state.symbol_b_hunter_count++;
            if(low_candidate.clean_symbol==m_config.symbol_a) state.symbol_a_clean_count++;
            if(low_candidate.clean_symbol==m_config.symbol_b) state.symbol_b_clean_count++;
         }
      }

      return candidate_count;
   }

   string FormatPrice(const double price)
   {
      if(price==0.0)
         return "-";
      return DoubleToString(price,CGD_PRICE_DIGITS);
   }

   string DirectionTextPublic(const ECGDDivergenceDirection direction)
   {
      return DirectionText(direction);
   }

   string SideTextPublic(const ECGDDivergenceSide side)
   {
      return SideText(side);
   }

   string FormatCycleRangeNY(const datetime start_ny,const datetime end_ny)
   {
      if(start_ny<=0 || end_ny<=0)
         return "-";
      return StringFormat("%s-%s NY",TimeToString(start_ny,TIME_MINUTES),TimeToString(end_ny-60,TIME_MINUTES));
   }
};

#endif
