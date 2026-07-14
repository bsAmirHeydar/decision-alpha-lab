#ifndef __FP_I14_HEALTH_DASHBOARD_MQH__
#define __FP_I14_HEALTH_DASHBOARD_MQH__
#include "FP_I14_Contracts.mqh"
string FP_I14_HealthText(const FP_I14_HealthSnapshot &h){return "FP-I14 DIAGNOSTIC\nIndicator events: "+(string)h.indicator_events+"\nEA events: "+(string)h.ea_events+"\nMismatches: "+(string)h.mismatches+"\nReason: "+h.reason_code;}
#endif
