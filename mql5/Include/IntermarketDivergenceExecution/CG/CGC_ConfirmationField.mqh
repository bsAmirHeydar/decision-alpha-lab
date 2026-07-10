#ifndef __CGC_CONFIRMATION_FIELD_MQH__
#define __CGC_CONFIRMATION_FIELD_MQH__

#include <IntermarketDivergenceExecution/CG/CGC_Types.mqh>
#include <IntermarketDivergenceExecution/CG/CGH_HuntField.mqh>
#include <IntermarketDivergenceExecution/CG/CGT_Time.mqh>

class CCGC_ConfirmationField
{
private:
   SCGCConfirmationConfig m_config;
   SCGHHuntConfig         m_hunt_config;
   CCGH_HuntField         m_hunt_field;
   SCGCProtectedReferenceLifecycleRecord m_lifecycle_records[];
   datetime               m_lifecycle_day_start_ny;
   bool                   m_lifecycle_initialized;

   void ResetLifecycleRecords()
   {
      ArrayResize(m_lifecycle_records,0);
      m_lifecycle_day_start_ny=0;
      m_lifecycle_initialized=false;
   }

   void EnsureLifecycleDay(SCGTTimeSnapshot &time_snapshot)
   {
      if(!m_config.enable_protected_reference_retirement)
         return;

      if(!m_config.reset_lifecycle_at_new_trading_day)
      {
         if(!m_lifecycle_initialized)
         {
            m_lifecycle_day_start_ny=time_snapshot.trading_day_start_ny;
            m_lifecycle_initialized=true;
         }
         return;
      }

      if(!m_lifecycle_initialized || m_lifecycle_day_start_ny!=time_snapshot.trading_day_start_ny)
      {
         ArrayResize(m_lifecycle_records,0);
         m_lifecycle_day_start_ny=time_snapshot.trading_day_start_ny;
         m_lifecycle_initialized=true;
      }
   }

   string BuildReferenceLifecycleKey(SCGTTimeSnapshot &time_snapshot,SCGHReferenceHuntState &hunt,const ECGCSignalSide side)
   {
      return StringFormat("EXP0017|REFLIFE|%s|TD:%s|R:%s|SIDE:%s",
                          hunt.group_name,
                          TimeToString(time_snapshot.trading_day_start_ny,TIME_DATE|TIME_MINUTES),
                          TimeToString(hunt.reference_cycle_start_ny,TIME_DATE|TIME_MINUTES),
                          SideText(side));
   }

   int FindLifecycleRecord(const string key)
   {
      int total=ArraySize(m_lifecycle_records);
      for(int i=0;i<total;i++)
      {
         if(m_lifecycle_records[i].key==key)
            return i;
      }
      return -1;
   }

   bool SymbolHuntedReferenceSide(SCGHReferenceHuntState &hunt,const ECGCSignalSide side,const string symbol)
   {
      if(symbol==m_config.symbol_a)
      {
         if(side==CGC_SIDE_HIGH)
            return hunt.symbol_a.high_hunted;
         if(side==CGC_SIDE_LOW)
            return hunt.symbol_a.low_hunted;
      }
      if(symbol==m_config.symbol_b)
      {
         if(side==CGC_SIDE_HIGH)
            return hunt.symbol_b.high_hunted;
         if(side==CGC_SIDE_LOW)
            return hunt.symbol_b.low_hunted;
      }
      return false;
   }

   void RetireLifecycleRecordByIndex(const int index,const datetime retirement_time_ny,const string reason)
   {
      if(index<0 || index>=ArraySize(m_lifecycle_records))
         return;
      m_lifecycle_records[index].retired=true;
      m_lifecycle_records[index].active=false;
      m_lifecycle_records[index].retirement_time_ny=retirement_time_ny;
      m_lifecycle_records[index].retirement_reason=reason;
   }

   bool ReferenceLifecycleIsRetired(const string key)
   {
      if(!m_config.enable_protected_reference_retirement)
         return false;
      int index=FindLifecycleRecord(key);
      if(index<0)
         return false;
      return m_lifecycle_records[index].retired;
   }

   void MarkProtectedBreachIfNeeded(SCGTTimeSnapshot &time_snapshot,SCGHReferenceHuntState &hunt,const ECGCSignalSide side)
   {
      if(!m_config.enable_protected_reference_retirement || !m_config.retire_reference_when_protected_hunts)
         return;
      string key=BuildReferenceLifecycleKey(time_snapshot,hunt,side);
      int index=FindLifecycleRecord(key);
      if(index<0)
         return;
      if(m_lifecycle_records[index].retired)
         return;
      string protected_symbol=m_lifecycle_records[index].protected_symbol;
      if(SymbolHuntedReferenceSide(hunt,side,protected_symbol))
         RetireLifecycleRecordByIndex(index,time_snapshot.new_york_now,"protected_symbol_hunted_its_reference_side");
   }

