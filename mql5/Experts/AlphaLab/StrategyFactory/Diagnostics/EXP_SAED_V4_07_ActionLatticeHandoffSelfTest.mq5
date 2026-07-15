#property strict
#include <AlphaLab/StrategyFactory/SAEDV4ActionLattice/SAEDV4ActionLattice.mqh>
int OnInit(){ Print("V4-08 handoff bounded=",SAEDV407HandoffAllowsV408OutcomeCube()," order=",SAEDV407HandoffAllowsOrderPlacement()); return(INIT_SUCCEEDED); }
void OnTick(){}
