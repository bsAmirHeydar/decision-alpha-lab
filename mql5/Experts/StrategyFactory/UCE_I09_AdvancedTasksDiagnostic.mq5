#property strict
#include <AlphaLab/StrategyFactory/AdvancedTasks/UCEI09_All.mqh>
int OnInit(){CUCEI09Registry registry;if(!registry.BuildDefault())return INIT_FAILED;registry.Freeze();Print("UCE-I09 advanced task catalog ready: ",registry.Count());return registry.Count()==18?INIT_SUCCEEDED:INIT_FAILED;}
void OnTick(){}
