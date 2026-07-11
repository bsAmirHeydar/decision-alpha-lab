#ifndef __SF15_PARITY_MQH__
#define __SF15_PARITY_MQH__
#include "SF15_InferenceEnums.mqh"
struct SF15_ParityVector{string vector_id;double values[];bool missing[];double expected_transformed[];double expected_raw_score,expected_calibrated_score;int expected_class;string vector_hash;};
struct SF15_ParityReport{string report_id,manifest_hash;ENUM_SF15_RUNTIME_BACKEND backend;int vector_count,passed_count,failed_count;double maximum_raw_abs_error,maximum_calibrated_abs_error,raw_tolerance,calibrated_tolerance;ENUM_SF15_PARITY_VERDICT verdict;string report_hash;};
#endif
