#ifndef SAED_V4_28_SAFFRON_MQH
#define SAED_V4_28_SAFFRON_MQH
double SAEDV428SaffronBase(const double q,const double lambda,const double gamma,const int rejections){ return MathMax(0.0,(1.0-lambda)*q*gamma*(1+rejections)); }
#endif
