#ifndef __SAEDV440QUOTA_MQH__
#define __SAEDV440QUOTA_MQH__
// SAEDV440 static mirror. Reference control-plane contract only.
struct SAEDV440Quota { string tenant_id; int max_cells; int max_replicas; int max_cpu_units; int max_memory_mb; };
#endif
