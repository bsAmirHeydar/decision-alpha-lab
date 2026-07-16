#ifndef __SAED_V4_25_TYPES_MQH__
#define __SAED_V4_25_TYPES_MQH__
enum ENUM_SAEDV425_DRIFT_CLASS { SAEDV425_STATIONARY=0, SAEDV425_GRADUAL=1, SAEDV425_SUDDEN=2, SAEDV425_RECURRING=3, SAEDV425_NOVEL=4 };
enum ENUM_SAEDV425_PATH { SAEDV425_SCRATCH_BASELINE=0, SAEDV425_TRANSFER_CANDIDATE=1 };
struct SAEDV425Authority { bool decision; bool promotion; bool runtime; bool risk_allocation; bool execution; bool order_submission; bool production; bool online_learning; };
struct SAEDV425TaskIdentity { string task_id; string context_id; string cluster_id; string regime; datetime decision_time; };
struct SAEDV425TransferEdge { string source_task_id; string target_task_id; double distance; double weight; bool eligible; };
struct SAEDV425GuardDecision { string task_id; ENUM_SAEDV425_PATH selected_path; bool accepted_for_research; string reason; };
#endif
