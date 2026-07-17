#ifndef __SAEDV440FLEETMANIFEST_MQH__
#define __SAEDV440FLEETMANIFEST_MQH__
// SAEDV440 static mirror. Reference control-plane contract only.
struct SAEDV440FleetManifest { string manifest_id; string manifest_hash; int cell_count; int replica_count; bool research_only; };
#endif
