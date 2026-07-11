#property strict
#include <AlphaLab/StrategyFactory/Inference/SF15_AllInference.mqh>
input bool InpUseCommonFolder=false;
input bool InpCpuOnly=true;
int OnInit()
  {
   SF15_OnnxModelManifest manifest;SF15_ReferenceManifest(manifest);string error;long size=0;string fingerprint="";
   if(!SF15_ReadModelFingerprint(manifest.relative_model_path,InpUseCommonFolder,size,fingerprint,error)){Print("SF15 diagnostic: ",error);return INIT_FAILED;}
   Print("SF15 model file size=",size," fnv1a64=",fingerprint," expected=",manifest.onnx_fnv1a64);
   CSF15OnnxSession session;if(!session.Open(manifest.relative_model_path,InpUseCommonFolder,InpCpuOnly,4,error)){Print("SF15 diagnostic: ",error);return INIT_FAILED;}
   double input[4]={0.6666666666666666,0.75,0.6,1.2};double score=0.0;int runtime_error=0;if(!session.Run(input,score,runtime_error,error)){Print("SF15 diagnostic: ",error);return INIT_FAILED;}
   Print("SF15 ONNX smoke score=",DoubleToString(score,12));return INIT_SUCCEEDED;
  }
void OnDeinit(const int reason){}
void OnTick(){}
