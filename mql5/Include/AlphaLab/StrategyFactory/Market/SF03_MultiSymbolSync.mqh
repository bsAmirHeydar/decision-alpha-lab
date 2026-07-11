#ifndef __SF03_MULTI_SYMBOL_SYNC_MQH__
#define __SF03_MULTI_SYMBOL_SYNC_MQH__
#include "SF03_BarCache.mqh"

class CSF03MultiSymbolSynchronizer
{
private:
   SF03_SyncRequirement m_requirements[];
public:
   bool AddRequirement(const SF03_SyncRequirement &value,string &error)
   {
      if(!SF01_IsSafeTerminalSymbol(value.symbol)){ error="invalid sync symbol"; return false; }
      if(value.timeframe_seconds<=0 || value.max_close_skew_milliseconds<0 ||
         value.max_staleness_milliseconds<0)
      { error="invalid sync requirement"; return false; }
      const int n=ArraySize(m_requirements);
      ArrayResize(m_requirements,n+1);
      m_requirements[n]=value;
      error="";
      return true;
   }
   bool Evaluate(const CSF03BarCache &cache,const long now_utc_msc,SF03_SyncResult &result) const
   {
      result.status=SF03_SYNC_UNKNOWN;
      result.minimum_close_utc_msc=0;
      result.maximum_close_utc_msc=0;
      result.close_skew_milliseconds=0;
      result.ready_count=0;
      result.required_count=ArraySize(m_requirements);
      result.detail="";
      if(result.required_count<=0)
      { result.status=SF03_SYNC_FAILED; result.detail="no requirements"; return false; }

      bool any_gap=false;
      bool any_stale=false;
      long allowed_skew=0;
      for(int i=0;i<result.required_count;i++)
      {
         SF01_BarRecord bar;
         string error="";
         const SF03_SyncRequirement requirement=m_requirements[i];
         if(!cache.Latest(requirement.symbol,requirement.timeframe_seconds,bar,error))
         { result.status=SF03_SYNC_WAITING; result.detail="missing "+requirement.symbol; return false; }

         const long close_msc=bar.close_time.utc_epoch_milliseconds;
         if(result.ready_count==0)
         {
            result.minimum_close_utc_msc=close_msc;
            result.maximum_close_utc_msc=close_msc;
         }
         else
         {
            if(close_msc<result.minimum_close_utc_msc) result.minimum_close_utc_msc=close_msc;
            if(close_msc>result.maximum_close_utc_msc) result.maximum_close_utc_msc=close_msc;
         }
         result.ready_count++;
         if(cache.HasGap(requirement.symbol,requirement.timeframe_seconds)) any_gap=true;
         if(now_utc_msc-close_msc>requirement.max_staleness_milliseconds) any_stale=true;
         if(requirement.max_close_skew_milliseconds>allowed_skew)
            allowed_skew=requirement.max_close_skew_milliseconds;
      }

      result.close_skew_milliseconds=result.maximum_close_utc_msc-result.minimum_close_utc_msc;
      if(any_gap){ result.status=SF03_SYNC_GAPPED; result.detail="series gap"; return false; }
      if(any_stale){ result.status=SF03_SYNC_STALE; result.detail="stale series"; return false; }
      if(result.close_skew_milliseconds>allowed_skew)
      { result.status=SF03_SYNC_WAITING; result.detail="close skew"; return false; }
      result.status=SF03_SYNC_READY;
      result.detail="synchronized";
      return true;
   }
};
#endif
