#ifndef SAEDV417KNOWNTIMEGUARD_MQH
#define SAEDV417KNOWNTIMEGUARD_MQH
bool SAEDV417KnownTimeValid(const datetime feature_time,const datetime decision_time){return feature_time<=decision_time;}
#endif
