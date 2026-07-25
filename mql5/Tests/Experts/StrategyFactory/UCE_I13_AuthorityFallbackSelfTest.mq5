#property strict
#include <AlphaLab/StrategyFactory/HybridPolicy/UCEI13_All.mqh>
int OnInit(){if(UCEI13ResolveAuthority(true,true,true,true)!=UCEI13_KILL)return INIT_FAILED;if(UCEI13FallbackFor(true,false)!=UCEI13_REJECT)return INIT_FAILED;if(UCEI13FallbackFor(false,true)!=UCEI13_ABSTAIN)return INIT_FAILED;return INIT_SUCCEEDED;}
void OnTick(){}
