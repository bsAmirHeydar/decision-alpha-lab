#ifndef __SF03_MARKET_VERSION_MQH__
#define __SF03_MARKET_VERSION_MQH__
#define SF03_MARKET_MAJOR 1
#define SF03_MARKET_MINOR 0
#define SF03_MARKET_PATCH 0
string SF03_MarketVersion()
{
   return IntegerToString(SF03_MARKET_MAJOR)+"."+
          IntegerToString(SF03_MARKET_MINOR)+"."+
          IntegerToString(SF03_MARKET_PATCH);
}
#endif
