#ifndef __CGX_SIGNAL_REGISTRY_MQH__
#define __CGX_SIGNAL_REGISTRY_MQH__

#include <IntermarketDivergenceExecution/CG/Execution/CGX_Types.mqh>

class CCGX_SignalRegistry
{
private:
   SCGXTradeEntitlementRecord m_records[];
   datetime                   m_trading_day_start_ny;
   int                        m_max_records;

   int FindIndex(const string entitlement_key)
   {
      int count=ArraySize(m_records);
      for(int i=0;i<count;i++)
      {
         if(m_records[i].entitlement_key==entitlement_key)
            return i;
      }
      return -1;
   }

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
      ArrayResize(m_records,0);
      m_trading_day_start_ny=0;
   }

   void EnsureTradingDay(const datetime trading_day_start_ny)
   {
      if(m_trading_day_start_ny!=trading_day_start_ny)
      {
         ArrayResize(m_records,0);
         m_trading_day_start_ny=trading_day_start_ny;
      }
   }

   bool Contains(const string entitlement_key)
   {
      return (FindIndex(entitlement_key)>=0);
   }

   int Count()
   {
      return ArraySize(m_records);
   }

   bool ConsumeFirstObservation(const SCGCFinalSignal &signal,
                                const datetime observation_close_broker,
                                const string entitlement_key,
                                string &reason)
   {
      if(entitlement_key=="")
      {
         reason="empty_trade_entitlement_key";
         return false;
      }
      if(signal.signal_id=="")
      {
         reason="empty_signal_id";
         return false;
      }
      if(Contains(entitlement_key))
      {
         reason="one_shot_entitlement_already_consumed";
         return false;
      }

      int count=ArraySize(m_records);
      if(count>=m_max_records)
      {
         reason="one_shot_registry_capacity_reached";
         return false;
      }

      ArrayResize(m_records,count+1);
      m_records[count].entitlement_key=entitlement_key;
      m_records[count].signal_id=signal.signal_id;
      m_records[count].group_name=signal.group_name;
      m_records[count].group_minutes=signal.group_minutes;
      m_records[count].side=signal.side;
      m_records[count].trading_day_start_ny=signal.trading_day_start_ny;
      m_records[count].current_cycle_start_ny=signal.current_cycle_start_ny;
      m_records[count].reference_cycle_start_ny=signal.reference_cycle_start_ny;
      m_records[count].first_observation_close_broker=observation_close_broker;
      m_records[count].state=CGX_ENTITLEMENT_CONSUMED;
      reason="one_shot_entitlement_consumed_on_first_observation";
      return true;
   }
};

#endif
