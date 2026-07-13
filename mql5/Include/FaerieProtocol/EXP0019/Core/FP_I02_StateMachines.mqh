#ifndef __EXP0019_FP_I02_STATE_MACHINES_MQH__
#define __EXP0019_FP_I02_STATE_MACHINES_MQH__

#include "FP_I02_Enums.mqh"

bool FP_I02_CandidateTransitionAllowed(const FP_I02_CandidateState from,const FP_I02_CandidateState to)
  {
   if(from==FP_CAND_OBSERVED) return to==FP_CAND_RAW || to==FP_CAND_INVALID_DATA;
   if(from==FP_CAND_RAW) return to==FP_CAND_CONFIRMED || to==FP_CAND_CANCELLED_SECOND_TOUCH || to==FP_CAND_EXPIRED_SESSION_DEADLINE || to==FP_CAND_INVALID_DATA;
   return false;
  }

bool FP_I02_ReferenceTransitionAllowed(const FP_I02_ReferenceState from,const FP_I02_ReferenceState to)
  {
   if(from==FP_REF_FRESH) return to==FP_REF_HUNTER_SEEN || to==FP_REF_CONSUMED_BY_PROTECTED_TOUCH || to==FP_REF_EXPIRED || to==FP_REF_SUPERSEDED;
   if(from==FP_REF_HUNTER_SEEN) return to==FP_REF_CONSUMED_BY_PROTECTED_TOUCH || to==FP_REF_EXPIRED || to==FP_REF_SUPERSEDED;
   if(from==FP_REF_CONSUMED_BY_PROTECTED_TOUCH) return to==FP_REF_EXPIRED || to==FP_REF_SUPERSEDED;
   return false;
  }

bool FP_I02_WWTransitionAllowed(const FP_I02_WWState from,const FP_I02_WWState to)
  {
   if(from==FP_WW_RAW) return to==FP_WW_CONFIRMED || to==FP_WW_INVALID_DATA || to==FP_WW_EXPIRED;
   if(from==FP_WW_CONFIRMED) return to==FP_WW_NEUTRALIZED || to==FP_WW_EXPIRED;
   if(from==FP_WW_NEUTRALIZED) return to==FP_WW_EXPIRED;
   return false;
  }

bool FP_I02_QuotaTransitionAllowed(const FP_I02_QuotaState from,const FP_I02_QuotaState to,const FP_I02_QuotaConsumptionPolicy policy)
  {
   if(from==FP_QUOTA_AVAILABLE) return to==FP_QUOTA_RESERVED;
   if(from==FP_QUOTA_RESERVED && to==FP_QUOTA_RELEASED) return true;
   if(from==FP_QUOTA_RESERVED && to==FP_QUOTA_CONSUMED) return policy!=FP_QUOTA_POLICY_UNSET;
   return false;
  }

#endif
