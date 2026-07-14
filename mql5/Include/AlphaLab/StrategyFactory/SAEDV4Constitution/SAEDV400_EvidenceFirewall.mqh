#ifndef __ALPHALAB_SAEDV400_EVIDENCE_FIREWALL_MQH__
#define __ALPHALAB_SAEDV400_EVIDENCE_FIREWALL_MQH__
#include "SAEDV400_Contracts.mqh"

class CSAEDV400EvidenceFirewall
  {
public:
   static bool IsTrainingLike(const ENUM_SAEDV400_EVIDENCE_OPERATION operation)
     {
      return(operation==SAEDV400_OPERATION_TRAIN || operation==SAEDV400_OPERATION_TUNE);
     }

   static bool IsProtected(const ENUM_SAEDV400_EVIDENCE_ROLE role)
     {
      return(role==SAEDV400_EVIDENCE_LOCKED_FINAL ||
             role==SAEDV400_EVIDENCE_PROSPECTIVE ||
             role==SAEDV400_EVIDENCE_SHADOW ||
             role==SAEDV400_EVIDENCE_MICRO_LIVE ||
             role==SAEDV400_EVIDENCE_LIVE ||
             role==SAEDV400_EVIDENCE_EXTERNAL_ACTUAL);
     }

   static bool IsAllowed(const ENUM_SAEDV400_EVIDENCE_ROLE role,
                         const ENUM_SAEDV400_EVIDENCE_OPERATION operation)
     {
      if(role==SAEDV400_EVIDENCE_DEVELOPMENT)
         return(operation==SAEDV400_OPERATION_TRAIN || operation==SAEDV400_OPERATION_TUNE || operation==SAEDV400_OPERATION_REPORT || operation==SAEDV400_OPERATION_REPLAY);
      if(role==SAEDV400_EVIDENCE_CALIBRATION)
         return(operation==SAEDV400_OPERATION_CALIBRATE || operation==SAEDV400_OPERATION_REPORT || operation==SAEDV400_OPERATION_REPLAY);
      if(role==SAEDV400_EVIDENCE_SELECTION_VALIDATION)
         return(operation==SAEDV400_OPERATION_SELECT || operation==SAEDV400_OPERATION_REPORT || operation==SAEDV400_OPERATION_REPLAY);
      if(role==SAEDV400_EVIDENCE_SYNTHETIC_STRESS)
         return(operation==SAEDV400_OPERATION_STRESS || operation==SAEDV400_OPERATION_REPORT || operation==SAEDV400_OPERATION_REPLAY);
      if(role==SAEDV400_EVIDENCE_EXTERNAL_STATIC)
         return(operation==SAEDV400_OPERATION_REPORT || operation==SAEDV400_OPERATION_REPLAY);
      if(role==SAEDV400_EVIDENCE_LIVE)
         return(operation==SAEDV400_OPERATION_REPORT || operation==SAEDV400_OPERATION_REPLAY);
      return(operation==SAEDV400_OPERATION_REPORT || operation==SAEDV400_OPERATION_PROMOTE || operation==SAEDV400_OPERATION_REPLAY);
     }

   static SAEDV400_Decision Evaluate(const SAEDV400_EvidenceRequest &request)
     {
      SAEDV400_Decision decision;
      decision.status=SAEDV400_DECISION_REJECT;
      decision.reason_code="authority_denied";
      decision.detail="Evidence operation is not allowed for role.";

      if((request.synthetic || request.evidence_role==SAEDV400_EVIDENCE_SYNTHETIC_STRESS) &&
         (request.positive_promotion_claim || request.operation==SAEDV400_OPERATION_PROMOTE))
        {
         decision.reason_code="synthetic_positive_promotion";
         decision.detail="Synthetic evidence may falsify but cannot positively promote.";
         return(decision);
        }
      if(IsProtected(request.evidence_role) && IsTrainingLike(request.operation))
        {
         decision.reason_code="protected_evidence_training";
         decision.detail="Protected evidence cannot feed training or adaptive search.";
         return(decision);
        }
      if(!IsAllowed(request.evidence_role,request.operation))
         return(decision);

      decision.status=SAEDV400_DECISION_ALLOW;
      decision.reason_code="ok";
      decision.detail="";
      return(decision);
     }
  };

#endif
