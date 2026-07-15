#ifndef SAED_V4_12_PARITY_MQH
#define SAED_V4_12_PARITY_MQH
bool SAEDV412WithinTolerance(const double a,const double b,const double tolerance){ return MathAbs(a-b)<=tolerance; }
#endif
