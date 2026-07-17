#ifndef SAED_V4_28_REJECTION_LEDGER_MQH
#define SAED_V4_28_REJECTION_LEDGER_MQH
bool SAEDV428RejectP(const double p,const double alpha,const bool eligible){ return eligible && alpha>=0.0 && p<=alpha; }
#endif
