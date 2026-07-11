#property strict
#property description "Phase 19 deterministic observability diagnostic. It has no broker authority."
#include <AlphaLab/StrategyFactory/Monitoring/SF19_AllMonitoring.mqh>
input int InpRingCapacity=256;
int OnInit(){string error;CSF19MonitoringCoordinator engine;if(!engine.Configure("sf19-diagnostic","generation-diagnostic","strategy-diagnostic","model-diagnostic",InpRingCapacity,error)){Print(error);return INIT_FAILED;}Print("SF19 diagnostic ready; monitoring is advisory and operator-approved");return INIT_SUCCEEDED;}
void OnTick(){}
