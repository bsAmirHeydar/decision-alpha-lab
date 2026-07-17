#ifndef __SAEDV440CELLIDENTITY_MQH__
#define __SAEDV440CELLIDENTITY_MQH__
// SAEDV440 static mirror. Reference control-plane contract only.
struct SAEDV440CellIdentity { string cell_id; string tenant_id; string context_id; int context_version; string runtime_hash; bool immutable; };
#endif
