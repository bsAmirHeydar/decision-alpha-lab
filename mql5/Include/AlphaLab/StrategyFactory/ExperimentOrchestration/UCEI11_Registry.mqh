#ifndef __UCEI11_REGISTRY_MQH__
#define __UCEI11_REGISTRY_MQH__

#include "UCEI11_Catalog.mqh"

class CUCEI11SearchRegistry
  {
private:
   UCEI11_SearchDescriptor m_items[];
   bool                    m_frozen;

public:
                           CUCEI11SearchRegistry()
     {
      m_frozen=false;
     }

   bool BuildDefault()
     {
      if(m_frozen)
         return false;
      ArrayResize(m_items,CUCEI11Catalog::Count());
      for(int index=0; index<ArraySize(m_items); index++)
        {
         if(!CUCEI11Catalog::Get(index,m_items[index]) || !m_items[index].Valid())
            return false;
         for(int previous=0; previous<index; previous++)
            if(m_items[previous].Key()==m_items[index].Key())
               return false;
        }
      return true;
     }

   void Freeze()
     {
      m_frozen=true;
     }

   bool Frozen() const
     {
      return m_frozen;
     }

   int Count() const
     {
      return ArraySize(m_items);
     }

   int NativeCount() const
     {
      int count=0;
      for(int index=0; index<ArraySize(m_items); index++)
         if(m_items[index].native_adapter)
            count++;
      return count;
     }

   bool ResolveExact(const string key,UCEI11_SearchDescriptor &out) const
     {
      for(int index=0; index<ArraySize(m_items); index++)
         if(m_items[index].Key()==key)
           {
            out=m_items[index];
            return true;
           }
      return false;
     }
  };

#endif
