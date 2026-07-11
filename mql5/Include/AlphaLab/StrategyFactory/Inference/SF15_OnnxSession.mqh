#ifndef __SF15_ONNX_SESSION_MQH__
#define __SF15_ONNX_SESSION_MQH__
#include "SF15_Hashing.mqh"
class CSF15OnnxSession
  {
private: long m_handle;int m_width;bool m_ready;string m_error;
public:
   CSF15OnnxSession(){m_handle=INVALID_HANDLE;m_width=0;m_ready=false;m_error="not opened";}
   ~CSF15OnnxSession(){Close();}
   void Close(){if(m_handle!=INVALID_HANDLE){OnnxRelease(m_handle);m_handle=INVALID_HANDLE;}m_width=0;m_ready=false;}
   bool Open(const string relative_path,const bool common_folder,const bool cpu_only,const int feature_width,string &error)
     {
      Close();if(feature_width<1){error="invalid feature width";m_error=error;return false;}
      uint flags=ONNX_LOGLEVEL_WARNING;if(common_folder)flags|=ONNX_COMMON_FOLDER;if(cpu_only)flags|=ONNX_USE_CPU_ONLY;
      ResetLastError();m_handle=OnnxCreate(relative_path,flags);if(m_handle==INVALID_HANDLE){error="OnnxCreate failed: "+IntegerToString(GetLastError());m_error=error;return false;}
      ulong input_shape[2];input_shape[0]=1;input_shape[1]=(ulong)feature_width;ulong output_shape[2];output_shape[0]=1;output_shape[1]=1;
      if(!OnnxSetInputShape(m_handle,0,input_shape)){error="OnnxSetInputShape failed: "+IntegerToString(GetLastError());Close();m_error=error;return false;}
      if(!OnnxSetOutputShape(m_handle,0,output_shape)){error="OnnxSetOutputShape failed: "+IntegerToString(GetLastError());Close();m_error=error;return false;}
      m_width=feature_width;m_ready=true;m_error="";error="";return true;
     }
   bool Run(const double &features[],double &score,int &runtime_error,string &error)
     {
      runtime_error=0;score=0.0;if(!m_ready||ArraySize(features)!=m_width){error="ONNX session is not ready or width mismatched";return false;}
      matrixf input(1,m_width);for(int i=0;i<m_width;i++){if(!SF15_IsFinite(features[i])){error="non-finite ONNX input";return false;}input[0][i]=(float)features[i];}
      vectorf output(1);ResetLastError();if(!OnnxRun(m_handle,ONNX_NO_CONVERSION,input,output)){runtime_error=GetLastError();error="OnnxRun failed: "+IntegerToString(runtime_error);return false;}
      score=(double)output[0];if(!SF15_IsFinite(score)){error="ONNX returned non-finite score";return false;}error="";return true;
     }
   bool Ready()const{return m_ready;}string LastError()const{return m_error;}
  };
#endif
