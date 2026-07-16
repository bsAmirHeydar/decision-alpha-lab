#property strict
#ifndef __DECISION_ALPHA_LAB_SAEDV420PARETO_MQH__
#define __DECISION_ALPHA_LAB_SAEDV420PARETO_MQH__
#define SAED_V4_20_PHASE "SAED_V4_20"
bool SAEDV420Dominates(const double a1,const double a2,const double b1,const double b2){ return a1>=b1 && a2>=b2 && (a1>b1 || a2>b2); }
#endif
