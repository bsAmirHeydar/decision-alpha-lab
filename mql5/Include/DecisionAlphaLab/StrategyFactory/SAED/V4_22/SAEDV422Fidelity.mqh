#ifndef SAEDV422_FIDELITY_MQH
#define SAEDV422_FIDELITY_MQH
double SAEDV422NormalizedError(const double observed,const double reference,const double limit){if(limit<=0)return DBL_MAX;return MathAbs(observed-reference)/limit;}
#endif
