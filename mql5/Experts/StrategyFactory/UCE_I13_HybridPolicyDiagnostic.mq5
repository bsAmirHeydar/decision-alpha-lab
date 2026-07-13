#property strict
#include <AlphaLab/StrategyFactory/HybridPolicy/UCEI13_All.mqh>
int OnInit(){Print("UCE-I13 catalog=",UCEI13CatalogCount()," registry=",UCEI13RegistryValid());return UCEI13RegistryValid()?INIT_SUCCEEDED:INIT_FAILED;}
void OnTick(){}
