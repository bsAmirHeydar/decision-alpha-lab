#property strict
#ifndef SAEDV423REWARDAUDIT_MQH
#define SAEDV423REWARDAUDIT_MQH
// SAED_V4_23 static mirror. Research-only; no broker, runtime, promotion or execution authority.
bool SAEDV423RewardSum(const double reward,const double gross,const double cost,const double risk){ return MathAbs(reward-(gross+cost+risk))<=1e-9; }

#endif
