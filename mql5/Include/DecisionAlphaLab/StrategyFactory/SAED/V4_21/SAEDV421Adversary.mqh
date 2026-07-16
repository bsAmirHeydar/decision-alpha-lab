#ifndef __DECISION_ALPHA_LAB_SAEDV421ADVERSARY_MQH__
#define __DECISION_ALPHA_LAB_SAEDV421ADVERSARY_MQH__
double SAEDV421BoundedAdverse(const double value,const double shock,const double bound){return value-MathMin(MathAbs(shock),MathAbs(bound));}
#endif
