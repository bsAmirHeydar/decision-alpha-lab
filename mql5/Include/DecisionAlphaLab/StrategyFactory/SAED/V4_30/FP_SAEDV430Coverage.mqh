#ifndef FP_SAEDV430COVERAGE_MQH
#define FP_SAEDV430COVERAGE_MQH
struct FP_SAEDV430Coverage { int lab_count; int pair_count; int environment_count; int run_count; int result_count; bool complete; bool external_lab_coverage; };
bool FP_SAEDV430CoverageReferenceValid(const FP_SAEDV430Coverage &value) { return(value.lab_count>=3 && value.pair_count>=3 && value.environment_count==value.lab_count && value.run_count==value.lab_count && value.result_count==value.lab_count && value.complete && !value.external_lab_coverage); }
#endif
