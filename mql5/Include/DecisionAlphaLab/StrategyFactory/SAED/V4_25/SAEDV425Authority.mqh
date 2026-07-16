#ifndef __SAED_V4_25_AUTHORITY_MQH__
#define __SAED_V4_25_AUTHORITY_MQH__
#include "SAEDV425Types.mqh"
SAEDV425Authority SAEDV425DeniedAuthority(){ SAEDV425Authority a; a.decision=false; a.promotion=false; a.runtime=false; a.risk_allocation=false; a.execution=false; a.order_submission=false; a.production=false; a.online_learning=false; return a; }
bool SAEDV425AuthoritySafe(const SAEDV425Authority &a){ return !a.decision && !a.promotion && !a.runtime && !a.risk_allocation && !a.execution && !a.order_submission && !a.production && !a.online_learning; }
#endif
