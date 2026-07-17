#ifndef ALPHALAB_ACL05_HANDOFF_CONTRACT_MQH
#define ALPHALAB_ACL05_HANDOFF_CONTRACT_MQH
struct ACL05ToACL06Handoff { string handoff_type; string batch_id; string handoff_digest; string batch_manifest_digest; string object_index_digest; bool order_submission_allowed; bool capital_activation_allowed; };
bool ACL05HandoffValid(const ACL05ToACL06Handoff &x){ return x.handoff_type=="ACL05_TO_ACL06" && StringLen(x.batch_id)>0 && StringLen(x.handoff_digest)==71 && StringLen(x.batch_manifest_digest)==71 && StringLen(x.object_index_digest)==71 && !x.order_submission_allowed && !x.capital_activation_allowed; }
#endif
