#property strict
#include <AlphaLab/StrategyFactory/SAEDV4EventModel/EventAll.mqh>
int OnInit(){Print("SAED V4-03 event diagnostic; safe=",SAED_EventAuthoritySafe());return INIT_SUCCEEDED;}
void OnTick(){}
