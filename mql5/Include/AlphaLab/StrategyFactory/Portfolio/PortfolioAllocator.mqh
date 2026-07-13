#ifndef ALPHALAB_PORTFOLIO_ALLOCATOR_MQH
#define ALPHALAB_PORTFOLIO_ALLOCATOR_MQH
#include "PortfolioEnums.mqh"
int ALPortfolioGate(const double selected_risk,const double reserved_risk,const double total_limit,const int contexts,const int min_contexts){ if(MathAbs(selected_risk-reserved_risk)>1e-9)return AL_PORTFOLIO_REJECT; if(selected_risk>total_limit)return AL_PORTFOLIO_REJECT; if(contexts<min_contexts)return AL_PORTFOLIO_ABSTAIN; return AL_PORTFOLIO_ALLOCATE; }
#endif
