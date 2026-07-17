#ifndef SAED_V4_39_SURVEILLANCE_MQH
#define SAED_V4_39_SURVEILLANCE_MQH
struct SAEDV439SurveillanceSnapshot { double latency_p95_ms; double mean_slippage_bps; double reject_rate; int unauthorized_order_count; bool hard_breach; };
#endif
