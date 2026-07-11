#ifndef __ISF02_CLOCK_PORT_MQH__
#define __ISF02_CLOCK_PORT_MQH__

#include "ISF02_LifecycleService.mqh"
#include "../Contracts/SF01_MarketTimestamp.mqh"

class ISF02ClockPort : public ISF02LifecycleService
{
public:
   virtual long UtcNowMilliseconds(void) const = 0;
   virtual ulong MonotonicMicroseconds(void) const = 0;
   virtual SF01_MarketTimestamp Now(const string source_clock_id = "runtime") const = 0;
};

#endif