   bool ActivateOrAllowProtectedReference(SCGTTimeSnapshot &time_snapshot,
                                          SCGHReferenceHuntState &hunt,
                                          const ECGCSignalSide side,
                                          const string hunter_symbol,
                                          const string clean_symbol,
                                          string &lifecycle_note)
   {
      lifecycle_note="";
      if(!m_config.enable_protected_reference_retirement)
         return true;

      string key=BuildReferenceLifecycleKey(time_snapshot,hunt,side);
      int index=FindLifecycleRecord(key);

      if(index>=0 && m_lifecycle_records[index].retired)
      {
         lifecycle_note="suppressed_reference_side_already_retired_after_protected_breach";
         return !m_config.suppress_retired_reference_signals;
      }

      if(index<0)
      {
         int max_records=m_config.max_protected_reference_records;
         if(max_records<1)
            max_records=2048;
         int total=ArraySize(m_lifecycle_records);
         if(total>=max_records)
         {
            lifecycle_note="suppressed_lifecycle_record_capacity_reached";
            return false;
         }
         ArrayResize(m_lifecycle_records,total+1);
         index=total;
         m_lifecycle_records[index].key=key;
         m_lifecycle_records[index].group_name=hunt.group_name;
         m_lifecycle_records[index].side=side;
         m_lifecycle_records[index].active=true;
         m_lifecycle_records[index].retired=false;
         m_lifecycle_records[index].protected_symbol=clean_symbol;
         m_lifecycle_records[index].first_hunter_symbol=hunter_symbol;
         m_lifecycle_records[index].trading_day_start_ny=time_snapshot.trading_day_start_ny;
         m_lifecycle_records[index].reference_cycle_start_ny=hunt.reference_cycle_start_ny;
         m_lifecycle_records[index].reference_cycle_end_ny=hunt.reference_cycle_end_ny;
         m_lifecycle_records[index].first_confirmation_time_ny=time_snapshot.new_york_now;
         m_lifecycle_records[index].last_allowed_confirmation_time_ny=time_snapshot.new_york_now;
         m_lifecycle_records[index].retirement_time_ny=0;
         m_lifecycle_records[index].retirement_reason="";
         lifecycle_note="protected_reference_lifecycle_started";
         return true;
      }

      if(m_lifecycle_records[index].protected_symbol==clean_symbol)
      {
         if(!m_config.allow_repeated_divergence_while_protected_survives)
         {
            lifecycle_note="suppressed_repeated_reference_signal_by_config";
            return false;
         }
         m_lifecycle_records[index].last_allowed_confirmation_time_ny=time_snapshot.new_york_now;
         lifecycle_note="repeated_divergence_allowed_while_same_protected_symbol_survives";
         return true;
      }

      // The protected side changed. Mechanically this means the symbol that was previously protected
      // is no longer protected relative to this reference side. Retire the whole reference-side key.
      RetireLifecycleRecordByIndex(index,time_snapshot.new_york_now,"protected_role_switched_reference_side_compromised");
      lifecycle_note="suppressed_reference_side_retired_after_protected_role_switch";
      return false;
   }

   void ResetSignal(SCGCFinalSignal &signal)
   {
      signal.signal_id="";
      signal.group_name="";
      signal.group_minutes=0;
      signal.current_cycle_index=-1;
      signal.current_cycle_number=0;
      signal.reference_cycle_index=-1;
      signal.reference_cycle_number=0;
      signal.trading_day_start_ny=0;
      signal.trading_day_end_ny=0;
      signal.current_cycle_start_ny=0;
      signal.current_cycle_end_ny=0;
      signal.reference_cycle_start_ny=0;
      signal.reference_cycle_end_ny=0;
      signal.confirmation_time_broker=0;
      signal.confirmation_time_utc=0;
      signal.confirmation_time_ny=0;
      signal.confirmation_timeframe=PERIOD_CURRENT;
      signal.confirmation_timeframe_seconds=0;
      signal.direction=CGC_DIRECTION_NONE;
      signal.side=CGC_SIDE_NONE;
      signal.status=CGC_STATUS_NONE;
      signal.hunter_symbol="";
      signal.clean_symbol="";
      signal.symbol_a_is_hunter=false;
      signal.symbol_b_is_hunter=false;
      signal.one_sided_hunt=false;
      signal.double_hunt_invalidated=false;
      signal.trade_permission_preview=false;
      signal.data_ready=false;
      signal.hunter_reference_price=0.0;
      signal.clean_reference_price=0.0;
      signal.hunter_current_extreme=0.0;
      signal.clean_current_extreme=0.0;
      signal.clean_stop_reference_price=0.0;
      signal.symbol_a_reference_price=0.0;
      signal.symbol_b_reference_price=0.0;
      signal.symbol_a_current_extreme=0.0;
      signal.symbol_b_current_extreme=0.0;
      signal.symbol_a_reference_frontier=false;
      signal.symbol_b_reference_frontier=false;
      signal.note="";
   }

