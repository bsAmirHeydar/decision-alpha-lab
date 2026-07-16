#ifndef DECISION_ALPHA_LAB_SAED_V424_DRIFT_MQH
#define DECISION_ALPHA_LAB_SAED_V424_DRIFT_MQH
bool SAEDV424DriftBreach(const double rate,const double max_rate,const double psi,const double max_psi){ return rate>max_rate||psi>max_psi; }
#endif
