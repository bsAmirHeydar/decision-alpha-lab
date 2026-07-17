#ifndef __SAEDV440HEALTH_MQH__
#define __SAEDV440HEALTH_MQH__
// SAEDV440 static mirror. Reference control-plane contract only.
struct SAEDV440Health { string cell_id; int sample_count; double error_rate; long latency_p99_ms; bool heartbeat_fresh; };
#endif
