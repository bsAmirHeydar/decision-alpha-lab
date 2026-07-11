#ifndef __SF09_OUTCOME_QUEUE_MQH__
#define __SF09_OUTCOME_QUEUE_MQH__
#include "SF09_OutcomeRecord.mqh"

class CSF09OutcomeQueue
{
private:
   SF09_OutcomeRecord m_items[SF09_MAX_OUTCOME_QUEUE];
   int m_head,m_tail,m_count,m_capacity;
   ENUM_SF09_QUEUE_OVERFLOW_POLICY m_policy;
   long m_dropped;
public:
   CSF09OutcomeQueue(void){m_head=0;m_tail=0;m_count=0;m_capacity=SF09_MAX_OUTCOME_QUEUE;m_policy=SF09_QUEUE_FAIL_ENGINE;m_dropped=0;}
   bool Configure(const int capacity,const ENUM_SF09_QUEUE_OVERFLOW_POLICY policy,string &error)
   {
      if(capacity<=0||capacity>SF09_MAX_OUTCOME_QUEUE){error="invalid outcome queue capacity";return false;}
      m_capacity=capacity;m_policy=policy;error="";return true;
   }
   bool Push(const SF09_OutcomeRecord &o,string &error)
   {
      if(m_count>=m_capacity)
      {
         if(m_policy==SF09_QUEUE_REJECT_NEW||m_policy==SF09_QUEUE_FAIL_ENGINE){error="outcome queue full";return false;}
         m_head=(m_head+1)%m_capacity;m_count--;m_dropped++;
      }
      m_items[m_tail]=o;m_tail=(m_tail+1)%m_capacity;m_count++;error="";return true;
   }
   bool Pop(SF09_OutcomeRecord &o)
   {
      if(m_count<=0)return false;o=m_items[m_head];m_head=(m_head+1)%m_capacity;m_count--;return true;
   }
   int Count(void) const{return m_count;}
   long Dropped(void) const{return m_dropped;}
};

#endif
