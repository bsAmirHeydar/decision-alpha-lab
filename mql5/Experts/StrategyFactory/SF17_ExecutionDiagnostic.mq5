#property strict
#include <AlphaLab/StrategyFactory/Execution/SF17_AllExecution.mqh>
int OnInit(){SF17_ExecutionPolicy p=SF17_ReferencePolicy();string error;Print("SF17 policy hash: ",SF17_DerivePolicyHash(p));Print("SF17 policy valid: ",SF17_ValidatePolicy(p,error)," ",error);Print("SF17 authority: PAPER/SHADOW ONLY; broker API disabled");return INIT_SUCCEEDED;}
