#ifndef __CGO_OUTCOME_FIELD_MQH__
#define __CGO_OUTCOME_FIELD_MQH__

#include <IntermarketDivergenceExecution/CG/CGO_Types.mqh>

class CCGO_OutcomeField
{
private:
   SCGOOutcomeConfig m_config;

   string DirectionText(const ECGCSignalDirection direction)
   {
      if(direction==CGC_DIRECTION_BUY) return "BUY";
      if(direction==CGC_DIRECTION_SELL) return "SELL";
      return "NONE";
   }

   datetime NyToBroker(const datetime ny_time,SCGCFinalSignal &signal)
   {
      int diff=(int)(signal.confirmation_time_broker-signal.confirmation_time_ny);
      return ny_time+diff;
   }

   double SymbolPoint(const string symbol)
   {
      double point=SymbolInfoDouble(symbol,SYMBOL_POINT);
      if(point<=0.0) point=_Point;
      if(point<=0.0) point=0.01;
      return point;
   }

   double SignedPoints(const ECGCSignalDirection direction,const double entry,const double exit,const double point)
   {
      if(point<=0.0) return 0.0;
      if(direction==CGC_DIRECTION_BUY)
         return (exit-entry)/point;
      if(direction==CGC_DIRECTION_SELL)
         return (entry-exit)/point;
      return 0.0;
   }

   double PriceAtOrBefore(const string symbol,const ENUM_TIMEFRAMES tf,const datetime close_time_broker,const bool use_open_next_bar,bool &ok)
   {
      ok=false;
      datetime t=close_time_broker;
      if(t<=0) return 0.0;
      int seconds=PeriodSeconds(tf);
      if(seconds<=0) seconds=60;

      if(use_open_next_bar)
      {
         int shift_next=iBarShift(symbol,tf,t,false);
         if(shift_next>=0)
         {
            double open=iOpen(symbol,tf,shift_next);
            if(open>0.0){ ok=true; return open; }
         }
      }

      int shift=iBarShift(symbol,tf,t-1,false);
      if(shift<0) shift=iBarShift(symbol,tf,t,false);
      if(shift<0) return 0.0;
      double close=iClose(symbol,tf,shift);
      if(close<=0.0) return 0.0;
      ok=true;
      return close;
   }

   bool ScanWindow(const string symbol,const datetime from_broker,const datetime to_broker,MqlRates &rates[])
   {
      ArrayResize(rates,0);
      if(symbol=="" || from_broker<=0 || to_broker<=from_broker)
         return false;
      ENUM_TIMEFRAMES tf=m_config.execution_timeframe;
      if(tf==PERIOD_CURRENT) tf=PERIOD_M1;
      int copied=CopyRates(symbol,tf,from_broker,to_broker,rates);
      return copied>0;
   }

   bool WindowHighLow(const string symbol,const datetime from_broker,const datetime to_broker,double &highest,double &lowest,datetime &high_time,datetime &low_time)
   {
      highest=0.0; lowest=0.0; high_time=0; low_time=0;
      MqlRates rates[];
      if(!ScanWindow(symbol,from_broker,to_broker,rates))
         return false;
      int total=ArraySize(rates);
      if(total<=0) return false;
      highest=rates[0].high;
      lowest=rates[0].low;
      high_time=rates[0].time;
      low_time=rates[0].time;
      for(int i=1;i<total;i++)
      {
         if(rates[i].high>highest){ highest=rates[i].high; high_time=rates[i].time; }
         if(rates[i].low<lowest){ lowest=rates[i].low; low_time=rates[i].time; }
      }
      return true;
   }

   bool StopHitInWindow(const string symbol,const ECGCSignalDirection direction,const double stop_price,const datetime from_broker,const datetime to_broker,datetime &stop_time)
   {
      stop_time=0;
      if(stop_price<=0.0) return false;
      MqlRates rates[];
      if(!ScanWindow(symbol,from_broker,to_broker,rates))
         return false;
      int total=ArraySize(rates);
      for(int i=0;i<total;i++)
      {
         if(direction==CGC_DIRECTION_BUY && rates[i].low<=stop_price)
         {
            stop_time=rates[i].time;
            return true;
         }
         if(direction==CGC_DIRECTION_SELL && rates[i].high>=stop_price)
         {
            stop_time=rates[i].time;
            return true;
         }
      }
      return false;
   }

