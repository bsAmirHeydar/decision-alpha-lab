#ifndef __SF17_QUOTE_OBSERVATION_MQH__
#define __SF17_QUOTE_OBSERVATION_MQH__
#include "../Contracts/SF01_AllContracts.mqh"
struct SF17_QuoteObservation{string symbol;double bid;double ask;long time_utc_msc;long sequence;string source;};
bool SF17_ValidateQuote(const SF17_QuoteObservation &q,string &error)
{
   if(!SF01_IsTerminalSymbol(q.symbol)||!SF01_IsSafeIdentifier(q.source,128)){error="invalid quote identity";return false;}
   if(!MathIsValidNumber(q.bid)||!MathIsValidNumber(q.ask)||q.bid<=0.0||q.ask<=0.0||q.ask<q.bid){error="invalid quote prices";return false;}
   if(q.time_utc_msc<=0||q.sequence<0){error="invalid quote time";return false;} error="";return true;
}
#endif
