#ifndef DECISION_ALPHA_LAB_SAED_V410_BASELINE_MQH
#define DECISION_ALPHA_LAB_SAED_V410_BASELINE_MQH
struct SAEDV410BaselineEntry { string baseline_key; string projected_node_id; bool frozen; bool outcome_fitted; };
bool SAEDV410BaselineIsAdmissible(const SAEDV410BaselineEntry &entry){return entry.frozen && !entry.outcome_fitted && StringLen(entry.projected_node_id)>0;}
#endif
