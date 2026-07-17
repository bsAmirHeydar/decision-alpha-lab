#ifndef FP_SAEDV430DISAGREEMENT_MQH
#define FP_SAEDV430DISAGREEMENT_MQH
#include "FP_SAEDV430Constants.mqh"
struct FP_SAEDV430Disagreement { int unresolved_count; bool accepted; int safe_status; };
bool FP_SAEDV430DisagreementFailClosed(const FP_SAEDV430Disagreement &value) { return((value.unresolved_count==0 && value.accepted) || (value.unresolved_count>0 && !value.accepted && value.safe_status==FP_SAEDV430_STATUS_QUARANTINED)); }
#endif
