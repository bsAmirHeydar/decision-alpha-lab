#ifndef __SF15_CALIBRATION_MQH__
#define __SF15_CALIBRATION_MQH__
#include "SF15_InferenceEnums.mqh"
#include "SF15_Hashing.mqh"
struct SF15_CalibrationContract
  {
   ENUM_SF15_CALIBRATION_METHOD method; double a,b,threshold; string calibration_hash;
   bool Validate(string &error)const{if(!SF15_IsFinite(a)||!SF15_IsFinite(b)||!SF15_IsFinite(threshold)||threshold<0.0||threshold>1.0||calibration_hash==""){error="invalid calibration contract";return false;}error="";return true;}
   bool Apply(const double raw,double &calibrated,string &error)const
     {
      if(!Validate(error)||!SF15_IsFinite(raw))return false;
      if(method==SF15_CALIBRATION_IDENTITY)calibrated=raw;
      else if(method==SF15_CALIBRATION_SIGMOID||method==SF15_CALIBRATION_PLATT){double z=a*raw+b;if(z>745.0)calibrated=1.0;else if(z<-745.0)calibrated=0.0;else calibrated=1.0/(1.0+MathExp(-z));}
      else{error="unsupported calibration method";return false;}
      if(!SF15_IsFinite(calibrated)){error="non-finite calibration output";return false;}error="";return true;
     }
  };
#endif