   bool FillWindowClose(const string symbol,const ECGCSignalDirection direction,const double entry,const double risk_points,const double point,const datetime target_broker,double &price,double &points,double &r)
   {
      bool ok=false;
      price=PriceAtOrBefore(symbol,m_config.execution_timeframe,target_broker,false,ok);
      if(!ok)
      {
         points=0.0; r=0.0; return false;
      }
      points=SignedPoints(direction,entry,price,point);
      r=(risk_points>0.0 ? points/risk_points : 0.0);
      return true;
   }

   string AvailabilityText(const ECGOOutcomeAvailability availability)
   {
      if(availability==CGO_OUTCOME_COMPLETE) return "COMPLETE";
      if(availability==CGO_OUTCOME_PENDING_FUTURE) return "PENDING_FUTURE";
      if(availability==CGO_OUTCOME_MISSING_DATA) return "MISSING_DATA";
      if(availability==CGO_OUTCOME_ZERO_RISK) return "ZERO_RISK";
      return "UNAVAILABLE";
   }

public:
   void Configure(SCGOOutcomeConfig &config)
   {
      m_config=config;
      if(m_config.execution_timeframe==PERIOD_CURRENT)
         m_config.execution_timeframe=PERIOD_M1;
      if(m_config.forward_cycles<0) m_config.forward_cycles=0;
      if(m_config.forward_cycles>3) m_config.forward_cycles=3;
      if(m_config.minimum_risk_points<=0.0) m_config.minimum_risk_points=0.1;
   }

   void ResetRow(SCGOOutcomeRow &row)
   {
      row.signal_id="";
      row.outcome_id="";
      row.group_name="";
      row.group_minutes=0;
      row.current_cycle_number=0;
      row.reference_cycle_number=0;
      row.trading_day_start_ny=0;
      row.trading_day_end_ny=0;
      row.confirmation_time_broker=0;
      row.confirmation_time_ny=0;
      row.entry_time_broker=0;
      row.entry_time_ny=0;
      row.clean_symbol="";
      row.hunter_symbol="";
      row.direction=CGC_DIRECTION_NONE;
      row.side=CGC_SIDE_NONE;
      row.entry_price=0.0;
      row.stop_price=0.0;
      row.stop_distance_price=0.0;
      row.stop_distance_points=0.0;
      row.point_size=0.0;
      row.tick_value=0.0;
      row.tick_size=0.0;
      row.data_ready=false;
      row.availability=CGO_OUTCOME_UNAVAILABLE;
      row.availability_note="";
      row.cycle_end_time_broker=0;
      row.cycle_end_price=0.0;
      row.cycle_end_points=0.0;
      row.cycle_end_r=0.0;
      row.cycle_end_stop_hit=false;
      row.plus1_time_broker=0; row.plus1_price=0.0; row.plus1_points=0.0; row.plus1_r=0.0;
      row.plus2_time_broker=0; row.plus2_price=0.0; row.plus2_points=0.0; row.plus2_r=0.0;
      row.plus3_time_broker=0; row.plus3_price=0.0; row.plus3_points=0.0; row.plus3_r=0.0;
      row.day_end_time_broker=0; row.day_end_price=0.0; row.day_end_points=0.0; row.day_end_r=0.0;
      row.mfe_price=0.0; row.mfe_points=0.0; row.mfe_r=0.0;
      row.mae_price=0.0; row.mae_points=0.0; row.mae_r=0.0;
      row.stop_hit_intraday=false; row.stop_hit_time_broker=0;
      row.daily_range_points=0.0;
      row.day_end_normalized_by_daily_range=0.0;
      row.mfe_normalized_by_daily_range=0.0;
      row.note="";
   }

