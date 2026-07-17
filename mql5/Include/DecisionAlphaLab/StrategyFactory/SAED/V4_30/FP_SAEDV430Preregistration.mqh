#ifndef FP_SAEDV430PREREGISTRATION_MQH
#define FP_SAEDV430PREREGISTRATION_MQH
struct FP_SAEDV430Preregistration { string preregistration_id; string lab_id; string assignment_id; datetime preregistered_at; datetime assignment_opened_at; datetime run_not_before; int maximum_runs; bool adaptive_changes_allowed; };
bool FP_SAEDV430PreregistrationOrdered(const FP_SAEDV430Preregistration &value) { return(value.preregistered_at<value.assignment_opened_at && value.assignment_opened_at<value.run_not_before && value.maximum_runs==1 && !value.adaptive_changes_allowed); }
#endif
