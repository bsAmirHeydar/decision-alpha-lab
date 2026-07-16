#property strict
#include <DecisionAlphaLab/StrategyFactory/SAED/V4_18/SAEDV418All.mqh>
int OnInit(){
 if(!SAEDV418TreatmentUniverseFrozen()) return INIT_FAILED;
 if(SAEDV418CanSelectLiveTreatment() || SAEDV418CanPromote() || SAEDV418CanActivateRuntime() || SAEDV418CanSendOrder()) return INIT_FAILED;
 if(SAEDV418RealTreatmentEffectClaim() || SAEDV418RealPolicyValueClaim() || SAEDV418TransportClaimAllowed()) return INIT_FAILED;
 return INIT_SUCCEEDED;
}
void OnTick(){}
