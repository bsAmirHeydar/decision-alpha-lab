#property strict
#include <AlphaLab/StrategyFactory/SAEDV4SemanticHypergraph/GraphAll.mqh>

int OnInit()
  {
   if(!SAEDHypergraphStaticSelfTest())
      return INIT_FAILED;
   return INIT_SUCCEEDED;
  }

void OnTick()
  {
  }
