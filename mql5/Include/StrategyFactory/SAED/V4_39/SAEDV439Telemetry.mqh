#ifndef SAED_V4_39_TELEMETRY_MQH
#define SAED_V4_39_TELEMETRY_MQH
struct SAEDV439Telemetry { datetime known_time; double spread_bps; int latency_ms; bool disconnected; int reject_count; };
#endif
