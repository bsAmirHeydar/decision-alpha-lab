#ifndef __SF03_FIXTURE_MARKET_SOURCE_MQH__
#define __SF03_FIXTURE_MARKET_SOURCE_MQH__

#include "../Market/ISF03_MarketSource.mqh"
#include "../Market/SF03_TimeKernel.mqh"

class CSF03FixtureMarketSource : public ISF03MarketSource
{
private:
   string m_symbols[];
   MqlTick m_ticks[];
   bool m_has_ticks[];
   SF03_SymbolSpecSnapshot m_specs[];
   bool m_has_specs[];
   SF01_BarRecord m_bars[];

   int Find(const string symbol) const
   {
      for(int i=0;i<ArraySize(m_symbols);i++)
         if(m_symbols[i]==symbol) return i;
      return -1;
   }

   int EnsureState(const string symbol)
   {
      int index=Find(symbol);
      if(index>=0) return index;
      index=ArraySize(m_symbols);
      ArrayResize(m_symbols,index+1);
      ArrayResize(m_ticks,index+1);
      ArrayResize(m_has_ticks,index+1);
      ArrayResize(m_specs,index+1);
      ArrayResize(m_has_specs,index+1);
      m_symbols[index]=symbol;
      m_has_ticks[index]=false;
      m_has_specs[index]=false;
      return index;
   }

public:
   string SourceId(void) const { return "sf03.fixture_market_source"; }

   bool EnsureSymbol(const string symbol,string &error)
   {
      if(!SF01_IsSafeTerminalSymbol(symbol))
      { error="invalid fixture symbol"; return false; }
      EnsureState(symbol);
      error="";
      return true;
   }

   bool PutTick(const string symbol,const MqlTick &tick,string &error)
   {
      if(!EnsureSymbol(symbol,error)) return false;
      const int index=Find(symbol);
      m_ticks[index]=tick;
      m_has_ticks[index]=true;
      error="";
      return true;
   }

   bool PutBar(const SF01_BarRecord &bar,string &error)
   {
      if(!EnsureSymbol(bar.symbol,error)) return false;
      if(!SF01_ValidateBarRecord(bar,error)) return false;
      const int n=ArraySize(m_bars);
      ArrayResize(m_bars,n+1);
      m_bars[n]=bar;
      error="";
      return true;
   }

   bool PutSpec(const SF03_SymbolSpecSnapshot &spec,string &error)
   {
      if(!EnsureSymbol(spec.symbol,error)) return false;
      const int index=Find(spec.symbol);
      m_specs[index]=spec;
      m_has_specs[index]=true;
      error="";
      return true;
   }

   bool ReadLatestTick(const string symbol,MqlTick &tick,string &error)
   {
      const int index=Find(symbol);
      if(index<0 || !m_has_ticks[index])
      { error="fixture tick unavailable"; return false; }
      tick=m_ticks[index];
      error="";
      return true;
   }

   int ReadClosedBars(const string symbol,const int timeframe_seconds,const int requested,
                      SF01_BarRecord &bars[],string &error)
   {
      int matches=0;
      for(int i=0;i<ArraySize(m_bars);i++)
         if(m_bars[i].symbol==symbol && m_bars[i].timeframe_seconds==timeframe_seconds)
            matches++;
      int take=requested;
      if(take<0) take=0;
      if(take>matches) take=matches;
      ArrayResize(bars,take);
      const int skip=matches-take;
      int seen=0;
      int written=0;
      for(int i=0;i<ArraySize(m_bars);i++)
      {
         if(m_bars[i].symbol!=symbol || m_bars[i].timeframe_seconds!=timeframe_seconds)
            continue;
         if(seen<skip){ seen++; continue; }
         bars[written++]=m_bars[i];
      }
      error="";
      return written;
   }

   bool ReadSymbolSpec(const string symbol,SF03_SymbolSpecSnapshot &spec,string &error)
   {
      const int index=Find(symbol);
      if(index<0 || !m_has_specs[index])
      { error="fixture specification unavailable"; return false; }
      spec=m_specs[index];
      error="";
      return true;
   }
};

SF01_BarRecord SF03_MakeFixtureBar(const string symbol,
                                   const int timeframe_seconds,
                                   const long open_utc_msc,
                                   const double open_price,
                                   const double high_price,
                                   const double low_price,
                                   const double close_price,
                                   const long tick_volume=100)
{
   SF01_BarRecord bar;
   bar.schema=SF01_BarRecordSchema();
   bar.symbol=symbol;
   bar.timeframe_seconds=timeframe_seconds;
   bar.open_time=SF01_MakeUtcMilliseconds(open_utc_msc,"UTC",0,"fixture",SF01_TIME_MILLISECONDS);
   bar.close_time=SF01_MakeUtcMilliseconds(
      open_utc_msc+((long)timeframe_seconds*1000L),
      "UTC",0,"fixture",SF01_TIME_MILLISECONDS
   );
   bar.open_price=open_price;
   bar.high_price=high_price;
   bar.low_price=low_price;
   bar.close_price=close_price;
   bar.tick_volume=tick_volume;
   bar.real_volume=0;
   bar.bid_close=close_price;
   bar.ask_close=close_price+0.25;
   bar.spread_points=1;
   bar.source_id="sf03.fixture_market_source";
   bar.source_bar_id=SF01_StableId(
      "srcbar",
      symbol+"|"+IntegerToString(timeframe_seconds)+"|"+IntegerToString(open_utc_msc)
   );
   return bar;
}

SF03_SymbolSpecSnapshot SF03_MakeFixtureSpec(const string symbol,
                                             const long observed_at_utc_msc)
{
   SF03_SymbolSpecSnapshot spec;
   spec.symbol=symbol;
   spec.digits=2;
   spec.point=0.01;
   spec.tick_size=0.25;
   spec.tick_value=5.0;
   spec.contract_size=1.0;
   spec.volume_min=0.01;
   spec.volume_max=100.0;
   spec.volume_step=0.01;
   spec.stops_level_points=0;
   spec.freeze_level_points=0;
   spec.filling_mode=0;
   spec.order_mode=0;
   spec.trade_mode=0;
   spec.specification_generation=1;
   spec.observed_at_utc_msc=observed_at_utc_msc;
   spec.quality=SF03_QUALITY_VALID;
   return spec;
}

#endif
