#ifndef __ISF02_FEATURE_PROVIDER_MQH__
#define __ISF02_FEATURE_PROVIDER_MQH__

#include "ISF02_LifecycleService.mqh"
#include "../Contracts/SF01_AnatomyEvent.mqh"
#include "../Contracts/SF01_FeatureSnapshot.mqh"

class ISF02FeatureProvider : public ISF02LifecycleService
{
public:
   virtual bool BuildSnapshot(const SF01_AnatomyEvent &event,
                              const long state_generation,
                              CSF01FeatureSnapshot &snapshot,
                              string &error) = 0;
};

#endif
