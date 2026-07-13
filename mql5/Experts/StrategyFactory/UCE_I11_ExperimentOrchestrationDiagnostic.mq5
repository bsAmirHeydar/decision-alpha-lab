#property strict
#property description "UCE-I11 experiment-orchestration contract diagnostic. No trading authority."

#include <AlphaLab/StrategyFactory/ExperimentOrchestration/UCEI11_All.mqh>

int OnInit()
  {
   CUCEI11SearchRegistry registry;
   if(!registry.BuildDefault())
      return INIT_FAILED;
   registry.Freeze();
   PrintFormat("UCE-I11 search registry: total=%d native=%d frozen=%s",
               registry.Count(),registry.NativeCount(),registry.Frozen() ? "true" : "false");
   if(registry.Count()!=10 || registry.NativeCount()!=9 || !registry.Frozen())
      return INIT_FAILED;
   return INIT_SUCCEEDED;
  }

void OnTick()
  {
   // Diagnostic only. No market, order, broker, position, or network authority.
  }
