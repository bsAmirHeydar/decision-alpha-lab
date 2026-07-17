#ifndef SAED_V4_28_ALPHA_INVESTING_MQH
#define SAED_V4_28_ALPHA_INVESTING_MQH
double SAEDV428AlphaInvesting(const double wealth,const double spend_fraction){ return MathMax(0.0,wealth*spend_fraction); }
#endif
