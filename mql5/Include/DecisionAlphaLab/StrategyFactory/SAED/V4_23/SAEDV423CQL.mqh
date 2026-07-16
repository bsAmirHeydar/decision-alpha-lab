#property strict
#ifndef SAEDV423CQL_MQH
#define SAEDV423CQL_MQH
// SAED_V4_23 static mirror. Research-only; no broker, runtime, promotion or execution authority.
double SAEDV423ConservativePenalty(const double alpha,const int count){ return alpha/MathSqrt((double)MathMax(1,count)); }

#endif
