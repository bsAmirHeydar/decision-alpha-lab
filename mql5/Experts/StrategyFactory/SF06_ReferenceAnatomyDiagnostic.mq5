#property strict
#property version "1.00"
#property description "No-send diagnostic for the central reference anatomy adapter"
#include <AlphaLab\StrategyFactory\Anatomy\SF06_AllAnatomy.mqh>
int OnInit(){Print("SF06 diagnostic loaded. Use SF06_StrategyHost for live data audit. No order authority exists.");return INIT_SUCCEEDED;}
