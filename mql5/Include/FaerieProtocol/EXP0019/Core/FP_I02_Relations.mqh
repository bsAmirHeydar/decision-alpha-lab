#ifndef __EXP0019_FP_I02_RELATIONS_MQH__
#define __EXP0019_FP_I02_RELATIONS_MQH__

#include "FP_I02_Enums.mqh"

struct FP_I02_RelationDescriptor
  {
   FP_I02_RelationCode code;
   FP_I02_WindowKind reference_kind;
   FP_I02_WindowScope reference_scope;
   FP_I02_WindowKind check_kind;
   FP_I02_WindowScope check_scope;
   string quota_session;
   bool ww_gated;
   bool tradeable;
   bool directional_gate;
  };

int FP_I02_RelationCount() { return 7; }

bool FP_I02_GetRelation(const FP_I02_RelationCode code,FP_I02_RelationDescriptor &out)
  {
   ZeroMemory(out); out.code=code; out.tradeable=true;
   switch(code)
     {
      case FP_REL_AL: out.reference_kind=FP_WINDOW_A; out.reference_scope=FP_SCOPE_SAME_TRADING_DAY; out.check_kind=FP_WINDOW_L; out.check_scope=FP_SCOPE_SAME_TRADING_DAY; out.quota_session="L"; out.ww_gated=true; return true;
      case FP_REL_AN: out.reference_kind=FP_WINDOW_A; out.reference_scope=FP_SCOPE_SAME_TRADING_DAY; out.check_kind=FP_WINDOW_N; out.check_scope=FP_SCOPE_SAME_TRADING_DAY; out.quota_session="N"; out.ww_gated=true; return true;
      case FP_REL_LN: out.reference_kind=FP_WINDOW_L; out.reference_scope=FP_SCOPE_SAME_TRADING_DAY; out.check_kind=FP_WINDOW_N; out.check_scope=FP_SCOPE_SAME_TRADING_DAY; out.quota_session="N"; out.ww_gated=true; return true;
      case FP_REL_NA: out.reference_kind=FP_WINDOW_N; out.reference_scope=FP_SCOPE_EXACT_PRIOR_CALENDAR_OFFSET; out.check_kind=FP_WINDOW_A; out.check_scope=FP_SCOPE_CURRENT_TRADING_DAY; out.quota_session="A"; out.ww_gated=true; return true;
      case FP_REL_NL: out.reference_kind=FP_WINDOW_N; out.reference_scope=FP_SCOPE_EXACT_PRIOR_CALENDAR_OFFSET; out.check_kind=FP_WINDOW_L; out.check_scope=FP_SCOPE_CURRENT_TRADING_DAY; out.quota_session="L"; out.ww_gated=true; return true;
      case FP_REL_NN: out.reference_kind=FP_WINDOW_N; out.reference_scope=FP_SCOPE_EXACT_PRIOR_CALENDAR_OFFSET; out.check_kind=FP_WINDOW_N; out.check_scope=FP_SCOPE_CURRENT_TRADING_DAY; out.quota_session="N"; out.ww_gated=true; return true;
      case FP_REL_WW: out.reference_kind=FP_WINDOW_W; out.reference_scope=FP_SCOPE_PREVIOUS_COMPLETED_NY_WEEK; out.check_kind=FP_WINDOW_W; out.check_scope=FP_SCOPE_CURRENT_NY_WEEK; out.quota_session="SESSION_AT_ENTRY_ELIGIBILITY"; out.ww_gated=false; out.directional_gate=true; return true;
     }
   return false;
  }

bool FP_I02_RelationRegistryValid()
  {
   for(int i=0;i<FP_I02_RelationCount();i++)
     {
      FP_I02_RelationDescriptor descriptor;
      if(!FP_I02_GetRelation((FP_I02_RelationCode)i,descriptor)) return false;
      if(!descriptor.tradeable) return false;
      if(descriptor.code==FP_REL_WW && (!descriptor.directional_gate || descriptor.ww_gated)) return false;
      if(descriptor.code!=FP_REL_WW && descriptor.directional_gate) return false;
     }
   return true;
  }

#endif
