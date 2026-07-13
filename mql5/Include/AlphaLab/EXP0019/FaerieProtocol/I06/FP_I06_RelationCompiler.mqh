#ifndef __FP_I06_RELATION_COMPILER_MQH__
#define __FP_I06_RELATION_COMPILER_MQH__
#include "FP_I06_RelationRegistry.mqh"
class FP_I06_RelationCompiler { public: static bool ValidateInstance(const FP_I06_RelationInstance &v){ if(!v.Valid() || !FP_I06_RelationRegistry::IsSupported(v.relation)) return false; if(FP_I06_RelationRegistry::Historical(v.relation)) return v.calendar_offset>0; return v.calendar_offset==0; } static bool ValidatePlan(const FP_I06_RelationSidePlan &p){return p.Valid() && p.state==FP_I06_PLAN_ELIGIBLE;} };
#endif
