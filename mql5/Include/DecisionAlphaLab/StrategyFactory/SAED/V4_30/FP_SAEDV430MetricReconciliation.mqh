#ifndef FP_SAEDV430METRICRECONCILIATION_MQH
#define FP_SAEDV430METRICRECONCILIATION_MQH
struct FP_SAEDV430MetricReconciliation { int comparison_count; bool all_within_tolerance; bool baseline_preserved; };
bool FP_SAEDV430MetricAccepted(const FP_SAEDV430MetricReconciliation &value) { return(value.comparison_count>=9 && value.all_within_tolerance && value.baseline_preserved); }
#endif
