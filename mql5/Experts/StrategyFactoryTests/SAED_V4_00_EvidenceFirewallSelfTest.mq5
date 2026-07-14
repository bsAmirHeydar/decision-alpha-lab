#property strict
#include <AlphaLab/StrategyFactory/SAEDV4Constitution/SAEDV400_All.mqh>

int OnInit()
  {
   SAEDV400_EvidenceRequest request;
   request.program_id="self-test";
   request.actor.actor_id="researcher";
   request.actor.actor_type=SAEDV400_ACTOR_HUMAN_RESEARCHER;
   request.actor.organization_unit="research";
   request.known_time=TimeCurrent();
   request.synthetic=false;
   request.positive_promotion_claim=false;

   request.evidence_role=SAEDV400_EVIDENCE_LOCKED_FINAL;
   request.operation=SAEDV400_OPERATION_TRAIN;
   SAEDV400_Decision decision=CSAEDV400EvidenceFirewall::Evaluate(request);
   if(decision.status!=SAEDV400_DECISION_REJECT || decision.reason_code!="protected_evidence_training")
      return(INIT_FAILED);

   request.evidence_role=SAEDV400_EVIDENCE_SYNTHETIC_STRESS;
   request.operation=SAEDV400_OPERATION_PROMOTE;
   request.synthetic=true;
   request.positive_promotion_claim=true;
   decision=CSAEDV400EvidenceFirewall::Evaluate(request);
   if(decision.status!=SAEDV400_DECISION_REJECT || decision.reason_code!="synthetic_positive_promotion")
      return(INIT_FAILED);
   return(INIT_SUCCEEDED);
  }

void OnTick() {}
