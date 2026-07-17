#ifndef __SAEDV440RECONCILIATION_MQH__
#define __SAEDV440RECONCILIATION_MQH__
// SAEDV440 static mirror. Reference control-plane contract only.
struct SAEDV440Reconciliation { int registered_count; int manifest_count; int routed_count; int health_count; bool reconciled; };
#endif
