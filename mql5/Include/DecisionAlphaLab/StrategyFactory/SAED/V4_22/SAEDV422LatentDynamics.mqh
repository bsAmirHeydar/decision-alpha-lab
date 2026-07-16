#ifndef SAEDV422_LATENT_DYNAMICS_MQH
#define SAEDV422_LATENT_DYNAMICS_MQH
double SAEDV422LatentStep(const double state,const double phi,const double innovation){return MathMax(-0.15,MathMin(0.15,phi*state+innovation));}
#endif
