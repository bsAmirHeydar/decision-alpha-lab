#ifndef __SF15_INFERENCE_REQUEST_MQH__
#define __SF15_INFERENCE_REQUEST_MQH__
#include "SF15_Hashing.mqh"
struct SF15_InferenceRequest
  {
   string request_id,run_id,generation_id,context_frame_id,candidate_id,feature_schema_hash,feature_order_hash;long known_time_utc_msc,decision_time_utc_msc;double values[];bool missing[];string request_hash;
   bool Validate(const int expected_width,string &error)const
     {
      if(request_id==""||run_id==""||generation_id==""||context_frame_id==""||candidate_id==""||feature_schema_hash==""||feature_order_hash==""){error="missing inference lineage";return false;}
      if(decision_time_utc_msc<known_time_utc_msc){error="decision precedes known time";return false;}
      if(ArraySize(values)!=expected_width||ArraySize(missing)!=expected_width){error="inference width mismatch";return false;}
      for(int i=0;i<expected_width;i++)if(!missing[i]&&!SF15_IsFinite(values[i])){error="non-finite observed feature";return false;}error="";return true;
     }
  };
#endif
