#ifndef DAL_SAED_V426_COUNTERFACTUAL_MQH
#define DAL_SAED_V426_COUNTERFACTUAL_MQH
bool SAEDV426ThresholdCrossed(const double before,const double after,const double threshold){ return (before<threshold && after>=threshold)||(before>=threshold && after<threshold); }
#endif
