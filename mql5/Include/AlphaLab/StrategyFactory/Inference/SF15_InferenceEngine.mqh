#ifndef __SF15_INFERENCE_ENGINE_MQH__
#define __SF15_INFERENCE_ENGINE_MQH__
#include "SF15_InferenceGuard.mqh"
#include "SF15_OnnxSession.mqh"
#include "SF15_InferenceResult.mqh"
class CSF15InferenceEngine
  {
public:
   bool Infer(const SF15_InferenceRequest &request,
              const SF15_OnnxModelManifest &manifest,
              const CSF15FeatureOrder &order,
              const CSF15Preprocessor &preprocessor,
              const SF15_CalibrationContract &calibration,
              const CSF15InferenceGuard &guard,
              CSF15OnnxSession &session,
              SF15_InferenceResult &result)
     {
      result.Reset();
      result.request_id=request.request_id;
      result.model_id=manifest.model_id;
      result.model_version=manifest.model_version;
      result.release_hash=manifest.release_hash;
      result.manifest_hash=manifest.manifest_hash;
      result.threshold=calibration.threshold;
      result.backend=SF15_BACKEND_ONNX;
      result.inference_time_utc_msc=(long)TimeCurrent()*1000;
      string error;
      if(!guard.ValidateRequest(request,order,error))
        {
         result.status=SF15_INFERENCE_LINEAGE_MISMATCH;
         result.error_message=error;
         return false;
        }
      double transformed[];
      if(!preprocessor.Transform(request.values,request.missing,transformed,error))
        {
         result.status=SF15_INFERENCE_REJECTED;
         result.error_message=error;
         return false;
        }
      ulong started=GetMicrosecondCount();
      int runtime_error=0;
      double raw=0.0;
      if(!session.Run(transformed,raw,runtime_error,error))
        {
         result.status=SF15_INFERENCE_RUNTIME_ERROR;
         result.error_code=runtime_error;
         result.error_message=error;
         return false;
        }
      result.latency_micros=(long)(GetMicrosecondCount()-started);
      double calibrated=0.0;
      if(!calibration.Apply(raw,calibrated,error))
        {
         result.status=SF15_INFERENCE_NON_FINITE;
         result.error_message=error;
         return false;
        }
      result.raw_score=raw;
      result.calibrated_score=calibrated;
      result.predicted_class=(calibrated>=calibration.threshold)?1:0;
      result.status=SF15_INFERENCE_ACCEPTED;
      return true;
     }
  };
#endif
