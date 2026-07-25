#ifndef __ALPHA_LAB_STRATEGY_FACTORY_PAPER_BROKER_MQH__
#define __ALPHA_LAB_STRATEGY_FACTORY_PAPER_BROKER_MQH__

#include "SF_Contracts.mqh"

struct SF_PaperOrderState
  {
   SF_ExecutionIntent intent;
   bool               accepted;
   bool               filled;
   bool               closed;
   datetime           fill_time_utc;
   double             fill_price;
   datetime           close_time_utc;
   double             close_price;
   string             close_reason;
  };

class CSF_PaperBroker
  {
private:
   SF_PaperOrderState m_orders[];
public:
   int OrderCount(void) const { return(ArraySize(m_orders)); }

   bool Submit(const SF_ExecutionIntent &intent,string &reason)
     {
      reason="";
      for(int i=0;i<ArraySize(m_orders);i++)
        {
         if(m_orders[i].intent.intent_id==intent.intent_id)
           { reason="duplicate_intent"; return(false); }
        }
      const int index=ArraySize(m_orders);
      if(ArrayResize(m_orders,index+1)!=index+1)
        { reason="array_resize_failed"; return(false); }
      m_orders[index].intent=intent;
      m_orders[index].accepted=true;
      m_orders[index].filled=false;
      m_orders[index].closed=false;
      return(true);
     }

   bool GetOrder(const int index,SF_PaperOrderState &state) const
     {
      if(index<0 || index>=ArraySize(m_orders))
         return(false);
      state=m_orders[index];
      return(true);
     }
  };

#endif
