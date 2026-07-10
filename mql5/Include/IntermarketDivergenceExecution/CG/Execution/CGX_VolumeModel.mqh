#ifndef __CGX_VOLUME_MODEL_MQH__
#define __CGX_VOLUME_MODEL_MQH__

#include <IntermarketDivergenceExecution/CG/Execution/CGX_TargetModelATR.mqh>

class CCGX_VolumeModel
{
private:
   bool LossPerLot(const string symbol,const ECGCSignalDirection direction,const double entry_price,const double stop_loss,double &loss_per_lot,string &reason)
   {
      loss_per_lot=0.0;
      ENUM_ORDER_TYPE order_type=(direction==CGC_DIRECTION_BUY ? ORDER_TYPE_BUY : ORDER_TYPE_SELL);
      double profit=0.0;
      if(OrderCalcProfit(order_type,symbol,1.0,entry_price,stop_loss,profit))
      {
         loss_per_lot=MathAbs(profit);
         if(loss_per_lot>0.0)
         {
            reason="ok_order_calc_profit";
            return true;
         }
      }

      double tick_size=SymbolInfoDouble(symbol,SYMBOL_TRADE_TICK_SIZE);
      double tick_value=SymbolInfoDouble(symbol,SYMBOL_TRADE_TICK_VALUE_LOSS);
      if(tick_value<=0.0)
         tick_value=SymbolInfoDouble(symbol,SYMBOL_TRADE_TICK_VALUE);
      double distance=MathAbs(entry_price-stop_loss);
      if(tick_size<=0.0 || tick_value<=0.0 || distance<=0.0)
      {
         reason="risk_per_lot_unavailable";
         return false;
      }

      loss_per_lot=(distance/tick_size)*tick_value;
      if(loss_per_lot<=0.0)
      {
         reason="risk_per_lot_non_positive";
         return false;
      }
      reason="ok_tick_value_fallback";
      return true;
   }

public:
   bool Build(const SCGXExecutionConfig &config,const string symbol,const ECGCSignalDirection direction,const double entry_price,const double stop_loss,double &risk_money,double &risk_per_lot,double &volume,string &reason)
   {
      risk_money=0.0;
      risk_per_lot=0.0;
      volume=0.0;

      double min_volume=SymbolInfoDouble(symbol,SYMBOL_VOLUME_MIN);
      double max_volume=SymbolInfoDouble(symbol,SYMBOL_VOLUME_MAX);
      double step=SymbolInfoDouble(symbol,SYMBOL_VOLUME_STEP);
      if(min_volume<=0.0 || max_volume<=0.0 || step<=0.0 || max_volume<min_volume)
      {
         reason="invalid_broker_volume_specification";
         return false;
      }

      double raw_volume=0.0;
      if(config.volume_model==CGX_VOLUME_FIXED_LOTS)
      {
         raw_volume=config.fixed_lots;
         if(raw_volume<=0.0)
         {
            reason="fixed_lots_not_positive";
            return false;
         }
      }
      else if(config.volume_model==CGX_VOLUME_RISK_PERCENT_EQUITY)
      {
         if(config.risk_percent_equity<=0.0)
         {
            reason="risk_percent_not_positive";
            return false;
         }
         double equity=AccountInfoDouble(ACCOUNT_EQUITY);
         if(equity<=0.0)
         {
            reason="account_equity_not_positive";
            return false;
         }
         risk_money=equity*config.risk_percent_equity/100.0;
         string risk_reason="";
         if(!LossPerLot(symbol,direction,entry_price,stop_loss,risk_per_lot,risk_reason))
         {
            reason=risk_reason;
            return false;
         }
         raw_volume=risk_money/risk_per_lot;
      }
      else
      {
         reason="unsupported_volume_model";
         return false;
      }

      if(raw_volume>max_volume)
         raw_volume=max_volume;
      volume=CGX_NormalizeVolumeDown(raw_volume,step);
      if(volume<min_volume)
      {
         if(config.volume_model==CGX_VOLUME_RISK_PERCENT_EQUITY && !config.allow_minimum_volume_risk_overflow)
         {
            reason="risk_sized_volume_below_broker_minimum";
            return false;
         }
         volume=min_volume;
      }
      volume=NormalizeDouble(volume,CGX_VolumeDigits(step));
      if(volume<min_volume || volume>max_volume || volume<=0.0)
      {
         reason="normalized_volume_outside_broker_bounds";
         return false;
      }

      reason="ok";
      return true;
   }
};

#endif
