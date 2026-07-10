#ifndef __CGX_VOLUME_MODEL_MQH__
#define __CGX_VOLUME_MODEL_MQH__

#include <IntermarketDivergenceExecution/CG/Execution/CGX_TargetModel.mqh>

class CCGX_VolumeModel
{
private:
   bool LossPerLot(const string symbol,
                   const ECGCSignalDirection direction,
                   const double entry_price,
                   const double stop_loss,
                   double &loss_per_lot,
                   string &reason)
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

   bool BuildLargestRiskCappedVolume(const double risk_budget,
                                     const double risk_per_lot,
                                     const double min_volume,
                                     const double max_volume,
                                     const double step,
                                     double &volume,
                                     double &planned_loss,
                                     string &reason)
   {
      volume=0.0;
      planned_loss=0.0;
      if(risk_budget<=0.0 || risk_per_lot<=0.0)
      {
         reason="invalid_risk_budget_or_risk_per_lot";
         return false;
      }

      double raw_volume=risk_budget/risk_per_lot;
      if(raw_volume>max_volume)
         raw_volume=max_volume;
      volume=CGX_NormalizeVolumeDown(raw_volume,step);

      if(volume<min_volume)
      {
         reason="risk_capped_volume_below_broker_minimum";
         return false;
      }

      double tolerance=MathMax(0.0000001,risk_budget*0.000000001);
      planned_loss=risk_per_lot*volume;
      int guard=0;
      while(planned_loss>risk_budget+tolerance && volume>=min_volume && guard<8)
      {
         volume=CGX_NormalizeVolumeDown(volume-step,step);
         planned_loss=risk_per_lot*volume;
         guard++;
      }

      volume=NormalizeDouble(volume,CGX_VolumeDigits(step));
      if(volume<min_volume || volume>max_volume || volume<=0.0)
      {
         reason="normalized_risk_capped_volume_outside_broker_bounds";
         return false;
      }
      if(planned_loss>risk_budget+tolerance)
      {
         reason="planned_loss_exceeds_risk_budget";
         return false;
      }

      reason="ok";
      return true;
   }

public:
   bool Build(const SCGXExecutionConfig &config,
              const string symbol,
              const ECGCSignalDirection direction,
              const double entry_price,
              const double stop_loss,
              double &risk_budget_money,
              double &risk_per_lot,
              double &planned_loss_at_stop,
              double &volume,
              string &reason)
   {
      risk_budget_money=0.0;
      risk_per_lot=0.0;
      planned_loss_at_stop=0.0;
      volume=0.0;

      double min_volume=SymbolInfoDouble(symbol,SYMBOL_VOLUME_MIN);
      double max_volume=SymbolInfoDouble(symbol,SYMBOL_VOLUME_MAX);
      double step=SymbolInfoDouble(symbol,SYMBOL_VOLUME_STEP);
      if(min_volume<=0.0 || max_volume<=0.0 || step<=0.0 || max_volume<min_volume)
      {
         reason="invalid_broker_volume_specification";
         return false;
      }

      string risk_reason="";
      if(!LossPerLot(symbol,direction,entry_price,stop_loss,risk_per_lot,risk_reason))
      {
         reason=risk_reason;
         return false;
      }

      if(config.volume_model==CGX_VOLUME_FIXED_RISK_MONEY)
      {
         if(config.fixed_risk_money<=0.0)
         {
            reason="fixed_risk_money_not_positive";
            return false;
         }
         risk_budget_money=config.fixed_risk_money;
         return BuildLargestRiskCappedVolume(risk_budget_money,risk_per_lot,min_volume,max_volume,step,volume,planned_loss_at_stop,reason);
      }

      if(config.volume_model==CGX_VOLUME_RISK_PERCENT_EQUITY)
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
         risk_budget_money=equity*config.risk_percent_equity/100.0;
         if(BuildLargestRiskCappedVolume(risk_budget_money,risk_per_lot,min_volume,max_volume,step,volume,planned_loss_at_stop,reason))
            return true;

         if(reason=="risk_capped_volume_below_broker_minimum" && config.allow_minimum_volume_risk_overflow)
         {
            volume=min_volume;
            planned_loss_at_stop=risk_per_lot*volume;
            reason="ok_minimum_volume_risk_overflow_allowed";
            return true;
         }
         return false;
      }

      if(config.volume_model==CGX_VOLUME_FIXED_LOTS)
      {
         if(config.fixed_lots<=0.0)
         {
            reason="fixed_lots_not_positive";
            return false;
         }
         double requested=MathMin(config.fixed_lots,max_volume);
         volume=CGX_NormalizeVolumeDown(requested,step);
         if(volume<min_volume)
            volume=min_volume;
         volume=NormalizeDouble(volume,CGX_VolumeDigits(step));
         if(volume<min_volume || volume>max_volume || volume<=0.0)
         {
            reason="normalized_fixed_volume_outside_broker_bounds";
            return false;
         }
         planned_loss_at_stop=risk_per_lot*volume;
         risk_budget_money=planned_loss_at_stop;
         reason="ok";
         return true;
      }

      reason="unsupported_volume_model";
      return false;
   }
};

#endif
