#property strict
#ifndef SAEDV423AUTHORITY_MQH
#define SAEDV423AUTHORITY_MQH
// SAED_V4_23 static mirror. Research-only; no broker, runtime, promotion or execution authority.
bool SAEDV423ResearchOnly(){ return true; }
bool SAEDV423RuntimeAllowed(){ return false; }
bool SAEDV423PromotionAllowed(){ return false; }

#endif
