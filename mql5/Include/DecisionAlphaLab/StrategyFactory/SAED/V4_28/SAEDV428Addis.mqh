#ifndef SAED_V4_28_ADDIS_MQH
#define SAED_V4_28_ADDIS_MQH
double SAEDV428AddisBase(const double q,const double lambda,const double tau,const double gamma,const int rejections,const bool discarded){ if(discarded) return 0.0; return MathMax(0.0,(tau-lambda)*q*gamma*(1+rejections)); }
#endif