   void ResetGroupState(SCGCGroupConfirmationState &state)
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
      state.final_state_count=0;
      state.confirmed_tradeable_count=0;
      state.invalidated_double_hunt_count=0;
      state.missing_data_count=0;
      state.buy_confirmed_count=0;
      state.sell_confirmed_count=0;
      state.symbol_a_clean_count=0;
      state.symbol_b_clean_count=0;
      state.high_side_final_count=0;
      state.low_side_final_count=0;
      state.has_any_final_state=false;
      state.has_confirmed_tradeable_signal=false;
      state.trading_day_start_ny=0;
      state.trading_day_end_ny=0;
      state.current_cycle_start_ny=0;
      state.current_cycle_end_ny=0;
      state.confirmation_time_broker=0;
      state.confirmation_time_ny=0;
   }

   string DirectionText(const ECGCSignalDirection direction)
   {
      if(direction==CGC_DIRECTION_BUY)
         return "BUY";
      if(direction==CGC_DIRECTION_SELL)
         return "SELL";
      return "NONE";
   }

   string SideText(const ECGCSignalSide side)
   {
      if(side==CGC_SIDE_HIGH)
         return "HIGH";
      if(side==CGC_SIDE_LOW)
         return "LOW";
      return "NONE";
   }

   string StatusText(const ECGCFinalStatus status)
   {
      if(status==CGC_STATUS_CONFIRMED_TRADEABLE)
         return "CONFIRMED_TRADEABLE";
      if(status==CGC_STATUS_INVALIDATED_DOUBLE_HUNT)
         return "INVALIDATED_DOUBLE_HUNT";
      if(status==CGC_STATUS_MISSING_DATA)
         return "MISSING_DATA";
      return "NONE";
   }


   void ResetFrontierEligibility(SCGCExtremeFrontierEligibility &e)
   {
      e.high_frontier_valid=false;
      e.low_frontier_valid=false;
      e.symbol_a_high_frontier=false;
      e.symbol_b_high_frontier=false;
      e.symbol_a_low_frontier=false;
      e.symbol_b_low_frontier=false;
      e.later_symbol_a_max_high=0.0;
      e.later_symbol_b_max_high=0.0;
      e.later_symbol_a_min_low=0.0;
      e.later_symbol_b_min_low=0.0;
      e.high_note="not_calculated";
      e.low_note="not_calculated";
   }

   string FrontierSuppressionText(const ECGCSignalSide side,const SCGCExtremeFrontierEligibility &e)
   {
      if(side==CGC_SIDE_HIGH)
      {
         return StringFormat("suppressed_non_frontier_high_reference|A_frontier:%s B_frontier:%s later_A_max:%s later_B_max:%s",
                             BoolText(e.symbol_a_high_frontier),
                             BoolText(e.symbol_b_high_frontier),
                             FormatPrice(e.later_symbol_a_max_high),
                             FormatPrice(e.later_symbol_b_max_high));
      }
      if(side==CGC_SIDE_LOW)
      {
         return StringFormat("suppressed_non_frontier_low_reference|A_frontier:%s B_frontier:%s later_A_min:%s later_B_min:%s",
                             BoolText(e.symbol_a_low_frontier),
                             BoolText(e.symbol_b_low_frontier),
                             FormatPrice(e.later_symbol_a_min_low),
                             FormatPrice(e.later_symbol_b_min_low));
      }
      return "suppressed_non_frontier_reference";
   }

   string BoolText(const bool value)
   {
      return value ? "true" : "false";
   }

   void BuildExtremeFrontierEligibility(SCGHReferenceHuntState &hunts[],SCGCExtremeFrontierEligibility &eligibility[])
   {
      int count=ArraySize(hunts);
      ArrayResize(eligibility,count);
      for(int i=0;i<count;i++)
         ResetFrontierEligibility(eligibility[i]);

      if(!m_config.enable_extreme_frontier_reference_filter)
      {
         for(int i=0;i<count;i++)
         {
            eligibility[i].high_frontier_valid=true;
            eligibility[i].low_frontier_valid=true;
            eligibility[i].symbol_a_high_frontier=true;
            eligibility[i].symbol_b_high_frontier=true;
            eligibility[i].symbol_a_low_frontier=true;
            eligibility[i].symbol_b_low_frontier=true;
            eligibility[i].high_note="extreme_frontier_filter_disabled";
            eligibility[i].low_note="extreme_frontier_filter_disabled";
         }
         return;
      }

      double later_a_max_high=-1.0e100;
      double later_b_max_high=-1.0e100;
      double later_a_min_low=1.0e100;
      double later_b_min_low=1.0e100;
      bool have_later_a_high=false;
      bool have_later_b_high=false;
      bool have_later_a_low=false;
      bool have_later_b_low=false;

      // References arrive oldest -> newest. To suppress stale internal levels, walk newest -> oldest.
      // A high is eligible only if no later completed cycle has already made an equal/higher high.
      // A low is eligible only if no later completed cycle has already made an equal/lower low.
      for(int i=count-1;i>=0;i--)
      {
         if(!hunts[i].reference_ready)
         {
            eligibility[i].high_note="reference_missing_no_frontier_classification";
            eligibility[i].low_note="reference_missing_no_frontier_classification";
            continue;
         }

         eligibility[i].later_symbol_a_max_high=(have_later_a_high ? later_a_max_high : 0.0);
         eligibility[i].later_symbol_b_max_high=(have_later_b_high ? later_b_max_high : 0.0);
         eligibility[i].later_symbol_a_min_low=(have_later_a_low ? later_a_min_low : 0.0);
         eligibility[i].later_symbol_b_min_low=(have_later_b_low ? later_b_min_low : 0.0);

         eligibility[i].symbol_a_high_frontier=(!have_later_a_high || hunts[i].symbol_a.reference_high>later_a_max_high);
         eligibility[i].symbol_b_high_frontier=(!have_later_b_high || hunts[i].symbol_b.reference_high>later_b_max_high);
         eligibility[i].symbol_a_low_frontier=(!have_later_a_low || hunts[i].symbol_a.reference_low<later_a_min_low);
         eligibility[i].symbol_b_low_frontier=(!have_later_b_low || hunts[i].symbol_b.reference_low<later_b_min_low);

         if(m_config.require_symbol_local_frontier_for_both_symbols)
         {
            eligibility[i].high_frontier_valid=(eligibility[i].symbol_a_high_frontier && eligibility[i].symbol_b_high_frontier);
            eligibility[i].low_frontier_valid=(eligibility[i].symbol_a_low_frontier && eligibility[i].symbol_b_low_frontier);
         }
         else
         {
            eligibility[i].high_frontier_valid=(eligibility[i].symbol_a_high_frontier || eligibility[i].symbol_b_high_frontier);
            eligibility[i].low_frontier_valid=(eligibility[i].symbol_a_low_frontier || eligibility[i].symbol_b_low_frontier);
         }

         eligibility[i].high_note=(eligibility[i].high_frontier_valid ? "high_reference_is_unbroken_extreme_frontier" : FrontierSuppressionText(CGC_SIDE_HIGH,eligibility[i]));
         eligibility[i].low_note=(eligibility[i].low_frontier_valid ? "low_reference_is_unbroken_extreme_frontier" : FrontierSuppressionText(CGC_SIDE_LOW,eligibility[i]));

         if(!have_later_a_high || hunts[i].symbol_a.reference_high>later_a_max_high)
            later_a_max_high=hunts[i].symbol_a.reference_high;
         if(!have_later_b_high || hunts[i].symbol_b.reference_high>later_b_max_high)
            later_b_max_high=hunts[i].symbol_b.reference_high;
         if(!have_later_a_low || hunts[i].symbol_a.reference_low<later_a_min_low)
            later_a_min_low=hunts[i].symbol_a.reference_low;
         if(!have_later_b_low || hunts[i].symbol_b.reference_low<later_b_min_low)
            later_b_min_low=hunts[i].symbol_b.reference_low;

         have_later_a_high=true;
         have_later_b_high=true;
         have_later_a_low=true;
         have_later_b_low=true;
      }
   }

   string BuildSignalId(SCGTTimeSnapshot &time_snapshot,SCGHReferenceHuntState &hunt,const ECGCSignalDirection direction,const ECGCSignalSide side,const ECGCFinalStatus status,const string hunter_symbol,const string clean_symbol)
   {
      return StringFormat("EXP0017|PH05|%s|TD%s|C%d|R%d|%s|%s|%s|H:%s|C:%s",
                          hunt.group_name,
                          TimeToString(time_snapshot.trading_day_start_ny,TIME_DATE),
                          hunt.current_cycle_start_ny,
                          hunt.reference_cycle_start_ny,
                          DirectionText(direction),
                          SideText(side),
                          StatusText(status),
                          hunter_symbol,
                          clean_symbol);
   }

   void FillSharedFields(SCGTTimeSnapshot &time_snapshot,SCGTCycleSnapshot &cycle,SCGHReferenceHuntState &hunt,SCGCFinalSignal &signal,const ECGCSignalDirection direction,const ECGCSignalSide side)
   {
      signal.group_name=hunt.group_name;
      signal.group_minutes=hunt.group_minutes;
      signal.current_cycle_index=cycle.current_cycle_index;
      signal.current_cycle_number=cycle.current_cycle_number;
      signal.reference_cycle_index=hunt.reference_cycle_index;
      signal.reference_cycle_number=hunt.reference_cycle_number;
      signal.trading_day_start_ny=time_snapshot.trading_day_start_ny;
      signal.trading_day_end_ny=time_snapshot.trading_day_end_ny;
      signal.current_cycle_start_ny=hunt.current_cycle_start_ny;
      signal.current_cycle_end_ny=hunt.current_cycle_end_ny;
      signal.reference_cycle_start_ny=hunt.reference_cycle_start_ny;
      signal.reference_cycle_end_ny=hunt.reference_cycle_end_ny;
      signal.confirmation_time_broker=time_snapshot.broker_now;
      signal.confirmation_time_utc=time_snapshot.utc_now;
      signal.confirmation_time_ny=time_snapshot.new_york_now;
      signal.confirmation_timeframe=m_config.confirmation_timeframe;
      signal.confirmation_timeframe_seconds=PeriodSeconds(m_config.confirmation_timeframe);
      signal.direction=direction;
      signal.side=side;
      signal.data_ready=(hunt.reference_ready && hunt.current_range_ready);
   }


   void FillSymbolLocalVisualFields(SCGHReferenceHuntState &hunt,SCGCFinalSignal &signal)
   {
      if(signal.side==CGC_SIDE_HIGH)
      {
         signal.symbol_a_reference_price=hunt.symbol_a.reference_high;
         signal.symbol_b_reference_price=hunt.symbol_b.reference_high;
         signal.symbol_a_current_extreme=hunt.symbol_a.current_high;
         signal.symbol_b_current_extreme=hunt.symbol_b.current_high;
      }
      else if(signal.side==CGC_SIDE_LOW)
      {
         signal.symbol_a_reference_price=hunt.symbol_a.reference_low;
         signal.symbol_b_reference_price=hunt.symbol_b.reference_low;
         signal.symbol_a_current_extreme=hunt.symbol_a.current_low;
         signal.symbol_b_current_extreme=hunt.symbol_b.current_low;
      }
   }

   void FillSymbolLocalFrontierFields(const SCGCExtremeFrontierEligibility &frontier,SCGCFinalSignal &signal)
   {
      signal.symbol_a_reference_frontier=false;
      signal.symbol_b_reference_frontier=false;

      if(signal.side==CGC_SIDE_HIGH)
      {
         signal.symbol_a_reference_frontier=frontier.symbol_a_high_frontier;
         signal.symbol_b_reference_frontier=frontier.symbol_b_high_frontier;
      }
      else if(signal.side==CGC_SIDE_LOW)
      {
         signal.symbol_a_reference_frontier=frontier.symbol_a_low_frontier;
         signal.symbol_b_reference_frontier=frontier.symbol_b_low_frontier;
      }
   }

   bool BuildConfirmedHighSignal(SCGTTimeSnapshot &time_snapshot,SCGTCycleSnapshot &cycle,SCGHReferenceHuntState &hunt,const SCGCExtremeFrontierEligibility &frontier,SCGCFinalSignal &signal)
   {
      ResetSignal(signal);
      FillSharedFields(time_snapshot,cycle,hunt,signal,CGC_DIRECTION_SELL,CGC_SIDE_HIGH);
      FillSymbolLocalVisualFields(hunt,signal);
      FillSymbolLocalFrontierFields(frontier,signal);

      if(!signal.data_ready)
      {
         signal.status=CGC_STATUS_MISSING_DATA;
         signal.note="missing_data_no_final_high_side_classification";
         return false;
      }

      if(m_config.enable_extreme_frontier_reference_filter && !frontier.high_frontier_valid)
      {
         signal.status=CGC_STATUS_NONE;
         signal.note=frontier.high_note;
         return !m_config.suppress_non_frontier_reference_signals;
      }

      string lifecycle_key=BuildReferenceLifecycleKey(time_snapshot,hunt,CGC_SIDE_HIGH);
      if(ReferenceLifecycleIsRetired(lifecycle_key))
      {
         signal.status=CGC_STATUS_NONE;
         signal.note="suppressed_high_side_reference_already_retired_after_protected_breach";
         return false;
      }

      if(hunt.symbol_a.high_hunted && hunt.symbol_b.high_hunted)
      {
         signal.status=CGC_STATUS_INVALIDATED_DOUBLE_HUNT;
         signal.double_hunt_invalidated=true;
         signal.trade_permission_preview=false;
         signal.hunter_symbol="BOTH_SYMBOLS";
         signal.clean_symbol="NONE";
         signal.hunter_reference_price=0.0;
         signal.clean_reference_price=0.0;
         signal.hunter_current_extreme=0.0;
         signal.clean_current_extreme=0.0;
         signal.clean_stop_reference_price=0.0;
         MarkProtectedBreachIfNeeded(time_snapshot,hunt,CGC_SIDE_HIGH);
         signal.signal_id=BuildSignalId(time_snapshot,hunt,signal.direction,signal.side,signal.status,signal.hunter_symbol,signal.clean_symbol);
         signal.note="both_symbols_hunted_high_at_closed_candle_no_sell_permission_reference_side_retired_if_protected_was_active";
         return true;
      }

      if(hunt.symbol_a.high_hunted==hunt.symbol_b.high_hunted)
         return false;

      signal.status=CGC_STATUS_CONFIRMED_TRADEABLE;
      signal.one_sided_hunt=true;
      signal.trade_permission_preview=true;
      signal.symbol_a_is_hunter=hunt.symbol_a.high_hunted;
      signal.symbol_b_is_hunter=hunt.symbol_b.high_hunted;

      if(signal.symbol_a_is_hunter)
      {
         signal.hunter_symbol=m_config.symbol_a;
         signal.clean_symbol=m_config.symbol_b;
         signal.hunter_reference_price=hunt.symbol_a.reference_high;
         signal.clean_reference_price=hunt.symbol_b.reference_high;
         signal.hunter_current_extreme=hunt.symbol_a.current_high;
         signal.clean_current_extreme=hunt.symbol_b.current_high;
         signal.clean_stop_reference_price=hunt.symbol_b.reference_high;
      }
      else
      {
         signal.hunter_symbol=m_config.symbol_b;
         signal.clean_symbol=m_config.symbol_a;
         signal.hunter_reference_price=hunt.symbol_b.reference_high;
         signal.clean_reference_price=hunt.symbol_a.reference_high;
         signal.hunter_current_extreme=hunt.symbol_b.current_high;
         signal.clean_current_extreme=hunt.symbol_a.current_high;
         signal.clean_stop_reference_price=hunt.symbol_a.reference_high;
      }

      string lifecycle_note="";
      if(!ActivateOrAllowProtectedReference(time_snapshot,hunt,CGC_SIDE_HIGH,signal.hunter_symbol,signal.clean_symbol,lifecycle_note))
      {
         signal.status=CGC_STATUS_NONE;
         signal.note=lifecycle_note;
         return false;
      }

      signal.signal_id=BuildSignalId(time_snapshot,hunt,signal.direction,signal.side,signal.status,signal.hunter_symbol,signal.clean_symbol);
      signal.note="closed_candle_one_sided_high_hunt_sell_confirmed_tradeable_preview_clean_symbol_only_no_order_yet|"+lifecycle_note;
      return true;
   }

   bool BuildConfirmedLowSignal(SCGTTimeSnapshot &time_snapshot,SCGTCycleSnapshot &cycle,SCGHReferenceHuntState &hunt,const SCGCExtremeFrontierEligibility &frontier,SCGCFinalSignal &signal)
   {
      ResetSignal(signal);
      FillSharedFields(time_snapshot,cycle,hunt,signal,CGC_DIRECTION_BUY,CGC_SIDE_LOW);
      FillSymbolLocalVisualFields(hunt,signal);
      FillSymbolLocalFrontierFields(frontier,signal);

      if(!signal.data_ready)
      {
         signal.status=CGC_STATUS_MISSING_DATA;
         signal.note="missing_data_no_final_low_side_classification";
         return false;
      }

      if(m_config.enable_extreme_frontier_reference_filter && !frontier.low_frontier_valid)
      {
         signal.status=CGC_STATUS_NONE;
         signal.note=frontier.low_note;
         return !m_config.suppress_non_frontier_reference_signals;
      }

      string lifecycle_key=BuildReferenceLifecycleKey(time_snapshot,hunt,CGC_SIDE_LOW);
      if(ReferenceLifecycleIsRetired(lifecycle_key))
      {
         signal.status=CGC_STATUS_NONE;
         signal.note="suppressed_low_side_reference_already_retired_after_protected_breach";
         return false;
      }

      if(hunt.symbol_a.low_hunted && hunt.symbol_b.low_hunted)
      {
         signal.status=CGC_STATUS_INVALIDATED_DOUBLE_HUNT;
         signal.double_hunt_invalidated=true;
         signal.trade_permission_preview=false;
         signal.hunter_symbol="BOTH_SYMBOLS";
         signal.clean_symbol="NONE";
         MarkProtectedBreachIfNeeded(time_snapshot,hunt,CGC_SIDE_LOW);
         signal.signal_id=BuildSignalId(time_snapshot,hunt,signal.direction,signal.side,signal.status,signal.hunter_symbol,signal.clean_symbol);
         signal.note="both_symbols_hunted_low_at_closed_candle_no_buy_permission_reference_side_retired_if_protected_was_active";
         return true;
      }

      if(hunt.symbol_a.low_hunted==hunt.symbol_b.low_hunted)
         return false;

      signal.status=CGC_STATUS_CONFIRMED_TRADEABLE;
      signal.one_sided_hunt=true;
      signal.trade_permission_preview=true;
      signal.symbol_a_is_hunter=hunt.symbol_a.low_hunted;
      signal.symbol_b_is_hunter=hunt.symbol_b.low_hunted;

      if(signal.symbol_a_is_hunter)
      {
         signal.hunter_symbol=m_config.symbol_a;
         signal.clean_symbol=m_config.symbol_b;
         signal.hunter_reference_price=hunt.symbol_a.reference_low;
         signal.clean_reference_price=hunt.symbol_b.reference_low;
         signal.hunter_current_extreme=hunt.symbol_a.current_low;
         signal.clean_current_extreme=hunt.symbol_b.current_low;
         signal.clean_stop_reference_price=hunt.symbol_b.reference_low;
      }
      else
      {
         signal.hunter_symbol=m_config.symbol_b;
         signal.clean_symbol=m_config.symbol_a;
         signal.hunter_reference_price=hunt.symbol_b.reference_low;
         signal.clean_reference_price=hunt.symbol_a.reference_low;
         signal.hunter_current_extreme=hunt.symbol_b.current_low;
         signal.clean_current_extreme=hunt.symbol_a.current_low;
         signal.clean_stop_reference_price=hunt.symbol_a.reference_low;
      }

      string lifecycle_note="";
      if(!ActivateOrAllowProtectedReference(time_snapshot,hunt,CGC_SIDE_LOW,signal.hunter_symbol,signal.clean_symbol,lifecycle_note))
      {
         signal.status=CGC_STATUS_NONE;
         signal.note=lifecycle_note;
         return false;
      }

      signal.signal_id=BuildSignalId(time_snapshot,hunt,signal.direction,signal.side,signal.status,signal.hunter_symbol,signal.clean_symbol);
      signal.note="closed_candle_one_sided_low_hunt_buy_confirmed_tradeable_preview_clean_symbol_only_no_order_yet|"+lifecycle_note;
      return true;
   }

   void CountSignal(SCGCFinalSignal &signal,SCGCGroupConfirmationState &state)
   {
      if(signal.status==CGC_STATUS_NONE)
         return;

      state.final_state_count++;
      state.has_any_final_state=true;

      if(signal.status==CGC_STATUS_CONFIRMED_TRADEABLE)
      {
         state.confirmed_tradeable_count++;
         state.has_confirmed_tradeable_signal=true;
         if(signal.direction==CGC_DIRECTION_BUY)
            state.buy_confirmed_count++;
         if(signal.direction==CGC_DIRECTION_SELL)
            state.sell_confirmed_count++;
         if(signal.clean_symbol==m_config.symbol_a)
            state.symbol_a_clean_count++;
         if(signal.clean_symbol==m_config.symbol_b)
            state.symbol_b_clean_count++;
      }
      else if(signal.status==CGC_STATUS_INVALIDATED_DOUBLE_HUNT)
      {
         state.invalidated_double_hunt_count++;
      }
      else if(signal.status==CGC_STATUS_MISSING_DATA)
      {
         state.missing_data_count++;
      }

      if(signal.side==CGC_SIDE_HIGH)
         state.high_side_final_count++;
      if(signal.side==CGC_SIDE_LOW)
         state.low_side_final_count++;
   }

