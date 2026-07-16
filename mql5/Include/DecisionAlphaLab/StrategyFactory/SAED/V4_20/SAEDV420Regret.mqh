#property strict
#ifndef __DECISION_ALPHA_LAB_SAEDV420REGRET_MQH__
#define __DECISION_ALPHA_LAB_SAEDV420REGRET_MQH__
#define SAED_V4_20_PHASE "SAED_V4_20"
double SAEDV420Regret(const double best,const double selected){ return MathMax(0.0,best-selected); }
#endif
