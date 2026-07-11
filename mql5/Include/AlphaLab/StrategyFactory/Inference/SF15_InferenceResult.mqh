#ifndef __SF15_INFERENCE_RESULT_MQH__
#define __SF15_INFERENCE_RESULT_MQH__
#include "SF15_InferenceEnums.mqh"
struct SF15_InferenceResult
  {
   string result_id,request_id,model_id,model_version,release_hash,manifest_hash;ENUM_SF15_INFERENCE_STATUS status;double raw_score,calibrated_score,threshold;int predicted_class;long inference_time_utc_msc,latency_micros;ENUM_SF15_RUNTIME_BACKEND backend;int error_code;string error_message,result_hash;
   void Reset(){result_id="";request_id="";model_id="";model_version="";release_hash="";manifest_hash="";status=SF15_INFERENCE_REJECTED;raw_score=0.0;calibrated_score=0.0;threshold=0.5;predicted_class=0;inference_time_utc_msc=0;latency_micros=0;backend=SF15_BACKEND_REFERENCE;error_code=0;error_message="";result_hash="";}
  };
#endif
