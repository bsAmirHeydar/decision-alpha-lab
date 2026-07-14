#property strict
#include <AlphaLab/StrategyFactory/SAEDV4ContextTwin/TwinAll.mqh>
int OnInit(){Print("SAED V4-02 diagnostic phase=",AL_SAED_V4_02_PHASE," safe=",ALTwinDiagnosticReady());return ALTwinDiagnosticReady()?INIT_SUCCEEDED:INIT_FAILED;}
void OnTick(){}
