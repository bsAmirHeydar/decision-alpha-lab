#property strict
#include <AlphaLab/StrategyFactory/Inference/SF15_AllInference.mqh>
input bool InpUseCommonFolder=false;

void SF15_LoadParityVector(const int index,double &values[],bool &missing[],double &expected_raw,double &expected_probability,int &expected_class)
  {
   ArrayResize(values,4);ArrayResize(missing,4);
   for(int i=0;i<4;i++)missing[i]=false;
   if(index==0){values[0]=0.1;values[1]=-0.2;values[2]=0.3;values[3]=0.5;expected_raw=-0.15;expected_probability=0.46257015465625045;expected_class=0;}
   else if(index==1){values[0]=0.9;values[1]=0.4;values[2]=1.5;values[3]=0.8;expected_raw=1.445;expected_probability=0.8092277361600781;expected_class=1;}
   else if(index==2){values[0]=-0.4;values[1]=-0.8;values[2]=-1.0;values[3]=0.2;expected_raw=-1.57;expected_probability=0.17221639173387782;expected_class=0;}
   else if(index==3){values[0]=0.0;values[1]=0.0;values[2]=0.0;values[3]=0.0;missing[0]=true;missing[1]=true;missing[2]=true;missing[3]=true;expected_raw=-0.375;expected_probability=0.40733340004593027;expected_class=0;}
   else if(index==4){values[0]=0.6;values[1]=0.1;values[2]=0.0;values[3]=0.75;missing[1]=true;expected_raw=1.1;expected_probability=0.7502601055951177;expected_class=1;}
   else if(index==5){values[0]=-1.2;values[1]=1.0;values[2]=2.5;values[3]=0.1;missing[2]=true;expected_raw=-3.51;expected_probability=0.02902903583634076;expected_class=0;}
   else if(index==6){values[0]=2.0;values[1]=-1.5;values[2]=0.75;values[3]=1.0;expected_raw=4.10625;expected_probability=0.983797427761907;expected_class=1;}
   else {values[0]=0.05;values[1]=-0.1;values[2]=0.25;values[3]=0.48;expected_raw=-0.338;expected_probability=0.4162953826316074;expected_class=0;}
  }

int OnInit()
  {
   SF15_OnnxModelManifest manifest;SF15_ReferenceManifest(manifest);string error;
   CSF15Preprocessor preprocessor;if(!SF15_ConfigureReferencePreprocessor(preprocessor,error)){Print(error);return INIT_FAILED;}
   SF15_CalibrationContract calibration;SF15_ReferenceCalibration(calibration);
   CSF15OnnxSession session;if(!session.Open(manifest.relative_model_path,InpUseCommonFolder,true,4,error)){Print(error);return INIT_FAILED;}
   const double raw_tolerance=1e-5;const double probability_tolerance=1e-5;
   for(int index=0;index<8;index++)
     {
      double values[];bool missing[];double expected_raw=0.0,expected_probability=0.0;int expected_class=0;
      SF15_LoadParityVector(index,values,missing,expected_raw,expected_probability,expected_class);
      double transformed[];if(!preprocessor.Transform(values,missing,transformed,error)){Print("vector ",index," preprocess failed: ",error);return INIT_FAILED;}
      double actual_raw=0.0;int runtime_error=0;if(!session.Run(transformed,actual_raw,runtime_error,error)){Print("vector ",index," ONNX failed: ",error);return INIT_FAILED;}
      double actual_probability=0.0;if(!calibration.Apply(actual_raw,actual_probability,error)){Print("vector ",index," calibration failed: ",error);return INIT_FAILED;}
      int actual_class=(actual_probability>=calibration.threshold)?1:0;
      if(MathAbs(actual_raw-expected_raw)>raw_tolerance || MathAbs(actual_probability-expected_probability)>probability_tolerance || actual_class!=expected_class)
        {
         Print("SF15 parity mismatch vector=",index," raw=",DoubleToString(actual_raw,12)," expected_raw=",DoubleToString(expected_raw,12)," p=",DoubleToString(actual_probability,12)," expected_p=",DoubleToString(expected_probability,12)," class=",actual_class," expected_class=",expected_class);
         return INIT_FAILED;
        }
     }
   Print("SF15 ONNX runtime parity PASS: 8/8 vectors");return INIT_SUCCEEDED;
  }
void OnDeinit(const int reason){}
void OnTick(){}
