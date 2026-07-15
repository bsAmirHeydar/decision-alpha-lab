#property strict
#include <AlphaLab/StrategyFactory/SAEDV4ActionLattice/SAEDV4ActionLattice.mqh>
int OnInit(){ Print("SAED V4-07 action lattice diagnostic self-test: execution authority=",SAEDV407HasExecutionAuthority()); return(INIT_SUCCEEDED); }
void OnTick(){}
