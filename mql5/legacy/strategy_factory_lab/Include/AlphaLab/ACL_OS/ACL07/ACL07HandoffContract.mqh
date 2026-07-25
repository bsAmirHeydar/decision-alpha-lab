#ifndef ALPHALAB_ACL07_HANDOFF_CONTRACT_MQH
#define ALPHALAB_ACL07_HANDOFF_CONTRACT_MQH
struct ACL07HandoffContract { string validation_id; string decision_bundle_digest; string gate_matrix_digest; bool order_allowed; bool capital_allowed; };
#endif
