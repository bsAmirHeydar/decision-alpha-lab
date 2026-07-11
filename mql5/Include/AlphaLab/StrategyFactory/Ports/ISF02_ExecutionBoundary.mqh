#ifndef __ISF02_EXECUTION_BOUNDARY_MQH__
#define __ISF02_EXECUTION_BOUNDARY_MQH__

#include "ISF02_LifecycleService.mqh"

class ISF02ExecutionBoundary : public ISF02LifecycleService
{
public:
   virtual bool HasLiveOrderAuthority(void) const = 0;
   virtual string AuthorityDescription(void) const = 0;
};

#endif
