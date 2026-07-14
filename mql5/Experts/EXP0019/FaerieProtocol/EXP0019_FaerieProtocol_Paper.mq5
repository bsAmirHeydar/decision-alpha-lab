#property strict
#property version "1.000"
#property description "EXP0019 Faerie Protocol paper-only execution product. No broker mutation."
#include <AlphaLab/EXP0019/FaerieProtocol/I15/FP_I15_All.mqh>
input bool InpEnablePaperExecution=false;
input double InpFixedRiskAmount=100.0;
input double InpTargetRMultiple=2.0;
input double InpMaxSlippagePoints=1.0;
input FP_I15_POLICY_PROFILE InpPaperQuotaPolicy=FP_I15_POLICY_TWO_STAGE_FILLED;
input bool InpRequireI14DiagnosticAcceptance=true;
string g_status="CREATED";
int OnInit(){
 if(InpFixedRiskAmount<=0||InpTargetRMultiple<=0){Print("FP-I15 BLOCKED invalid risk inputs");return INIT_PARAMETERS_INCORRECT;}
 if(InpPaperQuotaPolicy==FP_I15_POLICY_UNSET){Print("FP-I15 BLOCKED paper policy unset");return INIT_PARAMETERS_INCORRECT;}
 EventSetTimer(1);g_status=(InpEnablePaperExecution?"PAPER_READY":"PAPER_DISABLED");
 Print("FP-I15 initialized authority=",FP_I15_Authority()," live_policy=",FP_I15_LivePolicy()," status=",g_status);
 return INIT_SUCCEEDED;
}
void OnTimer(){ if(!InpEnablePaperExecution)return; Comment("FP-I15 PAPER ONLY
Authority: ",FP_I15_Authority(),"
Live policy: ",FP_I15_LivePolicy(),"
Status: ",g_status,"
Awaiting canonical winner feed from I14/I09 composition."); }
void OnTick(){}
void OnDeinit(const int reason){EventKillTimer();Comment("");}