   bool BuildOutcome(SCGCFinalSignal &signal,SCGOOutcomeRow &row)
   {
      ResetRow(row);
      row.signal_id=signal.signal_id;
      row.outcome_id=signal.signal_id+"|OUTCOME_V1";
      row.group_name=signal.group_name;
      row.group_minutes=signal.group_minutes;
      row.current_cycle_number=signal.current_cycle_number;
      row.reference_cycle_number=signal.reference_cycle_number;
      row.trading_day_start_ny=signal.trading_day_start_ny;
      row.trading_day_end_ny=signal.trading_day_end_ny;
      row.confirmation_time_broker=signal.confirmation_time_broker;
      row.confirmation_time_ny=signal.confirmation_time_ny;
      row.entry_time_broker=signal.confirmation_time_broker;
      row.entry_time_ny=signal.confirmation_time_ny;
      row.clean_symbol=signal.clean_symbol;
      row.hunter_symbol=signal.hunter_symbol;
      row.direction=signal.direction;
      row.side=signal.side;
      row.stop_price=signal.clean_stop_reference_price;
      row.point_size=SymbolPoint(row.clean_symbol);
      SymbolInfoDouble(row.clean_symbol,SYMBOL_TRADE_TICK_VALUE,row.tick_value);
      SymbolInfoDouble(row.clean_symbol,SYMBOL_TRADE_TICK_SIZE,row.tick_size);
      row.availability=CGO_OUTCOME_UNAVAILABLE;
      row.availability_note="not_processed";
      row.data_ready=false;

      if(signal.status!=CGC_STATUS_CONFIRMED_TRADEABLE || !signal.trade_permission_preview)
      {
         row.availability=CGO_OUTCOME_UNAVAILABLE;
         row.availability_note="not_confirmed_tradeable_signal";
         return false;
      }

      bool entry_ok=false;
      row.entry_price=PriceAtOrBefore(row.clean_symbol,signal.confirmation_timeframe,row.entry_time_broker,(m_config.entry_price_mode==CGO_ENTRY_NEXT_M1_OPEN),entry_ok);
      if(!entry_ok || row.entry_price<=0.0 || row.stop_price<=0.0)
      {
         row.availability=CGO_OUTCOME_MISSING_DATA;
         row.availability_note="missing_entry_or_stop_price";
         return true;
      }

      row.stop_distance_price=MathAbs(row.entry_price-row.stop_price);
      row.stop_distance_points=(row.point_size>0.0 ? row.stop_distance_price/row.point_size : 0.0);
      if(m_config.skip_zero_risk && row.stop_distance_points<m_config.minimum_risk_points)
      {
         row.availability=CGO_OUTCOME_ZERO_RISK;
         row.availability_note="zero_or_too_small_stop_distance";
         return true;
      }

      row.cycle_end_time_broker=NyToBroker(signal.current_cycle_end_ny,signal);
      row.plus1_time_broker=NyToBroker(signal.current_cycle_end_ny+(signal.group_minutes*60),signal);
      row.plus2_time_broker=NyToBroker(signal.current_cycle_end_ny+(signal.group_minutes*60*2),signal);
      row.plus3_time_broker=NyToBroker(signal.current_cycle_end_ny+(signal.group_minutes*60*3),signal);
      row.day_end_time_broker=NyToBroker(signal.trading_day_end_ny,signal);

      if(row.plus1_time_broker>row.day_end_time_broker) row.plus1_time_broker=row.day_end_time_broker;
      if(row.plus2_time_broker>row.day_end_time_broker) row.plus2_time_broker=row.day_end_time_broker;
      if(row.plus3_time_broker>row.day_end_time_broker) row.plus3_time_broker=row.day_end_time_broker;

      datetime now=TimeCurrent();
      if(m_config.require_complete_future_window && row.day_end_time_broker>now)
      {
         row.availability=CGO_OUTCOME_PENDING_FUTURE;
         row.availability_note="future_day_end_not_available_yet";
         return true;
      }

      bool any_window=false;
      bool window_ok=false;
      if(m_config.study_cycle_end)
      {
         window_ok=FillWindowClose(row.clean_symbol,row.direction,row.entry_price,row.stop_distance_points,row.point_size,row.cycle_end_time_broker,row.cycle_end_price,row.cycle_end_points,row.cycle_end_r);
         if(window_ok) any_window=true;
      }
      if(m_config.study_forward_cycles)
      {
         if(m_config.forward_cycles>=1)
         {
            window_ok=FillWindowClose(row.clean_symbol,row.direction,row.entry_price,row.stop_distance_points,row.point_size,row.plus1_time_broker,row.plus1_price,row.plus1_points,row.plus1_r);
            if(window_ok) any_window=true;
         }
         if(m_config.forward_cycles>=2)
         {
            window_ok=FillWindowClose(row.clean_symbol,row.direction,row.entry_price,row.stop_distance_points,row.point_size,row.plus2_time_broker,row.plus2_price,row.plus2_points,row.plus2_r);
            if(window_ok) any_window=true;
         }
         if(m_config.forward_cycles>=3)
         {
            window_ok=FillWindowClose(row.clean_symbol,row.direction,row.entry_price,row.stop_distance_points,row.point_size,row.plus3_time_broker,row.plus3_price,row.plus3_points,row.plus3_r);
            if(window_ok) any_window=true;
         }
      }
      if(m_config.study_day_end)
      {
         window_ok=FillWindowClose(row.clean_symbol,row.direction,row.entry_price,row.stop_distance_points,row.point_size,row.day_end_time_broker,row.day_end_price,row.day_end_points,row.day_end_r);
         if(window_ok) any_window=true;
      }

      datetime high_time=0,low_time=0;
      double highest=0.0,lowest=0.0;
      if(m_config.study_intraday_extremes && WindowHighLow(row.clean_symbol,row.entry_time_broker,row.day_end_time_broker,highest,lowest,high_time,low_time))
      {
         if(row.direction==CGC_DIRECTION_BUY)
         {
            row.mfe_price=highest;
            row.mae_price=lowest;
            row.mfe_points=(highest-row.entry_price)/row.point_size;
            row.mae_points=(row.entry_price-lowest)/row.point_size;
         }
         else if(row.direction==CGC_DIRECTION_SELL)
         {
            row.mfe_price=lowest;
            row.mae_price=highest;
            row.mfe_points=(row.entry_price-lowest)/row.point_size;
            row.mae_points=(highest-row.entry_price)/row.point_size;
         }
         row.mfe_r=(row.stop_distance_points>0.0 ? row.mfe_points/row.stop_distance_points : 0.0);
         row.mae_r=(row.stop_distance_points>0.0 ? row.mae_points/row.stop_distance_points : 0.0);
      }

      if(m_config.detect_stop_before_window_close)
         row.stop_hit_intraday=StopHitInWindow(row.clean_symbol,row.direction,row.stop_price,row.entry_time_broker,row.day_end_time_broker,row.stop_hit_time_broker);

      if(m_config.use_clean_symbol_daily_range_for_normalization)
      {
         double day_high=0.0,day_low=0.0; datetime day_high_time=0,day_low_time=0;
         if(WindowHighLow(row.clean_symbol,NyToBroker(signal.trading_day_start_ny,signal),row.day_end_time_broker,day_high,day_low,day_high_time,day_low_time))
         {
            row.daily_range_points=(row.point_size>0.0 ? MathAbs(day_high-day_low)/row.point_size : 0.0);
            if(row.daily_range_points>0.0)
            {
               row.day_end_normalized_by_daily_range=row.day_end_points/row.daily_range_points;
               row.mfe_normalized_by_daily_range=row.mfe_points/row.daily_range_points;
            }
         }
      }

      row.cycle_end_stop_hit=StopHitInWindow(row.clean_symbol,row.direction,row.stop_price,row.entry_time_broker,row.cycle_end_time_broker,row.stop_hit_time_broker);
      row.data_ready=any_window;
      row.availability=(any_window ? CGO_OUTCOME_COMPLETE : CGO_OUTCOME_MISSING_DATA);
      row.availability_note=(any_window ? "complete_outcome_windows_studied" : "missing_outcome_window_prices");
      row.note="study_only_no_order_entry_is_research_estimate|availability="+AvailabilityText(row.availability);
      return true;
   }
};

#endif
