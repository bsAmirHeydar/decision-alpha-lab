#property strict
#ifndef SAEDV423PROJECTION_MQH
#define SAEDV423PROJECTION_MQH
// SAED_V4_23 static mirror. Research-only; no broker, runtime, promotion or execution authority.
double SAEDV423SafeFloor(const double p,const double floor_p){ return MathMax(p,floor_p); }

#endif
