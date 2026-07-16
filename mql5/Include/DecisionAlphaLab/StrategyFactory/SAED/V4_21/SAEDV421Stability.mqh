#ifndef __DECISION_ALPHA_LAB_SAEDV421STABILITY_MQH__
#define __DECISION_ALPHA_LAB_SAEDV421STABILITY_MQH__
bool SAEDV421StableSpread(const double maximum_value,const double minimum_value,const double limit){return maximum_value-minimum_value<=limit;}
#endif
