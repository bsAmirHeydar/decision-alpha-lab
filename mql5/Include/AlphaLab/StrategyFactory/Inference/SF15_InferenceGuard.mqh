#ifndef __SF15_INFERENCE_GUARD_MQH__
#define __SF15_INFERENCE_GUARD_MQH__
#include "SF15_OnnxModelManifest.mqh"
#include "SF15_FeatureOrder.mqh"
#include "SF15_Preprocessing.mqh"
#include "SF15_Calibration.mqh"
#include "SF15_InferenceRequest.mqh"
class CSF15InferenceGuard
  {
private: bool m_ready;string m_error;
public:
   CSF15InferenceGuard(){m_ready=false;m_error="not validated";}
   bool ValidateStartup(const SF15_OnnxModelManifest &manifest,const CSF15FeatureOrder &order,const CSF15Preprocessor &preprocessor,const SF15_CalibrationContract &calibration,const long actual_size,const string actual_fnv,const int terminal_build,string &error)
     {
      string e;if(!manifest.Validate(e)){error=e;m_error=e;m_ready=false;return false;}
      if(terminal_build<manifest.minimum_terminal_build){error="terminal build below release minimum";m_error=error;m_ready=false;return false;}
      string actual_fingerprint=actual_fnv;string expected_fingerprint=manifest.onnx_fnv1a64;StringToLower(actual_fingerprint);StringToLower(expected_fingerprint);
      if(actual_size!=manifest.onnx_size_bytes||actual_fingerprint!=expected_fingerprint){error="model file fingerprint mismatch";m_error=error;m_ready=false;return false;}
      if(!order.Matches(manifest.feature_schema_hash,manifest.feature_order_hash,preprocessor.Width())){error="feature-order lineage mismatch";m_error=error;m_ready=false;return false;}
      if(!preprocessor.Ready()||preprocessor.TransformHash()!=manifest.transform_hash||preprocessor.ManifestHash()!=manifest.preprocessing_manifest_hash){error="preprocessing lineage mismatch";m_error=error;m_ready=false;return false;}
      if(!calibration.Validate(e)||calibration.calibration_hash!=manifest.calibration_hash){error="calibration lineage mismatch";m_error=error;m_ready=false;return false;}
      m_ready=true;m_error="";error="";return true;
     }
   bool ValidateRequest(const SF15_InferenceRequest &request,const CSF15FeatureOrder &order,string &error)const
     {if(!m_ready){error="inference guard is not ready";return false;}if(!request.Validate(order.Width(),error))return false;if(!order.Matches(request.feature_schema_hash,request.feature_order_hash,ArraySize(request.values))){error="request lineage mismatch";return false;}error="";return true;}
   bool Ready()const{return m_ready;}string LastError()const{return m_error;}
  };
#endif
