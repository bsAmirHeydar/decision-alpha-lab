#property strict
#ifndef SAEDV423OPE_MQH
#define SAEDV423OPE_MQH
// SAED_V4_23 static mirror. Research-only; no broker, runtime, promotion or execution authority.
double SAEDV423ImportanceRatio(const double pi,const double mu,const double clip){ if(mu<=0.0)return 0.0; return MathMin(clip,pi/mu); }

#endif
