#ifndef __UCEI09_COMPARISON_CONTRACTS_MQH__
#define __UCEI09_COMPARISON_CONTRACTS_MQH__
#include "UCEI09_Enums.mqh"
struct UCEI09_TaskComparisonObservation{string observation_id;string context_id;UCEI09_TASK_FAMILY family;string algorithm_key;string status;string primary_metric;double primary_value;double economic_utility;double calibration_value;UCEI09_GATE_DECISION support_gate;bool deterministic;int fit_ms;int predict_ms;string artifact_hash;};
struct UCEI09_TaskComparisonReport{string report_id;string context_id;string dataset_manifest_hash;bool promotion_ready;string blockers[];string warnings[];string evidence_hash;};
#endif
