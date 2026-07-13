#property strict
#include <AlphaLab/StrategyFactory/ContextTournament/UCEI15_Catalog.mqh>
#include <AlphaLab/StrategyFactory/ContextTournament/UCEI15_Tournament.mqh>
int OnInit(){Print("UCE-I15 diagnostic treatments=",UCEI15_TreatmentFamilyCount()," algorithms=",UCEI15_AlgorithmFamilyCount()," declared=",UCEI15_DeclaredTrials(2,9,9,3));return(INIT_SUCCEEDED);}
void OnTick(){}
