#property strict
#include <AlphaLab/StrategyFactory/Governance/SF14_AllGovernance.mqh>
input bool InpPrintAuthorityBoundary=true;
int OnInit(){Print("SF14 Governance Diagnostic initialized. Registry and release artifacts remain no-execution-authority.");if(InpPrintAuthorityBoundary)Print("Phase 14 may register, validate, nominate, challenge, champion, suspend, retire and plan rollback; it cannot load ONNX or submit orders.");return INIT_SUCCEEDED;}
void OnTick(){}
