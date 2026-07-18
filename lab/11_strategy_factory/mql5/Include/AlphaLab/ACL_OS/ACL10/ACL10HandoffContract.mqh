#ifndef ALPHALAB_ACL10_HANDOFF_CONTRACT_MQH
#define ALPHALAB_ACL10_HANDOFF_CONTRACT_MQH
struct ACL10HandoffContract { string handoff_type; string promotion_run_id; int runtime_candidate_count; bool runtime_generation_allowed; bool live_order_submission_allowed; bool capital_activation_allowed; };
#endif
