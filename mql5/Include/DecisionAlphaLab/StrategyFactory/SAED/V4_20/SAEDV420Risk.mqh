#property strict
#ifndef __DECISION_ALPHA_LAB_SAEDV420RISK_MQH__
#define __DECISION_ALPHA_LAB_SAEDV420RISK_MQH__
#define SAED_V4_20_PHASE "SAED_V4_20"
double SAEDV420LCB(const double mean,const double sigma,const double z){ return mean-z*sigma; }
#endif
