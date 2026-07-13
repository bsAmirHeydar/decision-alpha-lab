#ifndef ALPHALAB_PORTFOLIO_DEPENDENCE_MQH
#define ALPHALAB_PORTFOLIO_DEPENDENCE_MQH
double ALConservativeCorrelation(const bool same_symbol,const bool same_currency,const bool same_cluster,const double fallback_rho){ if(same_symbol)return 1.0; if(same_currency)return MathMax(0.8,fallback_rho); if(same_cluster)return MathMax(0.75,fallback_rho); return fallback_rho; }
#endif
