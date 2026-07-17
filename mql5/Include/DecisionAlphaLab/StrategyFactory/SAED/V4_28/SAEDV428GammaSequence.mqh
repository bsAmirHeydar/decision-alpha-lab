#ifndef SAED_V4_28_GAMMA_MQH
#define SAED_V4_28_GAMMA_MQH
double SAEDV428GammaAt(const double &weights[],const int index){ if(index<=0 || index>ArraySize(weights)) return 0.0; return weights[index-1]; }
#endif
