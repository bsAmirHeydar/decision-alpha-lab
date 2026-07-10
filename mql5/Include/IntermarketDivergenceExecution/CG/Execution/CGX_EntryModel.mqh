#ifndef __CGX_ENTRY_MODEL_MQH__
#define __CGX_ENTRY_MODEL_MQH__

#include <IntermarketDivergenceExecution/CG/Execution/CGX_ClosedCandle.mqh>

class CCGX_EntryModel
{
public:
   bool ResolveTradeSymbol(SCGCFinalSignal &signal,const ECGXTradeLeg leg,string &trade_symbol,string &reason)
   {
      trade_symbol=(leg==CGX_TRADE_PROTECTED_SYMBOL ? signal.clean_symbol : signal.hunter_symbol);
      if(trade_symbol=="" || trade_symbol=="NONE" || trade_symbol=="BOTH_SYMBOLS")
      {
         reason="invalid_trade_leg_symbol";
         return false;
      }
      if(!SymbolSelect(trade_symbol,true))
      {
         reason="trade_symbol_select_failed";
         return false;
      }
      reason="ok";
      return true;
   }

   bool BuildMarketEntry(const SCGXExecutionConfig &config,const string symbol,const ECGCSignalDirection direction,MqlTick &tick,double &entry_price,string &reason)
   {
      if(config.entry_model!=CGX_ENTRY_MARKET_ON_CLOSED_CANDLE)
      {
         reason="unsupported_entry_model";
         return false;
      }

      ZeroMemory(tick);
      if(!SymbolInfoTick(symbol,tick) || tick.bid<=0.0 || tick.ask<=0.0 || tick.ask<tick.bid)
      {
         reason="invalid_or_missing_market_tick";
         return false;
      }

      if(config.max_quote_age_seconds>0 && tick.time>0)
      {
         long age=(long)TimeCurrent()-(long)tick.time;
         if(age<0) age=-age;
         if(age>config.max_quote_age_seconds)
         {
            reason="secondary_symbol_quote_stale_age_"+IntegerToString((int)age);
            return false;
         }
      }

      double point=SymbolInfoDouble(symbol,SYMBOL_POINT);
      if(point<=0.0)
      {
         reason="invalid_symbol_point";
         return false;
      }
      double spread_points=(tick.ask-tick.bid)/point;
      if(config.max_spread_points>0.0 && spread_points>config.max_spread_points)
      {
         reason="spread_limit_exceeded";
         return false;
      }

      if(direction==CGC_DIRECTION_BUY)
         entry_price=tick.ask;
      else if(direction==CGC_DIRECTION_SELL)
         entry_price=tick.bid;
      else
      {
         reason="invalid_signal_direction";
         return false;
      }

      entry_price=CGX_NormalizePrice(symbol,entry_price);
      reason="ok";
      return true;
   }
};

#endif
