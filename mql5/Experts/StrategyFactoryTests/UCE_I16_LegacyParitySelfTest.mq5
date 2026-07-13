#property strict
#include <AlphaLab/StrategyFactory/ContextOnboarding/UCEI16_All.mqh>
int OnInit(){ bool same=UCEI16_Matches(1.25,1.25,0.0); bool diff=!UCEI16_Matches(1.25,1.50,0.01); return (same && diff)?INIT_SUCCEEDED:INIT_FAILED; }
void OnTick(){}
