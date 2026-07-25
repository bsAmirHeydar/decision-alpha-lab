#ifndef ALPHALAB_ACL06_RESULT_CONTRACT_MQH
#define ALPHALAB_ACL06_RESULT_CONTRACT_MQH
struct ACL06CandidateResult { string setup_id; string candidate_digest; string result_digest; int support; int signals; bool descriptive_only; bool promotion_allowed; };
#endif
