#ifndef __EXP0018_DAYE_SESSION_BOX_STORE_MQH__
#define __EXP0018_DAYE_SESSION_BOX_STORE_MQH__

#include <DayeTrader/EXP0018/DAYE_SessionBoxObjectManager.mqh>

class CDayeSessionBoxStore
{
private:
   DAYE_SessionBoxProjection m_items[];
public:
   CDayeSessionBoxStore(void) { ArrayResize(m_items,0); }
   void Clear(void) { ArrayResize(m_items,0); }
   int Count(void) { return ArraySize(m_items); }
   int Find(const string projection_id)
   {
      for(int i=0;i<ArraySize(m_items);i++) if(m_items[i].projection_id==projection_id) return i;
      return -1;
   }
   bool Get(const int index,DAYE_SessionBoxProjection &item)
   {
      if(index<0 || index>=ArraySize(m_items)) return false;
      item=m_items[index]; return true;
   }
   bool Upsert(const DAYE_SessionBoxProjection &item,const int maximum_count)
   {
      int index=Find(item.projection_id);
      if(index>=0) { m_items[index]=item; return true; }
      if(ArraySize(m_items)>=maximum_count) return false;
      int n=ArraySize(m_items); ArrayResize(m_items,n+1); m_items[n]=item; return true;
   }
   int Export(DAYE_SessionBoxProjection &items[])
   {
      ArrayResize(items,ArraySize(m_items));
      for(int i=0;i<ArraySize(m_items);i++) items[i]=m_items[i];
      return ArraySize(items);
   }
};

#endif
