#ifndef __DECISION_ALPHA_LAB_SAEDV421REGRET_MQH__
#define __DECISION_ALPHA_LAB_SAEDV421REGRET_MQH__
double SAEDV421Regret(const double oracle_value,const double candidate_value){return MathMax(0.0,oracle_value-candidate_value);}
#endif
