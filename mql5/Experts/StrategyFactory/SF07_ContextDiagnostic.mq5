#property strict
#property version "1.00"
#property description "No-send diagnostic for the Phase 07 context and feature DAG engine"
#include <AlphaLab\StrategyFactory\Context\SF07_AllContext.mqh>
int OnInit(){Print("SF07 diagnostic loaded. Context DAG, immutable frames and fixed vectors are available. No order authority exists.");return INIT_SUCCEEDED;}
