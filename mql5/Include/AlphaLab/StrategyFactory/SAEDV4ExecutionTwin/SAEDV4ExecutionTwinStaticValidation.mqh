#ifndef __SAED_V4_EXECUTION_TWIN_STATIC_VALIDATION_MQH__
#define __SAED_V4_EXECUTION_TWIN_STATIC_VALIDATION_MQH__
#include "SAEDV4ExecutionTwinAuthority.mqh"
#include "SAEDV4ExecutionTwinIntegrity.mqh"
bool SAEDV409StaticBoundarySelfTest(){return !SAEDV409CanSendOrder() && !SAEDV409CanSelectTreatment() && !SAEDV409CanReplaceShadow() && SAEDV409IdentityPresent("executiontwin_reference");}
#endif
