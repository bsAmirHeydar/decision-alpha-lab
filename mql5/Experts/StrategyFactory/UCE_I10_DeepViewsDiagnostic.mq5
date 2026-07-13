#property strict
#property description "UCE-I10 contract/catalog diagnostic only. No trading authority."

#include <AlphaLab/StrategyFactory/DeepViews/UCEI10_All.mqh>

int OnInit()
  {
   CUCEI10Registry registry;
   if(!registry.BuildDefault())
     {
      Print("UCE-I10: registry build failed");
      return INIT_FAILED;
     }
   registry.Freeze();
   PrintFormat("UCE-I10 catalog ready: total=%d native=%d frozen=%s",
               registry.Count(),registry.NativeCount(),registry.Frozen() ? "true" : "false");
   if(registry.Count()!=17 || registry.NativeCount()!=10 || !registry.Frozen())
      return INIT_FAILED;
   return INIT_SUCCEEDED;
  }

void OnTick()
  {
   // Contract diagnostic only. Intentionally no market or execution behavior.
  }
