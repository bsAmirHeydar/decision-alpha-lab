#ifndef DECISION_ALPHA_LAB_SAED_V4_14_FEATURE_CONTRACT_MQH
#define DECISION_ALPHA_LAB_SAED_V4_14_FEATURE_CONTRACT_MQH
#include "SAEDV414Types.mqh"
bool SAEDV414ValidateFeature(const SAEDV414FeatureEnvelope &x){ if(x.feature_id=="" || x.feature_hash=="" || x.known_as_of=="") return false; if(x.runtime_authority) return false; if(x.uncertainty_scale<0.0) return false; return true; }
#endif
