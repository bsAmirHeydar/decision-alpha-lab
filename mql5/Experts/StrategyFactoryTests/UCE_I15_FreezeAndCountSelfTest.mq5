#property strict
#include <AlphaLab/StrategyFactory/ContextTournament/UCEI15_Freeze.mqh>
#include <AlphaLab/StrategyFactory/ContextTournament/UCEI15_Tournament.mqh>
int OnInit(){if(!UCEI15_FreezePass(1,2,true,true))return(INIT_FAILED);if(UCEI15_DeclaredTrials(2,9,9,3)!=486)return(INIT_FAILED);if(!UCEI15_CountsPass(486,486,486,0))return(INIT_FAILED);return(INIT_SUCCEEDED);}
void OnTick(){}
