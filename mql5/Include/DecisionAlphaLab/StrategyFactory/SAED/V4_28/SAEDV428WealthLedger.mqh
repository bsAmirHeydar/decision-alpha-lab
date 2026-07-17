#ifndef SAED_V4_28_WEALTH_LEDGER_MQH
#define SAED_V4_28_WEALTH_LEDGER_MQH
double SAEDV428NextWealth(const double before,const double alpha,const double reward){ return MathMax(0.0,before-alpha+reward); }
#endif
