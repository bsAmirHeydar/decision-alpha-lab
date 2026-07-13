#property strict
#include <AlphaLab/StrategyFactory/ContextOnboarding/UCEI16_All.mqh>
int OnInit(){ Print("UCE-I16 contexts=",UCEI16_TotalMigrationUnitCount()," authority=",UCEI16_HasTradingAuthority()); return INIT_SUCCEEDED; }
void OnTick(){}
