#ifndef ALPHALAB_ACL07_CANDIDATE_DECISION_MQH
#define ALPHALAB_ACL07_CANDIDATE_DECISION_MQH
#include "ACL07DecisionStatus.mqh"
struct ACL07CandidateDecision { string setup_id; string candidate_id; ENUM_ACL07_DECISION_STATUS status; bool promotion_allowed; bool capital_allowed; };
#endif
