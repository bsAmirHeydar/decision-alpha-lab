#property strict
#include <AlphaLab/StrategyFactory/SAEDV4OutcomeCube/SAEDV4OutcomeCube.mqh>
int OnInit(){if(SAEDV408CanSendOrder())return INIT_FAILED;if(SAEDV408Phase()!="SAED_V4_08")return INIT_FAILED;Print("SAED V4-08 diagnostic self-test passed; no runtime authority");return INIT_SUCCEEDED;}
void OnTick(){}