public:
   void Configure(SCGCConfirmationConfig &config)
   {
      m_config=config;
      ResetLifecycleRecords();
      if(m_config.max_groups_shown<1)
         m_config.max_groups_shown=1;
      if(m_config.max_signals_per_group_shown<0)
         m_config.max_signals_per_group_shown=0;
      if(m_config.confirmation_timeframe==PERIOD_CURRENT)
         m_config.confirmation_timeframe=(ENUM_TIMEFRAMES)_Period;
      if(m_config.max_protected_reference_records<1)
         m_config.max_protected_reference_records=2048;
      if(!m_config.enable_extreme_frontier_reference_filter)
         m_config.suppress_non_frontier_reference_signals=false;

      m_hunt_config.symbol_a=m_config.symbol_a;
      m_hunt_config.symbol_b=m_config.symbol_b;
      m_hunt_config.broker_utc_offset_hours=m_config.broker_utc_offset_hours;
      m_hunt_config.max_groups_shown=m_config.max_groups_shown;
      m_hunt_config.max_hunts_per_group_shown=m_config.max_signals_per_group_shown;
      m_hunt_config.require_m1_history=m_config.require_m1_history;
      m_hunt_config.show_only_groups_with_hunts=false;
      m_hunt_config.show_reference_prices=m_config.show_prices;
      m_hunt_config.show_current_cycle_ranges=m_config.show_prices;
      m_hunt_field.Configure(m_hunt_config);
   }

   int BuildFinalSignalsForGroup(SCGTTimeSnapshot &time_snapshot,SCGTCycleSnapshot &cycle,SCGCFinalSignal &signals[],SCGCGroupConfirmationState &state)
   {
      ArrayResize(signals,0);
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
      state.confirmation_time_broker=time_snapshot.broker_now;
      state.confirmation_time_ny=time_snapshot.new_york_now;

      EnsureLifecycleDay(time_snapshot);

      if(!cycle.enabled || !cycle.inside_trading_day || cycle.previous_cycle_count<=0)
         return 0;

      SCGHReferenceHuntState hunts[];
      SCGHGroupHuntState hunt_state;
      int hunt_count=m_hunt_field.BuildHuntsForGroup(time_snapshot,cycle,hunts,hunt_state);
      state.raw_hunt_count=hunt_state.hunt_state_count;
      state.ready_reference_count=hunt_state.ready_reference_count;
      state.missing_reference_count=hunt_state.missing_reference_count;

      if(hunt_count<=0)
         return 0;

      SCGCExtremeFrontierEligibility frontier[];
      BuildExtremeFrontierEligibility(hunts,frontier);

      for(int i=0;i<hunt_count;i++)
      {
         SCGCFinalSignal high_signal;
         if(BuildConfirmedHighSignal(time_snapshot,cycle,hunts[i],frontier[i],high_signal))
         {
            if(high_signal.status==CGC_STATUS_CONFIRMED_TRADEABLE || m_config.show_invalidated_double_hunts)
            {
               int n=ArraySize(signals);
               ArrayResize(signals,n+1);
               signals[n]=high_signal;
               CountSignal(high_signal,state);
            }
         }

         SCGCFinalSignal low_signal;
         if(BuildConfirmedLowSignal(time_snapshot,cycle,hunts[i],frontier[i],low_signal))
         {
            if(low_signal.status==CGC_STATUS_CONFIRMED_TRADEABLE || m_config.show_invalidated_double_hunts)
            {
               int n=ArraySize(signals);
               ArrayResize(signals,n+1);
               signals[n]=low_signal;
               CountSignal(low_signal,state);
            }
         }
      }

      return ArraySize(signals);
   }

   string DirectionTextPublic(const ECGCSignalDirection direction) { return DirectionText(direction); }
   string SideTextPublic(const ECGCSignalSide side) { return SideText(side); }
   string StatusTextPublic(const ECGCFinalStatus status) { return StatusText(status); }

   string FormatPrice(const double price)
   {
      if(price==0.0)
         return "-";
      return DoubleToString(price,CGC_PRICE_DIGITS);
   }

   string FormatCycleRangeNY(const datetime start_ny,const datetime end_ny)
   {
      if(start_ny<=0 || end_ny<=0)
         return "-";
      return StringFormat("%s-%s NY",TimeToString(start_ny,TIME_MINUTES),TimeToString(end_ny-60,TIME_MINUTES));
   }
};

#endif
