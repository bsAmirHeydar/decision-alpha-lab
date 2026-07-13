#ifndef FP_I07_TIMEFRAME_RESOLVER_MQH
#define FP_I07_TIMEFRAME_RESOLVER_MQH
bool FP_I07_ResolveHostTimeframe(const ENUM_TIMEFRAMES requested, ENUM_TIMEFRAMES &resolved, int &seconds, string &reason)
{
   if(requested==PERIOD_CURRENT) { reason="FP_CRC_TIMEFRAME_NOT_RESOLVED"; return false; }
   seconds=PeriodSeconds(requested); if(seconds<=0 || (seconds%60)!=0) { reason="FP_CRC_TIMEFRAME_UNSUPPORTED"; return false; }
   resolved=requested; reason="FP_CRC_TIMEFRAME_RESOLVED"; return true;
}
#endif
