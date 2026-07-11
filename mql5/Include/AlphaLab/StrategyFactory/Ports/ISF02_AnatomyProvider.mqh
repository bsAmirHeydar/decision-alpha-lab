#ifndef __ISF02_ANATOMY_PROVIDER_MQH__
#define __ISF02_ANATOMY_PROVIDER_MQH__

#include "ISF02_LifecycleService.mqh"
#include "../Contracts/SF01_AnatomyEvent.mqh"

class ISF02AnatomyProvider : public ISF02LifecycleService
{
public:
   virtual void ProcessTick(const MqlTick &tick) = 0;
   virtual void ProcessTimer(const long now_utc_msc) = 0;
   virtual bool PopEvent(SF01_AnatomyEvent &event) = 0;
   virtual int PendingEventCount(void) const = 0;
};

#endif
