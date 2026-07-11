#property strict
#include <AlphaLab/StrategyFactory/Live/SF18_AllLive.mqh>
int OnInit()
{
 Print("SF18 Live Safety Diagnostic");Print("Default authority: LOCKED");Print("Only SF18_Mql5BrokerAdapter.mqh owns OrderCheck and OrderSend authority.");Print("No strategy intent is submitted by this diagnostic EA.");return INIT_SUCCEEDED;
}
void OnTick(){}
