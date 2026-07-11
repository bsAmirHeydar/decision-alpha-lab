#property strict
#include <AlphaLab/StrategyFactory/Inference/SF15_AllInference.mqh>
input bool InpUseCommonFolder=false;
input bool InpCpuOnly=true;
CSF15FeatureOrder g_order;CSF15Preprocessor g_preprocessor;SF15_CalibrationContract g_calibration;SF15_OnnxModelManifest g_manifest;CSF15InferenceGuard g_guard;CSF15OnnxSession g_session;CSF15InferenceEngine g_engine;
int OnInit()
  {
   string error;SF15_ReferenceManifest(g_manifest);if(!SF15_ConfigureReferenceOrder(g_order,error)||!SF15_ConfigureReferencePreprocessor(g_preprocessor,error)){Print(error);return INIT_FAILED;}SF15_ReferenceCalibration(g_calibration);
   long size=0;string fingerprint="";if(!SF15_ReadModelFingerprint(g_manifest.relative_model_path,InpUseCommonFolder,size,fingerprint,error)){Print(error);return INIT_FAILED;}
   if(!g_guard.ValidateStartup(g_manifest,g_order,g_preprocessor,g_calibration,size,fingerprint,(int)TerminalInfoInteger(TERMINAL_BUILD),error)){Print(error);return INIT_FAILED;}
   if(!g_session.Open(g_manifest.relative_model_path,InpUseCommonFolder,InpCpuOnly,g_order.Width(),error)){Print(error);return INIT_FAILED;}
   Print("SF15 inference host ready; prediction authority only, no trade/risk/order authority");return INIT_SUCCEEDED;
  }
void OnDeinit(const int reason){g_session.Close();}
void OnTick(){}
