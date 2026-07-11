#ifndef __SF18_QUOTE_SNAPSHOT_MQH__
#define __SF18_QUOTE_SNAPSHOT_MQH__
#include "SF18_AccountGuardSnapshot.mqh"
struct SF18_QuoteSnapshot{string symbol;double bid,ask,point;long time_utc_msc,sequence;};
bool SF18_ReadQuoteSnapshot(const string symbol,const long sequence,SF18_QuoteSnapshot &q,string &error)
{
 MqlTick tick;if(!SymbolInfoTick(symbol,tick)){error="SymbolInfoTick failed:"+IntegerToString(GetLastError());return false;}
 q.symbol=symbol;q.bid=tick.bid;q.ask=tick.ask;q.point=SymbolInfoDouble(symbol,SYMBOL_POINT);q.time_utc_msc=(long)tick.time_msc;q.sequence=sequence;
 if(!SF01_IsTerminalSymbol(q.symbol)||q.bid<=0.0||q.ask<q.bid||q.point<=0.0||q.time_utc_msc<=0){error="invalid quote snapshot";return false;}error="";return true;
}
double SF18_SpreadPoints(const SF18_QuoteSnapshot &q){return (q.ask-q.bid)/q.point;}
#endif
