#ifndef FP_SAEDV430ASSIGNMENT_MQH
#define FP_SAEDV430ASSIGNMENT_MQH
struct FP_SAEDV430Assignment { string assignment_id; string lab_id; string package_id; string blind_code; int maximum_runs; bool candidate_identity_visible; bool hidden_labels_visible; };
bool FP_SAEDV430AssignmentValid(const FP_SAEDV430Assignment &value) { return(value.maximum_runs==1 && !value.candidate_identity_visible && !value.hidden_labels_visible); }
#endif
