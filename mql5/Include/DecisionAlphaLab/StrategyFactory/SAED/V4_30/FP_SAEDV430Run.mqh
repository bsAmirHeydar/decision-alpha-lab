#ifndef FP_SAEDV430RUN_MQH
#define FP_SAEDV430RUN_MQH
struct FP_SAEDV430Run { string run_id; string lab_id; string assignment_id; int run_ordinal; int retry_count; bool network_access; bool interactive_adaptation; int future_suffix_records_seen; };
bool FP_SAEDV430RunValid(const FP_SAEDV430Run &value) { return(value.run_ordinal==1 && value.retry_count==0 && !value.network_access && !value.interactive_adaptation && value.future_suffix_records_seen==0); }
#endif
