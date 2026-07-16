#property strict
#ifndef SAEDV423FQE_MQH
#define SAEDV423FQE_MQH
// SAED_V4_23 static mirror. Research-only; no broker, runtime, promotion or execution authority.
double SAEDV423BellmanTarget(const double reward,const double discount,const double next_value,const bool done){ return reward+(done?0.0:discount*next_value); }

#endif
