#ifndef __SAED_V4_25_TRANSFER_MQH__
#define __SAED_V4_25_TRANSFER_MQH__
double SAEDV425TransferWeight(const bool same_regime,const bool same_context,const double support,const double ood_pvalue,const double distance){ double regime_bonus=same_regime?1.15:1.0; double context_bonus=same_context?1.10:1.0; return regime_bonus*context_bonus*support*ood_pvalue/(1.0+distance); }
bool SAEDV425TransferFallsBack(const int eligible_sources){ return eligible_sources<=0; }
#endif
