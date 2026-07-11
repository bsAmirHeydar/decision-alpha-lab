#ifndef __ISF02_SYMBOL_SPEC_PORT_MQH__
#define __ISF02_SYMBOL_SPEC_PORT_MQH__

#include "ISF02_LifecycleService.mqh"

struct SF02_SymbolSpec
{
   string symbol;
   double point;
   double tick_size;
   double tick_value;
   double volume_min;
   double volume_max;
   double volume_step;
   int stops_level_points;
   int freeze_level_points;
   long specification_generation;
};

class ISF02SymbolSpecPort : public ISF02LifecycleService
{
public:
   virtual bool Get(const string symbol, SF02_SymbolSpec &spec, string &error) = 0;
};

#endif
