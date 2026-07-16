#property strict
#ifndef SAEDV423CHALLENGE_MQH
#define SAEDV423CHALLENGE_MQH
// SAED_V4_23 static mirror. Research-only; no broker, runtime, promotion or execution authority.
bool SAEDV423SyntheticVeto(const double score,const double threshold){ return score<=threshold; }

#endif
