#ifndef FP_SAEDV430RESULT_MQH
#define FP_SAEDV430RESULT_MQH
struct FP_SAEDV430Result { string result_id; string lab_id; string run_id; string semantic_output_hash; double accuracy; double brier; double mean_probability; bool raw_rows_exported; bool hidden_labels_exported; };
bool FP_SAEDV430ResultAggregateOnly(const FP_SAEDV430Result &value) { return(StringLen(value.semantic_output_hash)==64 && !value.raw_rows_exported && !value.hidden_labels_exported); }
#endif
