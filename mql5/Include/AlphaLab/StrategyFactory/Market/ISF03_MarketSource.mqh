#ifndef __ISF03_MARKET_SOURCE_MQH__
#define __ISF03_MARKET_SOURCE_MQH__
#include "SF03_MarketTypes.mqh"
class ISF03MarketSource
{
public:
   virtual string SourceId(void) const=0;
   virtual bool EnsureSymbol(const string symbol,string &error)=0;
   virtual bool ReadLatestTick(const string symbol,MqlTick &tick,string &error)=0;
   virtual int ReadClosedBars(const string symbol,const int timeframe_seconds,const int requested,
                              SF01_BarRecord &bars[],string &error)=0;
   virtual bool ReadSymbolSpec(const string symbol,SF03_SymbolSpecSnapshot &spec,string &error)=0;
};
#endif
