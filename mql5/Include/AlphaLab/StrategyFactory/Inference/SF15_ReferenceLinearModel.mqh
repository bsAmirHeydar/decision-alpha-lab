#ifndef __SF15_REFERENCE_LINEAR_MODEL_MQH__
#define __SF15_REFERENCE_LINEAR_MODEL_MQH__
#include "SF15_Hashing.mqh"
class CSF15ReferenceLinearModel
  {
private: double m_weights[],m_bias;bool m_ready;
public:
   CSF15ReferenceLinearModel(){m_bias=0.0;m_ready=false;}
   bool Configure(const double &weights[],const double bias,string &error){if(ArraySize(weights)<1||!SF15_IsFinite(bias)){error="invalid reference model";return false;}ArrayResize(m_weights,ArraySize(weights));for(int i=0;i<ArraySize(weights);i++){if(!SF15_IsFinite(weights[i])){error="non-finite model weight";return false;}m_weights[i]=weights[i];}m_bias=bias;m_ready=true;error="";return true;}
   bool Run(const double &features[],double &score,string &error)const{if(!m_ready||ArraySize(features)!=ArraySize(m_weights)){error="reference model width mismatch";return false;}score=m_bias;for(int i=0;i<ArraySize(features);i++)score+=features[i]*m_weights[i];if(!SF15_IsFinite(score)){error="non-finite reference score";return false;}error="";return true;}
  };
#endif
