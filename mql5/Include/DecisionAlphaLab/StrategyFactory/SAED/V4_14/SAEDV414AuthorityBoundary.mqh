#ifndef DECISION_ALPHA_LAB_SAED_V4_14_AUTHORITY_MQH
#define DECISION_ALPHA_LAB_SAED_V4_14_AUTHORITY_MQH
#include "SAEDV414Types.mqh"
class SAEDV414AuthorityBoundary { public: static bool CanPredictOutcome(){return false;} static bool CanSelectTreatment(){return false;} static bool CanAllocateRisk(){return false;} static bool CanSendOrder(){return false;} static bool CanConsumeFrozenFeature(){return true;} };
#endif
