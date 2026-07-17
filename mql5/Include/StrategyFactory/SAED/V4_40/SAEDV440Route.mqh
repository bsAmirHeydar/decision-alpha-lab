#ifndef __SAEDV440ROUTE_MQH__
#define __SAEDV440ROUTE_MQH__
// SAEDV440 static mirror. Reference control-plane contract only.
struct SAEDV440Route { string tenant_id; string context_id; int context_version; string cell_id; bool enabled; };
#endif
