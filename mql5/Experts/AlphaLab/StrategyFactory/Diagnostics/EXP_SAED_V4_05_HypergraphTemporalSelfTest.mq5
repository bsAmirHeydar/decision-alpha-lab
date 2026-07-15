#property strict
#include <AlphaLab/StrategyFactory/SAEDV4SemanticHypergraph/GraphAll.mqh>

int OnInit()
  {
   datetime event_as_of=D'2026.01.05 14:30:00';
   datetime known_as_of=D'2026.01.05 14:30:01';
   if(!SAEDHypergraphBoundaryVisible(event_as_of,known_as_of,event_as_of,known_as_of))
      return INIT_FAILED;
   if(SAEDHypergraphBoundaryVisible(D'2026.01.05 14:30:02',known_as_of,event_as_of,known_as_of))
      return INIT_FAILED;
   return INIT_SUCCEEDED;
  }

void OnTick()
  {
  }
