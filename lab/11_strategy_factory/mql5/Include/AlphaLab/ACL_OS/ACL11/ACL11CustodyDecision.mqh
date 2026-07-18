#ifndef ALPHALAB_ACL11_CUSTODY_DECISION_MQH
#define ALPHALAB_ACL11_CUSTODY_DECISION_MQH
struct ACL11CustodyDecision { string decision_id; ENUM_ACL11_CUSTODY_STATE state; int runtime_candidate_count; bool executable; };
#endif
