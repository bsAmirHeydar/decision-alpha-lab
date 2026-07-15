#ifndef DECISION_ALPHA_LAB_SAED_V410_TYPES_MQH
#define DECISION_ALPHA_LAB_SAED_V410_TYPES_MQH
struct SAEDV410Predicate { string feature_ref; string op; string expected; string missing_policy; };
struct SAEDV410Rule { string rule_id; int priority; SAEDV410Predicate predicates[]; string projected_node_id; string reason_code; };
struct SAEDV410Trace { string program_hash; string projected_node_id; string matched_rule_id; string reason_code; bool selection_authority; bool execution_authority; };
#endif
