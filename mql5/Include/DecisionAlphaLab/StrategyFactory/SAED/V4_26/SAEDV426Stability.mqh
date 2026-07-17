#ifndef DAL_SAED_V426_STABILITY_MQH
#define DAL_SAED_V426_STABILITY_MQH
bool SAEDV426StabilityGate(const double cosine,const double floor){ return cosine>=floor; }
#endif
