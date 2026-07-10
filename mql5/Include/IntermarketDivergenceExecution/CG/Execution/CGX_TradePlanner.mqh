#ifndef __CGX_TRADE_PLANNER_MQH__
#define __CGX_TRADE_PLANNER_MQH__

#include <IntermarketDivergenceExecution/CG/Execution/CGX_VolumeModel.mqh>

class CCGX_TradePlanner
{
private:
   SCGXExecutionConfig       m_config;
   CCGX_ClosedCandleProvider m_candle_provider;
   CCGX_EntryModel           m_entry_model;
   CCGX_StopModel            m_stop_model;
   CCGX_TargetModel          m_target_model;
   CCGX_VolumeModel          m_volume_model;

   void ResetPlan(SCGXTradePlan &plan)
   {
      plan.valid=false;
      plan.rejection_reason="";
      plan.signal_id="";
      plan.group_name="";
      plan.group_minutes=0;
      plan.group_index=-1;
      plan.direction=CGC_DIRECTION_NONE;
      plan.trade_leg=CGX_TRADE_PROTECTED_SYMBOL;
      plan.target_model=CGX_TARGET_ATR_MULTIPLE;
      plan.volume_model=CGX_VOLUME_FIXED_RISK_MONEY;
      plan.hunter_symbol="";
      plan.protected_symbol="";
      plan.trade_symbol="";
      plan.confirmation_time_broker=0;
      plan.confirmation_timeframe=PERIOD_CURRENT;
      plan.candle_open_time_broker=0;
      plan.candle_high=0.0;
      plan.candle_low=0.0;
      plan.candle_close=0.0;
      plan.quote_bid=0.0;
      plan.quote_ask=0.0;
      plan.spread_price=0.0;
      plan.spread_points=0.0;
      plan.planned_entry_price=0.0;
      plan.stop_loss=0.0;
      plan.stop_distance=0.0;
      plan.atr_value=0.0;
      plan.take_profit=0.0;
      plan.target_distance=0.0;
      plan.risk_budget_money=0.0;
      plan.risk_per_lot=0.0;
      plan.planned_loss_at_stop=0.0;
      plan.volume=0.0;
      plan.magic_number=0;
      plan.order_comment="";
   }

   bool ValidateBrokerGeometry(SCGXTradePlan &plan,string &reason)
   {
      double point=SymbolInfoDouble(plan.trade_symbol,SYMBOL_POINT);
      int stops_level=(int)SymbolInfoInteger(plan.trade_symbol,SYMBOL_TRADE_STOPS_LEVEL);
      double min_distance=MathMax(0.0,stops_level*point);
      if(point<=0.0)
      {
         reason="invalid_symbol_point_for_geometry";
         return false;
      }

      if(plan.direction==CGC_DIRECTION_BUY)
      {
         if(!(plan.stop_loss<plan.planned_entry_price && plan.take_profit>plan.planned_entry_price))
         {
            reason="invalid_buy_sl_tp_geometry";
            return false;
         }
         if((plan.planned_entry_price-plan.stop_loss)<min_distance || (plan.take_profit-plan.planned_entry_price)<min_distance)
         {
            reason="buy_sl_or_tp_inside_broker_stops_level";
            return false;
         }
      }
      else if(plan.direction==CGC_DIRECTION_SELL)
      {
         if(!(plan.stop_loss>plan.planned_entry_price && plan.take_profit<plan.planned_entry_price))
         {
            reason="invalid_sell_sl_tp_geometry";
            return false;
         }
         if((plan.stop_loss-plan.planned_entry_price)<min_distance || (plan.planned_entry_price-plan.take_profit)<min_distance)
         {
            reason="sell_sl_or_tp_inside_broker_stops_level";
            return false;
         }
      }
      else
      {
         reason="invalid_direction_for_geometry";
         return false;
      }
      reason="ok";
      return true;
   }

public:
   void Configure(const SCGXExecutionConfig &config)
   {
      m_config=config;
   }

