#ifndef ALPHALAB_ACL10_STATE_DECISION_CONTRACT_MQH
#define ALPHALAB_ACL10_STATE_DECISION_CONTRACT_MQH
#include "ACL10StateIds.mqh"
struct ACL10StateDecisionContract { string decision_id; string subject_id; ENUM_ACL10_STATE state; bool promotion_review_eligible; bool promotion_executed; };
#endif
