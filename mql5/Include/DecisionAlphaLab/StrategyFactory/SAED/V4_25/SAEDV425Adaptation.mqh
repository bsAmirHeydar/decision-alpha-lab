#ifndef __SAED_V4_25_ADAPTATION_MQH__
#define __SAED_V4_25_ADAPTATION_MQH__
#include "SAEDV425Canonical.mqh"
double SAEDV425BlendParameter(const double empirical,const double prior_value,const double baseline,const double sample_size,const double prior_strength,const double maximum_delta){ double candidate=(sample_size*empirical+prior_strength*prior_value)/(sample_size+prior_strength); return baseline+SAEDV425Clamp(candidate-baseline,-maximum_delta,maximum_delta); }
#endif
