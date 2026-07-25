#ifndef ALPHALAB_ACL06_DAG_CONTRACT_MQH
#define ALPHALAB_ACL06_DAG_CONTRACT_MQH
struct ACL06DAGContract { string plan_id; string dag_digest; int task_count; bool closed; bool batch_mutation_allowed; bool candidate_mutation_allowed; };
#endif
