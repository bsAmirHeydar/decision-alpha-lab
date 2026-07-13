#ifndef UCEI08_BENCHMARK_CONTRACTS_MQH
#define UCEI08_BENCHMARK_CONTRACTS_MQH
#include "UCEI08_Enums.mqh"
struct UCEI08_BenchmarkObservation{string observation_id;string case_id;string algorithm_key;UCEI08_AlgorithmFamily family;UCEI08_BenchmarkStatus status;string primary_metric;double primary_value;string calibration_method;double calibration_value;long fit_ms;long predict_ms;double peak_memory_mb;bool deterministic_rerun;bool serializable;bool exportable;bool explanation_available;string oof_evidence_hash;string final_test_evidence_hash;string error_code;string error_message;};
struct UCEI08_ClassicalGate{string gate_id;string context_id;string report_id;UCEI08_GateState state;bool has_baseline;bool has_linear;bool has_tree;bool probability_disclosed;bool optional_failures_clean;string blockers_csv;string warnings_csv;bool Passed()const{return state==UCEI08_GATE_PASS && has_baseline && has_linear && has_tree && probability_disclosed && optional_failures_clean;}};
#endif
