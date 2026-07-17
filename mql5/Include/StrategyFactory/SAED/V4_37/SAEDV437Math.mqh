#ifndef SAED_V4_37_MATH_MQH
#define SAED_V4_37_MATH_MQH
// SAED_V4_37 deterministic arithmetic helpers.
double SAEDV437Clamp(const double x,const double lo,const double hi){return MathMax(lo,MathMin(hi,x));}
double SAEDV437BpsCost(const double notional,const double bps){return MathAbs(notional)*bps/10000.0;}
#endif
