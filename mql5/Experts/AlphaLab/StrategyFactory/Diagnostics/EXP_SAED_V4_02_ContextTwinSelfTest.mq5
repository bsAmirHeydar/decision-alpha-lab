#property strict
#include <AlphaLab/StrategyFactory/SAEDV4ContextTwin/TwinAll.mqh>
int OnInit(){bool ok=ALTwinAuthoritySafe() && ALTwinSupportStatus(1.0,0.8,0.4,false,false)==AL_SUPPORT_SUPPORTED && ALTwinTransitionDisposition(true,true,true,true,true,false)==AL_TRANSITION_APPLIED;Print("SAED V4-02 selftest=",ok);return ok?INIT_SUCCEEDED:INIT_FAILED;}
void OnTick(){}
