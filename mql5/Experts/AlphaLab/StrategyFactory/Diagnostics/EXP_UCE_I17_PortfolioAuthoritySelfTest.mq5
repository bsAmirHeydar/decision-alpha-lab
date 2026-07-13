#property strict
#include <AlphaLab/StrategyFactory/Portfolio/PortfolioAll.mqh>
int OnInit(){ if(AL_PORTFOLIO_ORDER_AUTHORITY||AL_PORTFOLIO_BROKER_AUTHORITY||AL_PORTFOLIO_NETWORK_AUTHORITY)return INIT_FAILED; return INIT_SUCCEEDED; }
void OnTick(){}
