#property strict
#include <AlphaLab/StrategyFactory/SAEDV4EventModel/EventAll.mqh>
int OnInit(){return SAED_EventSelfTest()?INIT_SUCCEEDED:INIT_FAILED;}
void OnTick(){}
