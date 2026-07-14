#property strict
#include <AlphaLab/StrategyFactory/SAEDV4EventModel/EventAuthority.mqh>
int OnInit(){return SAED_EventAuthoritySafe()?INIT_SUCCEEDED:INIT_FAILED;}
void OnTick(){}
