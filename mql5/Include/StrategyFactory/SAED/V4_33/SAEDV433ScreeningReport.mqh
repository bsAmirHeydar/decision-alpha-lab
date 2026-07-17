#ifndef SAEDV433SCREENINGREPORT_MQH
#define SAEDV433SCREENINGREPORT_MQH
// SAED_V4_33 — outlier screening mirror. Static contract mirror only.
#define SAED_V4_33_RESEARCH_ONLY true
#define SAED_V4_33_PROMOTION_AUTHORITY false
#define SAED_V4_33_EXECUTION_AUTHORITY false
#define SAED_V4_33_PRODUCTION_AUTHORITY false
struct SAEDV433ReferenceReceipt { string artifact_id; string artifact_hash; bool accepted_reference; };
#endif
