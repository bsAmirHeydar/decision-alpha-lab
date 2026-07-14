#ifndef AL_SAED_V4_02_TWIN_DIAGNOSTICS_MQH
#define AL_SAED_V4_02_TWIN_DIAGNOSTICS_MQH
#include "TwinAuthority.mqh"
#include "TwinIntegrity.mqh"
bool ALTwinDiagnosticReady(){return ALTwinAuthoritySafe();}
#endif
