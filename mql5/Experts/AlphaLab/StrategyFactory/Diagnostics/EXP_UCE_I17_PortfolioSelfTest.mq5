#property strict
#include <AlphaLab/StrategyFactory/Portfolio/PortfolioAll.mqh>
int OnInit(){ int gate=ALPortfolioGate(2.0,2.0,4.0,2,2); if(gate!=AL_PORTFOLIO_ALLOCATE)return INIT_FAILED; if(ALPortfolioGate(2.0,0.0,4.0,2,2)!=AL_PORTFOLIO_REJECT)return INIT_FAILED; return INIT_SUCCEEDED; }
void OnTick(){}
