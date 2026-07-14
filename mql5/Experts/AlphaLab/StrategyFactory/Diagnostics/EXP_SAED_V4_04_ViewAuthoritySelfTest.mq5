#property strict
#include <AlphaLab/StrategyFactory/SAEDV4MultimodalViews/ViewAll.mqh>
int OnInit(){ return SAEDViewAuthoritySafe()?INIT_SUCCEEDED:INIT_FAILED; }
void OnTick(){}
