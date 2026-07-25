#ifndef ALPHALAB_ACL06_HANDOFF_CONTRACT_MQH
#define ALPHALAB_ACL06_HANDOFF_CONTRACT_MQH
struct ACL06Handoff { string handoff_type; string handoff_digest; string run_id; string batch_id; string result_bundle_digest; bool order_allowed; bool capital_allowed; };
#endif
