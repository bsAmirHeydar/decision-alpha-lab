#ifndef __UCEI12_REGISTRY_MQH__
#define __UCEI12_REGISTRY_MQH__

#include "UCEI12_Catalog.mqh"

class CUCEI12SuiteRegistry
  {
private:
   UCEI12_SuiteDescriptor m_items[];
   bool m_frozen;
public:
   CUCEI12SuiteRegistry() { m_frozen=false; }
   bool BuildDefault()
     {
      if(m_frozen) return false;
      ArrayResize(m_items,CUCEI12Catalog::Count());
      for(int i=0;i<ArraySize(m_items);i++)
        {
         if(!CUCEI12Catalog::Get(i,m_items[i]) || !m_items[i].Valid()) return false;
         for(int j=0;j<i;j++) if(m_items[j].RegistryKey()==m_items[i].RegistryKey()) return false;
        }
      return true;
     }
   void Freeze() { m_frozen=true; }
   bool Frozen() const { return m_frozen; }
   int Count() const { return ArraySize(m_items); }
   int CriticalCount() const
     {
      int count=0; for(int i=0;i<ArraySize(m_items);i++) if(m_items[i].critical) count++; return count;
     }
   bool ResolveExact(const string key,UCEI12_SuiteDescriptor &out) const
     {
      for(int i=0;i<ArraySize(m_items);i++) if(m_items[i].RegistryKey()==key) { out=m_items[i]; return true; }
      return false;
     }
  };

#endif