   bool Build(SCGCFinalSignal &signal,const int group_index,SCGXTradePlan &plan)
   {
      ResetPlan(plan);
      plan.signal_id=signal.signal_id;
      plan.group_name=signal.group_name;
      plan.group_minutes=signal.group_minutes;
      plan.group_index=group_index;
      plan.direction=signal.direction;
      plan.trade_leg=m_config.trade_leg;
      plan.target_model=m_config.target_model;
      plan.volume_model=m_config.volume_model;
      plan.hunter_symbol=signal.hunter_symbol;
      plan.protected_symbol=signal.clean_symbol;
      plan.confirmation_time_broker=signal.confirmation_time_broker;
      plan.confirmation_timeframe=signal.confirmation_timeframe;
      plan.magic_number=m_config.magic_base+group_index;

      if(signal.status!=CGC_STATUS_CONFIRMED_TRADEABLE || !signal.trade_permission_preview || !signal.data_ready)
      {
         plan.rejection_reason="signal_not_confirmed_tradeable";
         return false;
      }
      if(signal.signal_id=="")
      {
         plan.rejection_reason="empty_signal_id";
         return false;
      }

      string reason="";
      if(!m_entry_model.ResolveTradeSymbol(signal,m_config.trade_leg,plan.trade_symbol,reason))
      {
         plan.rejection_reason=reason;
         return false;
      }

      SCGXClosedCandle candle;
      if(!m_candle_provider.Build(plan.trade_symbol,signal.confirmation_timeframe,signal.confirmation_time_broker,candle))
      {
         plan.rejection_reason=candle.error_text;
         return false;
      }
      plan.candle_open_time_broker=candle.open_time_broker;
      plan.candle_high=candle.high;
      plan.candle_low=candle.low;
      plan.candle_close=candle.close;

      MqlTick tick;
      if(!m_entry_model.BuildMarketEntry(m_config,plan.trade_symbol,signal.direction,tick,plan.planned_entry_price,reason))
      {
         plan.rejection_reason=reason;
         return false;
      }
      plan.quote_bid=tick.bid;
      plan.quote_ask=tick.ask;
      plan.spread_price=MathMax(0.0,tick.ask-tick.bid);
      double point=SymbolInfoDouble(plan.trade_symbol,SYMBOL_POINT);
      if(point>0.0)
         plan.spread_points=plan.spread_price/point;

      if(!m_stop_model.Build(m_config,candle,signal.direction,plan.planned_entry_price,plan.spread_price,plan.stop_loss,reason))
      {
         plan.rejection_reason=reason;
         return false;
      }
      plan.stop_distance=MathAbs(plan.planned_entry_price-plan.stop_loss);

      if(!m_target_model.Build(m_config,
                               plan.trade_symbol,
                               signal.confirmation_timeframe,
                               signal.confirmation_time_broker,
                               signal.direction,
                               plan.planned_entry_price,
                               plan.stop_loss,
                               plan.atr_value,
                               plan.take_profit,
                               reason))
      {
         plan.rejection_reason=reason;
         return false;
      }
      plan.target_distance=MathAbs(plan.take_profit-plan.planned_entry_price);

      if(!ValidateBrokerGeometry(plan,reason))
      {
         plan.rejection_reason=reason;
         return false;
      }
      if(!m_volume_model.Build(m_config,
                               plan.trade_symbol,
                               signal.direction,
                               plan.planned_entry_price,
                               plan.stop_loss,
                               plan.risk_budget_money,
                               plan.risk_per_lot,
                               plan.planned_loss_at_stop,
                               plan.volume,
                               reason))
      {
         plan.rejection_reason=reason;
         return false;
      }

      plan.order_comment=CGX_BuildOrderComment(plan);
      plan.valid=true;
      plan.rejection_reason="ok";
      return true;
   }
};

#endif
