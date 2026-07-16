#ifndef SAEDV416_RISKSET_MQH
#define SAEDV416_RISKSET_MQH
#define SAED_V4_16_PHASE "SAED_V4_16"
bool SAEDV416RiskSetValid(const int at_risk,const int observed,const int censored){return at_risk>=0 && observed>=0 && censored>=0 && observed+censored<=at_risk;}
#endif
