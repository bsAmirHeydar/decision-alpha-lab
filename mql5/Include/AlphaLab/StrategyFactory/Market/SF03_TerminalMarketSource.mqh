#ifndef __SF03_TERMINAL_MARKET_SOURCE_MQH__
#define __SF03_TERMINAL_MARKET_SOURCE_MQH__
#include "ISF03_MarketSource.mqh"
#include "SF03_TimeKernel.mqh"

class CSF03TerminalMarketSource : public ISF03MarketSource
{
private:
   CSF03TimeKernel *m_clock;

   ENUM_TIMEFRAMES ToTimeframe(const int seconds) const
   {
      if(seconds==60) return PERIOD_M1;
      if(seconds==120) return PERIOD_M2;
      if(seconds==180) return PERIOD_M3;
      if(seconds==240) return PERIOD_M4;
      if(seconds==300) return PERIOD_M5;
      if(seconds==360) return PERIOD_M6;
      if(seconds==600) return PERIOD_M10;
      if(seconds==720) return PERIOD_M12;
      if(seconds==900) return PERIOD_M15;
      if(seconds==1200) return PERIOD_M20;
      if(seconds==1800) return PERIOD_M30;
      if(seconds==3600) return PERIOD_H1;
      if(seconds==7200) return PERIOD_H2;
      if(seconds==10800) return PERIOD_H3;
      if(seconds==14400) return PERIOD_H4;
      if(seconds==21600) return PERIOD_H6;
      if(seconds==28800) return PERIOD_H8;
      if(seconds==43200) return PERIOD_H12;
      if(seconds==86400) return PERIOD_D1;
      if(seconds==604800) return PERIOD_W1;
      return PERIOD_CURRENT;
   }

public:
   CSF03TerminalMarketSource(void){ m_clock=NULL; }
   void BindClock(CSF03TimeKernel *value){ m_clock=value; }
   string SourceId(void) const { return "mt5_terminal"; }

   bool EnsureSymbol(const string symbol,string &error)
   {
      if(!SF01_IsSafeTerminalSymbol(symbol)){ error="invalid symbol"; return false; }
      if(!SymbolSelect(symbol,true)){ error="SymbolSelect failed"; return false; }
      error="";
      return true;
   }

   bool ReadLatestTick(const string symbol,MqlTick &tick,string &error)
   {
      if(!SymbolInfoTick(symbol,tick)){ error="SymbolInfoTick failed"; return false; }
      error="";
      return true;
   }

   int ReadClosedBars(const string symbol,const int timeframe_seconds,const int requested,
                      SF01_BarRecord &bars[],string &error)
   {
      ArrayResize(bars,0);
      if(CheckPointer(m_clock)==POINTER_INVALID){ error="clock not bound"; return 0; }
      const ENUM_TIMEFRAMES timeframe=ToTimeframe(timeframe_seconds);
      if(timeframe==PERIOD_CURRENT && timeframe_seconds!=PeriodSeconds(PERIOD_CURRENT))
      { error="unsupported timeframe"; return 0; }

      MqlRates rates[];
      ArraySetAsSeries(rates,true);
      const int copied=CopyRates(symbol,timeframe,1,requested,rates);
      if(copied<=0){ error="CopyRates returned no closed bars"; return 0; }
      ArrayResize(bars,copied);

      for(int i=0;i<copied;i++)
      {
         const MqlRates rate=rates[copied-1-i];
         const long open_utc=m_clock.ServerSecondsToUtcMilliseconds(rate.time);
         SF01_BarRecord bar;
         bar.schema=SF01_BarRecordSchema();
         bar.symbol=symbol;
         bar.timeframe_seconds=timeframe_seconds;
         bar.open_time=SF01_MakeUtcMilliseconds(open_utc,"UTC",0,"mt5_bar_open",SF01_TIME_SECONDS);
         bar.close_time=SF01_MakeUtcMilliseconds(open_utc+((long)timeframe_seconds*1000L),
                                                "UTC",0,"mt5_bar_close",SF01_TIME_SECONDS);
         bar.open_price=rate.open;
         bar.high_price=rate.high;
         bar.low_price=rate.low;
         bar.close_price=rate.close;
         bar.tick_volume=rate.tick_volume;
         bar.real_volume=rate.real_volume;
         bar.bid_close=rate.close;
         bar.ask_close=0.0;
         bar.spread_points=(double)rate.spread;
         bar.source_id=SourceId();
         bar.source_bar_id=SF01_StableId(
            "srcbar",
            symbol+"|"+IntegerToString(timeframe_seconds)+"|"+IntegerToString(open_utc)
         );
         bars[i]=bar;
      }
      error="";
      return copied;
   }

   bool ReadSymbolSpec(const string symbol,SF03_SymbolSpecSnapshot &spec,string &error)
   {
      if(!EnsureSymbol(symbol,error)) return false;
      spec.symbol=symbol;
      spec.digits=(int)SymbolInfoInteger(symbol,SYMBOL_DIGITS);
      spec.point=SymbolInfoDouble(symbol,SYMBOL_POINT);
      spec.tick_size=SymbolInfoDouble(symbol,SYMBOL_TRADE_TICK_SIZE);
      spec.tick_value=SymbolInfoDouble(symbol,SYMBOL_TRADE_TICK_VALUE);
      spec.contract_size=SymbolInfoDouble(symbol,SYMBOL_TRADE_CONTRACT_SIZE);
      spec.volume_min=SymbolInfoDouble(symbol,SYMBOL_VOLUME_MIN);
      spec.volume_max=SymbolInfoDouble(symbol,SYMBOL_VOLUME_MAX);
      spec.volume_step=SymbolInfoDouble(symbol,SYMBOL_VOLUME_STEP);
      spec.stops_level_points=(int)SymbolInfoInteger(symbol,SYMBOL_TRADE_STOPS_LEVEL);
      spec.freeze_level_points=(int)SymbolInfoInteger(symbol,SYMBOL_TRADE_FREEZE_LEVEL);
      spec.filling_mode=SymbolInfoInteger(symbol,SYMBOL_FILLING_MODE);
      spec.order_mode=SymbolInfoInteger(symbol,SYMBOL_ORDER_MODE);
      spec.trade_mode=SymbolInfoInteger(symbol,SYMBOL_TRADE_MODE);
      spec.specification_generation=0;
      spec.observed_at_utc_msc=(CheckPointer(m_clock)==POINTER_INVALID)?0:m_clock.UtcNowMilliseconds();
      spec.quality=SF03_QUALITY_VALID;
      if(spec.point<=0.0 || spec.tick_size<=0.0 || spec.volume_step<=0.0)
      { error="invalid symbol specification"; return false; }
      error="";
      return true;
   }
};
#endif
