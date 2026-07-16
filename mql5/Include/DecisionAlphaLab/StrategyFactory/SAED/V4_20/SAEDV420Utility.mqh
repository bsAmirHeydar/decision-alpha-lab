#property strict
#ifndef __DECISION_ALPHA_LAB_SAEDV420UTILITY_MQH__
#define __DECISION_ALPHA_LAB_SAEDV420UTILITY_MQH__
#define SAED_V4_20_PHASE "SAED_V4_20"
double SAEDV420Utility(const double reward,const double cost,const double risk){ return reward-cost-risk; }
#endif
