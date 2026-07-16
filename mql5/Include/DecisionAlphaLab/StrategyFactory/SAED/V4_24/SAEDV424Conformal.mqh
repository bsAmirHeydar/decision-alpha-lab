#ifndef DECISION_ALPHA_LAB_SAED_V424_CONFORMAL_MQH
#define DECISION_ALPHA_LAB_SAED_V424_CONFORMAL_MQH
double SAEDV424LowerBound(const double prediction,const double quantile){ return prediction-quantile; }
bool SAEDV424ConformalPass(const double lower,const double minimum){ return lower>=minimum; }
#endif
