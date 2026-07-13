#property strict
#property version "1.00"
#property description "UCE-I12 offline statistical promotion contract diagnostic"

#include "../../Include/AlphaLab/StrategyFactory/StatisticalPromotion/UCEI12_All.mqh"

int OnInit()
  {
   CUCEI12SuiteRegistry registry;
   if(!registry.BuildDefault()) return INIT_FAILED;
   registry.Freeze();
   Print("UCE-I12 registry suites=",registry.Count()," critical=",registry.CriticalCount()," frozen=",registry.Frozen());
   return INIT_SUCCEEDED;
  }

void OnTick() {}
