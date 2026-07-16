#ifndef DECISION_ALPHA_LAB_SAED_V4_14_CONFORMANCE_MQH
#define DECISION_ALPHA_LAB_SAED_V4_14_CONFORMANCE_MQH
#include "SAEDV414AuthorityBoundary.mqh"
#include "SAEDV414FallbackPolicy.mqh"
#include "SAEDV414QuantileGuard.mqh"
bool SAEDV414StaticConformance(){if(SAEDV414AuthorityBoundary::CanPredictOutcome())return false;if(SAEDV414AuthorityBoundary::CanSelectTreatment())return false;if(SAEDV414ResolveFallback(false,false,true)!=V414_NATIVE_BASELINE)return false;return true;}
#endif
