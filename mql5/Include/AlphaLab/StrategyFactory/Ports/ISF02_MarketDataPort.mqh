#ifndef __ISF02_MARKET_DATA_PORT_MQH__
#define __ISF02_MARKET_DATA_PORT_MQH__

#include "ISF02_LifecycleService.mqh"
#include "../Contracts/SF01_BarRecord.mqh"

class ISF02MarketDataPort : public ISF02LifecycleService
{
public:
   virtual bool EnsureSymbol(const string symbol, string &error) = 0;
   virtual bool LatestTick(const string symbol, MqlTick &tick, string &error) = 0;
   virtual bool LatestClosedBar(const string symbol,
                                const int timeframe_seconds,
                                SF01_BarRecord &bar,
                                string &error) = 0;
   virtual bool IsSynchronized(const string symbol,
                               const int timeframe_seconds) const = 0;
};

#endif
