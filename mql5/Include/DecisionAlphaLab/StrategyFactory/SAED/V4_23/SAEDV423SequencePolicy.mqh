#property strict
#ifndef SAEDV423SEQUENCEPOLICY_MQH
#define SAEDV423SEQUENCEPOLICY_MQH
// SAED_V4_23 static mirror. Research-only; no broker, runtime, promotion or execution authority.
double SAEDV423RecencyWeight(const double decay,const int age){ return MathPow(decay,(double)MathMax(0,age)); }

#endif
