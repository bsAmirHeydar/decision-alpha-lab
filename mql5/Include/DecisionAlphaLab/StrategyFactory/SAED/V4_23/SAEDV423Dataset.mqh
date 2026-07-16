#property strict
#ifndef SAEDV423DATASET_MQH
#define SAEDV423DATASET_MQH
// SAED_V4_23 static mirror. Research-only; no broker, runtime, promotion or execution authority.
bool SAEDV423KnownTime(const datetime known_at,const datetime cutoff){ return known_at<=cutoff; }

#endif
