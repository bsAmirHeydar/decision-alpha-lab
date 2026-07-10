#ifndef __CGX_CLOSED_CANDLE_MQH__
#define __CGX_CLOSED_CANDLE_MQH__

#include <IntermarketDivergenceExecution/CG/Execution/CGX_Utilities.mqh>

class CCGX_ClosedCandleProvider
{
private:
   void Reset(SCGXClosedCandle &candle)
   {
      candle.ready=false;
      candle.symbol="";
      candle.timeframe=PERIOD_CURRENT;
      candle.open_time_broker=0;
      candle.close_time_broker=0;
      candle.open=0.0;
      candle.high=0.0;
      candle.low=0.0;
      candle.close=0.0;
      candle.tick_volume=0;
      candle.error_text="";
   }

public:
   bool Build(const string symbol,const ENUM_TIMEFRAMES timeframe,const datetime close_time_broker,SCGXClosedCandle &candle)
   {
      Reset(candle);
      candle.symbol=symbol;
      candle.timeframe=timeframe;
      candle.close_time_broker=close_time_broker;

      if(symbol=="" || close_time_broker<=0)
      {
         candle.error_text="invalid_symbol_or_close_time";
         return false;
      }
      if(!SymbolSelect(symbol,true))
      {
         candle.error_text="symbol_select_failed";
         return false;
      }

      int seconds=PeriodSeconds(timeframe);
      if(seconds<=0)
      {
         candle.error_text="invalid_confirmation_timeframe_seconds";
         return false;
      }

      datetime expected_open=(datetime)(close_time_broker-seconds);
      MqlRates rates[];
      ArraySetAsSeries(rates,false);
      int copied=CopyRates(symbol,timeframe,expected_open,close_time_broker-1,rates);
      if(copied!=1)
      {
         candle.error_text="confirmation_candle_copy_failed_or_ambiguous_"+IntegerToString(copied);
         return false;
      }
      if(rates[0].time!=expected_open)
      {
         candle.error_text="confirmation_candle_open_time_mismatch";
         return false;
      }
      if(rates[0].high<rates[0].low || rates[0].open<=0.0 || rates[0].close<=0.0)
      {
         candle.error_text="invalid_confirmation_candle_ohlc";
         return false;
      }

      candle.open_time_broker=rates[0].time;
      candle.open=rates[0].open;
      candle.high=rates[0].high;
      candle.low=rates[0].low;
      candle.close=rates[0].close;
      candle.tick_volume=rates[0].tick_volume;
      candle.ready=true;
      candle.error_text="ok";
      return true;
   }
};

#endif
