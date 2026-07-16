#ifndef DECISION_ALPHA_LAB_SAED_V4_14_FALLBACK_POLICY_MQH
#define DECISION_ALPHA_LAB_SAED_V4_14_FALLBACK_POLICY_MQH
#include "SAEDV414Types.mqh"
SAEDV414Fallback SAEDV414ResolveFallback(const bool intake_admitted,const bool domain_supported,const bool baseline_available){if(intake_admitted && domain_supported)return V414_FEATURE;if(baseline_available)return V414_NATIVE_BASELINE;return V414_ABSTAIN;}
#endif
