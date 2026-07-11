#ifndef __SF15_ONNX_MODEL_MANIFEST_MQH__
#define __SF15_ONNX_MODEL_MANIFEST_MQH__
#include "SF15_InferenceEnums.mqh"
struct SF15_OnnxModelManifest
  {
   string export_id,model_id,model_version,release_hash,registry_scope_hash,model_artifact_hash;
   string onnx_sha256,onnx_fnv1a64; long onnx_size_bytes;
   string feature_schema_hash,feature_order_hash,transform_hash,preprocessing_manifest_hash,calibration_hash,input_contract_hash,output_contract_hash;
   ENUM_SF15_OUTPUT_SEMANTICS output_semantics; int opset,ir_version;string graph_name,relative_model_path;int minimum_terminal_build;long generated_at_utc_msc;string code_revision,manifest_hash;
   bool Validate(string &error)const
     {
      if(export_id==""||model_id==""||model_version==""||release_hash==""||onnx_sha256==""||onnx_fnv1a64==""||onnx_size_bytes<1||feature_schema_hash==""||feature_order_hash==""||transform_hash==""||preprocessing_manifest_hash==""||calibration_hash==""||input_contract_hash==""||output_contract_hash==""||graph_name==""||relative_model_path==""||minimum_terminal_build<1||manifest_hash==""){error="incomplete ONNX manifest";return false;}
      if(StringLen(onnx_sha256)!=64||StringLen(onnx_fnv1a64)!=16||opset<7||ir_version<3){error="unsupported ONNX metadata";return false;}error="";return true;
     }
  };
#endif
