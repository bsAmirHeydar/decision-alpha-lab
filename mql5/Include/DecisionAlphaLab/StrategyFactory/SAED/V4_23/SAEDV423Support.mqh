#property strict
#ifndef SAEDV423SUPPORT_MQH
#define SAEDV423SUPPORT_MQH
// SAED_V4_23 static mirror. Research-only; no broker, runtime, promotion or execution authority.
bool SAEDV423SupportPass(const int count,const double behavior_p,const int min_count,const double min_p){ return count>=min_count && behavior_p>=min_p; }

#endif
