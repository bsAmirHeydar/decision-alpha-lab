#ifndef __CGX_SIGNAL_REGISTRY_MQH__
#define __CGX_SIGNAL_REGISTRY_MQH__

#include <IntermarketDivergenceExecution/CG/Execution/CGX_TradePlanner.mqh>

class CCGX_SignalRegistry
{
private:
   string   m_keys[];
   datetime m_trading_day_start_ny;
   int      m_max_records;

public:
   void Configure(const int max_records)
   {
      m_max_records=max_records;
      if(m_max_records<100)
         m_max_records=100;
      Clear();
   }

   void Clear()
   {
      ArrayResize(m_keys,0);
      m_trading_day_start_ny=0;
   }

   void EnsureTradingDay(const datetime trading_day_start_ny)
   {
      if(m_trading_day_start_ny!=trading_day_start_ny)
      {
         ArrayResize(m_keys,0);
         m_trading_day_start_ny=trading_day_start_ny;
      }
   }

   bool Contains(const string key)
   {
      int count=ArraySize(m_keys);
      for(int i=0;i<count;i++)
      {
         if(m_keys[i]==key)
            return true;
      }
      return false;
   }

   bool RegisterAttempt(const string key,string &reason)
   {
      if(key=="")
      {
         reason="empty_registry_key";
         return false;
      }
      if(Contains(key))
      {
         reason="duplicate_signal_id";
         return false;
      }
      int count=ArraySize(m_keys);
      if(count>=m_max_records)
      {
         reason="signal_registry_capacity_reached";
         return false;
      }
      ArrayResize(m_keys,count+1);
      m_keys[count]=key;
      reason="registered";
      return true;
   }
};

#endif
