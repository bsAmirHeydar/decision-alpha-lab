#property strict
#include <AlphaLab/StrategyFactory/SAEDV4ExecutionTwin/SAEDV4ExecutionTwin.mqh>
int OnInit(){return (SAEDV409ScaledLatency(10,2.0,-5)==15 && SAEDV409QueueAhead(1.0,2.0,-0.5)==1.5)?INIT_SUCCEEDED:INIT_FAILED;} void OnTick(){}
