#ifndef DECISION_ALPHA_LAB_SAED_V4_14_TYPES_MQH
#define DECISION_ALPHA_LAB_SAED_V4_14_TYPES_MQH
#include "SAEDV414Version.mqh"
enum SAEDV414Fallback { V414_FEATURE=0, V414_NATIVE_BASELINE=1, V414_ABSTAIN=2, V414_QUARANTINE=3 };
struct SAEDV414FeatureEnvelope { string feature_id; string feature_hash; string known_as_of; double uncertainty_scale; bool supported; bool runtime_authority; };
#endif
