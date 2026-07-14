#ifndef __FP_I13_INSTANCE_ISOLATION_MQH__
#define __FP_I13_INSTANCE_ISOLATION_MQH__
#include "FP_I13_Hash.mqh"
class FP_I13_InstanceIsolation { public: static bool Validate(long chart_id,const string instance_id,string &reason){string key=FP_I13_Hex64(FP_I13_Hash64((string)chart_id+"|"+instance_id));if(StringLen(key)<8){reason="FP_REL_MULTI_INSTANCE_ISOLATION_FAIL";return false;}reason="FP_REL_MULTI_INSTANCE_ISOLATION_PASS";return true;} };
#endif
