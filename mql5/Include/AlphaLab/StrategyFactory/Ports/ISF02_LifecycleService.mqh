#ifndef __ISF02_LIFECYCLE_SERVICE_MQH__
#define __ISF02_LIFECYCLE_SERVICE_MQH__

#include "../Core/SF02_RuntimeConfig.mqh"
#include "../Core/SF02_ServiceHealth.mqh"

class ISF02LifecycleService
{
public:
   virtual string ServiceId(void) const = 0;
   virtual ENUM_SF02_SERVICE_KIND ServiceKind(void) const = 0;
   virtual bool Initialize(const SF02_RuntimeConfig &config, string &error) = 0;
   virtual bool Start(string &error) = 0;
   virtual void Stop(void) = 0;
   virtual void Shutdown(void) = 0;
   virtual SF02_ServiceHealth Health(const long now_utc_msc) const = 0;
};

#endif
