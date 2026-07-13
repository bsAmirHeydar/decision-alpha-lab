#ifndef ALPHALAB_UCEI14_FAILURE
#define ALPHALAB_UCEI14_FAILURE
#include "UCEI14_Contracts.mqh"
bool UCEI14CriticalFailure(const string code){return(code=="corrupt_artifact"||code=="feature_order_mismatch"||code=="signature_failure"||code=="parity_failure"||code=="restart_reconciliation"||code=="kill_switch");}
string UCEI14FailureDisposition(const string code){if(code=="corrupt_artifact")return("quarantine_bundle");if(code=="feature_order_mismatch"||code=="signature_failure"||code=="parity_failure")return("refuse_activation");if(code=="kill_switch")return("reject");return("abstain_and_alert");}
#endif
