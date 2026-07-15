#ifndef __SAED_V4_EXECUTION_TWIN_LATENCY_MQH__
#define __SAED_V4_EXECUTION_TWIN_LATENCY_MQH__
long SAEDV409ScaledLatency(const long base_ms,const double multiplier,const long jitter_ms){long value=(long)MathRound(base_ms*multiplier)+jitter_ms;return value<0?0:value;}
#endif
