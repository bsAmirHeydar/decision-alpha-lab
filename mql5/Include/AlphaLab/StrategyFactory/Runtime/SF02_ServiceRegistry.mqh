#ifndef __SF02_SERVICE_REGISTRY_MQH__
#define __SF02_SERVICE_REGISTRY_MQH__

#include "../Ports/ISF02_LifecycleService.mqh"

class CSF02ServiceRegistry
{
private:
   ISF02LifecycleService *m_services[];
   string m_ids[];

public:
   CSF02ServiceRegistry(void)
   {
      ArrayResize(m_services, 0);
      ArrayResize(m_ids, 0);
   }

   int Count(void) const { return ArraySize(m_ids); }

   bool Register(ISF02LifecycleService *service, string &error)
   {
      if(CheckPointer(service) == POINTER_INVALID)
      { error = "invalid service pointer"; return false; }
      const string id = service.ServiceId();
      if(!SF01_IsSafeIdentifier(id)) { error = "invalid service id"; return false; }
      const int count = ArraySize(m_ids);
      for(int i = 0; i < count; i++)
      {
         if(m_ids[i] == id) { error = "duplicate service id: " + id; return false; }
      }
      ArrayResize(m_ids, count + 1);
      ArrayResize(m_services, count + 1);
      m_ids[count] = id;
      m_services[count] = service;
      error = "";
      return true;
   }

   ISF02LifecycleService *At(const int index) const
   {
      if(index < 0 || index >= ArraySize(m_services)) return NULL;
      return m_services[index];
   }
};

#endif
