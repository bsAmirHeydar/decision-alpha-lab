#ifndef __UCEI10_REGISTRY_MQH__
#define __UCEI10_REGISTRY_MQH__

#include "UCEI10_Catalog.mqh"

class CUCEI10Registry
  {
private:
   UCEI10_AlgorithmDescriptor m_items[];
   bool                       m_frozen;

public:
                              CUCEI10Registry()
     {
      m_frozen=false;
     }

   bool BuildDefault()
     {
      if(m_frozen)
         return false;
      ArrayResize(m_items,0);
      ArrayResize(m_items,CUCEI10Catalog::Count());
      for(int index=0; index<ArraySize(m_items); index++)
        {
         if(!CUCEI10Catalog::Get(index,m_items[index]))
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
         if(m_items[index].native_algorithm)
            count++;
      return count;
     }

   bool ResolveExact(const string key,UCEI10_AlgorithmDescriptor &out) const
     {
      for(int index=0; index<ArraySize(m_items); index++)
        {
         if(m_items[index].Key()==key)
           {
            out=m_items[index];
            return true;
           }
        }
      return false;
     }
  };

#endif
