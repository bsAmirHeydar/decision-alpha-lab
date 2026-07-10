#ifndef __CGX_TARGET_MODEL_ATR_MQH__
#define __CGX_TARGET_MODEL_ATR_MQH__

#include <IntermarketDivergenceExecution/CG/Execution/CGX_StopModel.mqh>

class CCGX_TargetModelATR
{
private:
   bool CalculateWilderATR(const string symbol,const ENUM_TIMEFRAMES timeframe,const datetime confirmation_close,const int period,double &atr,string &reason)
   {
      atr=0.0;
      if(period<1)
      {
         reason="atr_period_less_than_one";
         return false;
      }

      int seconds=PeriodSeconds(timeframe);
      if(seconds<=0)
      {
         reason="atr_invalid_timeframe";
         return false;
      }
      datetime target_open=(datetime)(confirmation_close-seconds);
      int shift=iBarShift(symbol,timeframe,confirmation_close-1,false);
      if(shift<0)
      {
         reason="atr_target_bar_shift_not_found";
         return false;
      }

      int warmup=period*10;
      if(warmup<100) warmup=100;
      if(warmup>1000) warmup=1000;
      int requested=period+warmup+1;

      MqlRates rates[];
      ArraySetAsSeries(rates,false);
      int copied=CopyRates(symbol,timeframe,shift,requested,rates);
      if(copied<period+1)
      {
         reason="atr_insufficient_closed_history_"+IntegerToString(copied);
         return false;
      }
      if(rates[copied-1].time!=target_open)
      {
         reason="atr_target_bar_time_mismatch";
         return false;
      }

      int tr_count=0;
      double running=0.0;
      double value=0.0;
      for(int i=1;i<copied;i++)
      {
         double high_low=rates[i].high-rates[i].low;
         double high_prev=MathAbs(rates[i].high-rates[i-1].close);
         double low_prev=MathAbs(rates[i].low-rates[i-1].close);
         double tr=MathMax(high_low,MathMax(high_prev,low_prev));
         if(tr<=0.0)
            continue;

         tr_count++;
         if(tr_count<=period)
         {
            running+=tr;
            if(tr_count==period)
               value=running/period;
         }
         else
            value=((value*(period-1))+tr)/period;
      }

      if(tr_count<period || value<=0.0)
      {
         reason="atr_calculation_failed";
         return false;
      }

      atr=value;
      reason="ok";
      return true;
   }

public:
   bool Build(const SCGXExecutionConfig &config,
              const string symbol,
              const ENUM_TIMEFRAMES timeframe,
              const datetime confirmation_close,
              const ECGCSignalDirection direction,
              const double entry_price,
              double &atr_value,
              double &take_profit,
              string &reason)
   {
      atr_value=0.0;
      take_profit=0.0;
      if(config.atr_multiplier<=0.0)
      {
         reason="atr_multiplier_not_positive";
         return false;
      }
      if(!CalculateWilderATR(symbol,timeframe,confirmation_close,config.atr_period,atr_value,reason))
         return false;

      double distance=atr_value*config.atr_multiplier;
      if(direction==CGC_DIRECTION_BUY)
         take_profit=entry_price+distance;
      else if(direction==CGC_DIRECTION_SELL)
         take_profit=entry_price-distance;
      else
      {
         reason="invalid_direction_for_target";
         return false;
      }

      take_profit=CGX_NormalizePrice(symbol,take_profit);
      reason="ok";
      return true;
   }
};

#endif
