#ifndef __EXP0018_DAYE_RELATIONSHIP_STORE_MQH__
#define __EXP0018_DAYE_RELATIONSHIP_STORE_MQH__

#include <DayeTrader/EXP0018/DAYE_RelationshipResolver.mqh>

class CDayeRelationshipStore
{
private:
   DAYE_RelationshipResolution m_items[];

public:
   CDayeRelationshipStore(void)
   {
      ArrayResize(m_items,0);
   }

   void Clear(void)
   {
      ArrayResize(m_items,0);
   }

   void Replace(const DAYE_RelationshipResolution &items[])
   {
      ArrayResize(m_items,ArraySize(items));
      for(int i=0;i<ArraySize(items);i++)
         m_items[i] = items[i];
   }

   int Count(void)
   {
      return ArraySize(m_items);
   }

   bool Get(const int index,DAYE_RelationshipResolution &item)
   {
      if(index < 0 || index >= ArraySize(m_items))
         return false;
      item = m_items[index];
      return true;
   }

   int Export(DAYE_RelationshipResolution &items[])
   {
      ArrayResize(items,ArraySize(m_items));
      for(int i=0;i<ArraySize(m_items);i++)
         items[i] = m_items[i];
      return ArraySize(items);
   }

   bool FindByOpportunityId(const string opportunity_id,DAYE_RelationshipResolution &item)
   {
      for(int i=0;i<ArraySize(m_items);i++)
      {
         if(m_items[i].opportunity_id == opportunity_id)
         {
            item = m_items[i];
            return true;
         }
      }
      return false;
   }

   bool LatestReady(DAYE_RelationshipResolution &item)
   {
      for(int i=ArraySize(m_items)-1;i>=0;i--)
      {
         if(m_items[i].status == DAYE_REL_RESOLUTION_READY && m_items[i].is_publishable)
         {
            item = m_items[i];
            return true;
         }
      }
      return false;
   }
};

#endif
