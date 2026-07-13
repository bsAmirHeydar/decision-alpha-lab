#property strict
#include <AlphaLab/StrategyFactory/ImmutableRuntime/UCEI14_All.mqh>
int OnInit(){Print("UCE-I14 runtime contract v",UCEI14ContractVersionMajor()," export=",UCEI14ExportFormat()," components=",UCEI14RequiredComponentCount());return(INIT_SUCCEEDED);}
void OnTick(){}
