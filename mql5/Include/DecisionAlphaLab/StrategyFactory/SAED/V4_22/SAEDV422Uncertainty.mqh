#ifndef SAEDV422_UNCERTAINTY_MQH
#define SAEDV422_UNCERTAINTY_MQH
bool SAEDV422TrustedHorizonStep(const double ensemble_std,const double threshold){return ensemble_std<=threshold;}
#endif
