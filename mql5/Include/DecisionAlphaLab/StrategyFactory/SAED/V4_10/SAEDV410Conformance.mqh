#ifndef DECISION_ALPHA_LAB_SAED_V410_CONFORMANCE_MQH
#define DECISION_ALPHA_LAB_SAED_V410_CONFORMANCE_MQH
#include "SAEDV410Authority.mqh"
bool SAEDV410AuthorityConforms(){return SAEDV410CanCompileManualProgram() && !SAEDV410CanTrainModel() && !SAEDV410CanSelectTreatment() && !SAEDV410CanAllocateRisk() && !SAEDV410CanSendOrder();}
#endif
