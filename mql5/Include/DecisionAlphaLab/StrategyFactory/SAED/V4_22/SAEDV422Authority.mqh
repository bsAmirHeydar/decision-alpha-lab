#ifndef SAEDV422_AUTHORITY_MQH
#define SAEDV422_AUTHORITY_MQH
#include "SAEDV422Types.mqh"
SAEDV422Authority SAEDV422DeniedAuthority(){SAEDV422Authority a;a.decision=false;a.execution=false;a.promotion=false;a.production=false;a.risk_allocation=false;a.runtime=false;return a;}
#endif
