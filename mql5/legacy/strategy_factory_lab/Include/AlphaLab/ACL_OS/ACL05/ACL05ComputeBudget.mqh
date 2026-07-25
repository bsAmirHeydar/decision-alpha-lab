#ifndef ALPHALAB_ACL05_COMPUTE_BUDGET_MQH
#define ALPHALAB_ACL05_COMPUTE_BUDGET_MQH
struct ACL05ComputeBudget { string budget_id; string budget_digest; int max_tasks; long max_cpu_seconds; long max_memory_mb; long max_store_bytes; int max_store_objects; };
bool ACL05BudgetValid(const ACL05ComputeBudget &x){ return x.max_tasks>0 && x.max_cpu_seconds>0 && x.max_memory_mb>0 && x.max_store_bytes>0 && x.max_store_objects>0 && StringLen(x.budget_digest)==71; }
#endif
