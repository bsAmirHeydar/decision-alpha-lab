#ifndef __SF08_CANDIDATE_QUEUE_MQH__
#define __SF08_CANDIDATE_QUEUE_MQH__
#include "SF08_TradeCandidate.mqh"

class CSF08CandidateQueue
{
private:
   SF08_TradeCandidate m_items[];
   int m_capacity;
   ENUM_SF08_QUEUE_OVERFLOW_POLICY m_policy;
   long m_dropped;
public:
   CSF08CandidateQueue(void){ArrayResize(m_items,0);m_capacity=SF08_MAX_CANDIDATES_PER_EVENT;m_policy=SF08_QUEUE_FAIL_ENGINE;m_dropped=0;}
   bool Configure(const int capacity,const ENUM_SF08_QUEUE_OVERFLOW_POLICY policy,string &error)
   {if(capacity<1||capacity>4096){error="invalid candidate queue capacity";return false;}m_capacity=capacity;m_policy=policy;ArrayResize(m_items,0);m_dropped=0;error="";return true;}
   int Count(void)const{return ArraySize(m_items);} long Dropped(void)const{return m_dropped;}
   bool Contains(const string candidate_id)const{for(int i=0;i<ArraySize(m_items);i++)if(m_items[i].candidate_id==candidate_id)return true;return false;}
   bool Push(const SF08_TradeCandidate &candidate,string &error)
   {
      if(Contains(candidate.candidate_id)){error="duplicate candidate id";return false;}
      int n=ArraySize(m_items);
      if(n>=m_capacity)
      {
         if(m_policy==SF08_QUEUE_REJECT_NEW){m_dropped++;error="candidate queue full";return false;}
         if(m_policy==SF08_QUEUE_FAIL_ENGINE){error="candidate queue overflow";return false;}
         for(int i=1;i<n;i++)m_items[i-1]=m_items[i];ArrayResize(m_items,n-1);m_dropped++;n--;
      }
      ArrayResize(m_items,n+1);m_items[n]=candidate;error="";return true;
   }
   bool Pop(SF08_TradeCandidate &candidate)
   {int n=ArraySize(m_items);if(n<=0)return false;candidate=m_items[0];for(int i=1;i<n;i++)m_items[i-1]=m_items[i];ArrayResize(m_items,n-1);return true;}
   void Clear(void){ArrayResize(m_items,0);}
};

#endif
