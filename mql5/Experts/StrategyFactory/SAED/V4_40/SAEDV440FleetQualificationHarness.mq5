#property strict
// SAEDV440 offline fleet qualification harness. It does not submit orders or activate capital.
#include <StrategyFactory/SAED/V4_40/SAEDV440Authority.mqh>
#include <StrategyFactory/SAED/V4_40/SAEDV440CellIdentity.mqh>
int OnInit(){ if(SAEDV440_LIVE_ORDER_SUBMISSION_ALLOWED!=0) return INIT_FAILED; if(SAEDV440_CAPITAL_ACTIVATION_ALLOWED!=0) return INIT_FAILED; return INIT_SUCCEEDED; }
void OnTick(){}
