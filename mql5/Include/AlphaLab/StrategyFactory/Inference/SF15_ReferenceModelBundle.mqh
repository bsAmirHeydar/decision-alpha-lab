#ifndef __SF15_REFERENCE_MODEL_BUNDLE_MQH__
#define __SF15_REFERENCE_MODEL_BUNDLE_MQH__
#include "SF15_OnnxModelManifest.mqh"
#include "SF15_FeatureOrder.mqh"
#include "SF15_Preprocessing.mqh"
#include "SF15_Calibration.mqh"
void SF15_ReferenceManifest(SF15_OnnxModelManifest &m)
  {
   m.export_id="oxpt_7e63ded84fc9888d";m.model_id="sf15.reference.linear_classifier";m.model_version="1.0.0";m.release_hash="mrel_da0b4459eae24ad0";m.registry_scope_hash="rscope_reference_phase15";m.model_artifact_hash="mart_reference_phase15";
   m.onnx_sha256="3e0fa5825e5656cfefdcf34bb9e05e1844ab231c8dbb74150619068c392fcac8";m.onnx_fnv1a64="1e623513209288b3";m.onnx_size_bytes=269;m.feature_schema_hash="fvec_b0f3a1edd021edee";m.feature_order_hash="ford_9ae1141c6d2f1b1d";m.transform_hash="xform_bb9fb122fd545bcc";m.preprocessing_manifest_hash="prep_0a2d9c471003c4a6";m.calibration_hash="cal_a8e1f8e97506568a";m.input_contract_hash="tens_4f7ea306375d3d3a";m.output_contract_hash="tens_af4bf8033a09c95b";m.output_semantics=SF15_OUTPUT_BINARY_LOGIT;m.opset=13;m.ir_version=8;m.graph_name="AlphaLabLinearScalarV1";m.relative_model_path="StrategyFactory/Models/phase15/reference_linear_classifier.onnx";m.minimum_terminal_build=3900;m.generated_at_utc_msc=1783771200000;m.code_revision="phase15-reference";m.manifest_hash="omnf_d07081ff8fb2361e";
  }
bool SF15_ConfigureReferenceOrder(CSF15FeatureOrder &order,string &error)
  {
   SF15_FeatureBinding items[4];
   items[0].feature_id="ref.range_position";items[0].feature_version="1.0.0";items[0].ordinal=0;items[0].value_type="float32";items[0].required=true;
   items[1].feature_id="ref.body_fraction";items[1].feature_version="1.0.0";items[1].ordinal=1;items[1].value_type="float32";items[1].required=true;
   items[2].feature_id="ref.displacement_atr";items[2].feature_version="1.0.0";items[2].ordinal=2;items[2].value_type="float32";items[2].required=true;
   items[3].feature_id="ref.session_progress";items[3].feature_version="1.0.0";items[3].ordinal=3;items[3].value_type="float32";items[3].required=true;
   return order.Configure("fvec_b0f3a1edd021edee","ford_9ae1141c6d2f1b1d",items,error);
  }
bool SF15_ConfigureReferencePreprocessor(CSF15Preprocessor &p,string &error)
  {double impute[4]={0.0,0.0,0.0,0.5};double means[4]={0.1,-0.2,0.3,0.5};double scales[4]={1.2,0.8,2.0,0.25};return p.Configure("fvec_b0f3a1edd021edee","xform_bb9fb122fd545bcc","prep_0a2d9c471003c4a6",impute,means,scales,error);}
void SF15_ReferenceCalibration(SF15_CalibrationContract &c){c.method=SF15_CALIBRATION_SIGMOID;c.a=1.0;c.b=0.0;c.threshold=0.55;c.calibration_hash="cal_a8e1f8e97506568a";}
void SF15_ReferenceWeights(double &weights[],double &bias){ArrayResize(weights,4);weights[0]=0.75;weights[1]=-0.5;weights[2]=0.25;weights[3]=1.1;bias=-0.15;}
#endif
