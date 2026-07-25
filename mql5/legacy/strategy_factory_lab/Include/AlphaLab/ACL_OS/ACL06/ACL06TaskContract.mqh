#ifndef ALPHALAB_ACL06_TASK_CONTRACT_MQH
#define ALPHALAB_ACL06_TASK_CONTRACT_MQH
struct ACL06TaskContract { string task_id; string task_contract_digest; string cache_key; int task_type; bool deterministic; bool idempotent; };
#endif
