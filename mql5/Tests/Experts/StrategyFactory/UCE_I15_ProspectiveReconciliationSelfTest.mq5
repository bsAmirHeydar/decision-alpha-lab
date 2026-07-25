#property strict
#include <AlphaLab/StrategyFactory/ContextTournament/UCEI15_Paper.mqh>
int OnInit(){if(!UCEI15_PaperPlanPass(100,200,20,false,false))return(INIT_FAILED);if(!UCEI15_ReconciliationPass(100.0,100.01,0.10,0.11,0.05))return(INIT_FAILED);if(UCEI15_ReconciliationPass(100.0,100.20,0.10,0.11,0.05))return(INIT_FAILED);return(INIT_SUCCEEDED);}
void OnTick(){}
