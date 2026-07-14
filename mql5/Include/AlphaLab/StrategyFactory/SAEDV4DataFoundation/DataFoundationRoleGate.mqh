#ifndef __AL_SAED_V4_DATA_FOUNDATION_ROLE_GATE_MQH__
#define __AL_SAED_V4_DATA_FOUNDATION_ROLE_GATE_MQH__
#include "DataFoundationEnums.mqh"
class ALDataRoleGate {
public:
 static bool Allow(const AL_DATA_ROLE role,const AL_DATA_OPERATION operation,string &reason){
   if((operation==AL_OP_TRAIN || operation==AL_OP_TUNE) && role!=AL_ROLE_DEVELOPMENT){reason="protected_or_nondevelopment_cannot_train";return false;}
   if(operation==AL_OP_CALIBRATE && role!=AL_ROLE_CALIBRATION){reason="wrong_calibration_role";return false;}
   if(operation==AL_OP_SELECT && role!=AL_ROLE_SELECTION_VALIDATION){reason="wrong_selection_role";return false;}
   if(operation==AL_OP_PROMOTE && (role==AL_ROLE_SYNTHETIC_STRESS || role==AL_ROLE_EXTERNAL_STATIC)){reason="nonpositive_evidence_cannot_promote";return false;}
   reason="pass";return true;
 }
 static int ProtectionRank(const AL_DATA_ROLE role){
   if(role>=AL_ROLE_DEVELOPMENT && role<=AL_ROLE_LIVE)return (int)role;
   return -1;
 }
 static bool AllowDerivation(const AL_DATA_ROLE source,const AL_DATA_ROLE target,string &reason){
   int s=ProtectionRank(source),t=ProtectionRank(target);
   if(s>=0 && t>=0 && t<s){reason="backward_evidence_flow";return false;}
   reason="pass";return true;
 }
};
#endif
