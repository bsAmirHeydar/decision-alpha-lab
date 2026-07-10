#ifndef __EXP0018_DAYE_HUNT_STORE_MQH__
#define __EXP0018_DAYE_HUNT_STORE_MQH__

#include <DayeTrader/EXP0018/DAYE_HuntClassifier.mqh>

class CDayeHuntStore
{
private:
   DAYE_HuntObservation m_items[];

public:
   CDayeHuntStore(void) { ArrayResize(m_items,0); }
   void Clear(void) { ArrayResize(m_items,0); }

   void Replace(const DAYE_HuntObservation &items[])
   {
      ArrayResize(m_items,ArraySize(items));
      for(int i=0;i<ArraySize(items);i++) m_items[i] = items[i];
   }

   int Count(void) { return ArraySize(m_items); }

   bool Get(const int index,DAYE_HuntObservation &item)
   {
      if(index < 0 || index >= ArraySize(m_items)) return false;
      item = m_items[index];
      return true;
   }

   int Export(DAYE_HuntObservation &items[])
   {
      ArrayResize(items,ArraySize(m_items));
      for(int i=0;i<ArraySize(m_items);i++) items[i] = m_items[i];
      return ArraySize(items);
   }

   bool FindByObservationId(const string observation_id,DAYE_HuntObservation &item)
   {
      for(int i=0;i<ArraySize(m_items);i++)
      {
         if(m_items[i].observation_id == observation_id)
         {
            item = m_items[i];
            return true;
         }
      }
      return false;
   }

   bool LatestReady(DAYE_HuntObservation &item)
   {
      for(int i=ArraySize(m_items)-1;i>=0;i--)
      {
         if(m_items[i].status == DAYE_HUNT_STATUS_READY && m_items[i].is_publishable)
         {
            item = m_items[i];
            return true;
         }
      }
      return false;
   }

   bool LatestOneSided(DAYE_HuntObservation &item)
   {
      for(int i=ArraySize(m_items)-1;i>=0;i--)
      {
         if(m_items[i].status == DAYE_HUNT_STATUS_READY && m_items[i].is_one_sided)
         {
            item = m_items[i];
            return true;
         }
      }
      return false;
   }
};

#endif
