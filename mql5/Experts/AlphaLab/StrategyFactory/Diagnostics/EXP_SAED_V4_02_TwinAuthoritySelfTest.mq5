#property strict
#include <AlphaLab/StrategyFactory/SAEDV4ContextTwin/TwinAuthority.mqh>
int OnInit(){bool ok=ALTwinAuthoritySafe();Print("SAED V4-02 authority=",ok);return ok?INIT_SUCCEEDED:INIT_FAILED;}
void OnTick(){}
