#ifndef SAEDV416_TAIL_MQH
#define SAEDV416_TAIL_MQH
#define SAED_V4_16_PHASE "SAED_V4_16"
bool SAEDV416TailRiskValid(const double level,const double var_value,const double expected_shortfall,const int n,const int minimum_n){return level>0.0&&level<0.5&&expected_shortfall<=var_value&&n>=minimum_n;}
#endif
