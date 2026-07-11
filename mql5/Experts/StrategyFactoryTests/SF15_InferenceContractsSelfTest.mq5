#property strict
#include <AlphaLab/StrategyFactory/Inference/SF15_AllInference.mqh>
int OnInit()
  {
   string error;CSF15FeatureOrder order;if(!SF15_ConfigureReferenceOrder(order,error)){Print(error);return INIT_FAILED;}
   CSF15Preprocessor prep;if(!SF15_ConfigureReferencePreprocessor(prep,error)){Print(error);return INIT_FAILED;}
   SF15_CalibrationContract cal;SF15_ReferenceCalibration(cal);if(!cal.Validate(error)){Print(error);return INIT_FAILED;}
   double values[4]={0.9,0.4,1.5,0.8};bool missing[4]={false,false,false,false};double transformed[];
   if(!prep.Transform(values,missing,transformed,error)){Print(error);return INIT_FAILED;}
   double weights[],bias;SF15_ReferenceWeights(weights,bias);CSF15ReferenceLinearModel model;if(!model.Configure(weights,bias,error)){Print(error);return INIT_FAILED;}
   double raw=0.0;if(!model.Run(transformed,raw,error)){Print(error);return INIT_FAILED;}double probability=0.0;if(!cal.Apply(raw,probability,error)){Print(error);return INIT_FAILED;}
   if(MathAbs(raw-1.445)>1e-12 || MathAbs(probability-0.809227736160)>1e-9){Print("reference parity failed raw=",raw," p=",probability);return INIT_FAILED;}
   SF15_InferenceRequest request;request.request_id="req";request.run_id="run";request.generation_id="gen";request.context_frame_id="frame";request.candidate_id="candidate";request.feature_schema_hash=order.FeatureSchemaHash();request.feature_order_hash=order.OrderHash();request.known_time_utc_msc=1000;request.decision_time_utc_msc=1000;ArrayCopy(request.values,values);ArrayCopy(request.missing,missing);
   if(!request.Validate(4,error)){Print(error);return INIT_FAILED;}request.feature_order_hash="wrong";CSF15InferenceGuard guard;if(guard.ValidateRequest(request,order,error)){Print("unready guard accepted request");return INIT_FAILED;}
   Print("SF15 inference contracts self-test PASS");return INIT_SUCCEEDED;
  }
void OnDeinit(const int reason){}
void OnTick(){}
