#property strict
#include <AlphaLab/StrategyFactory/TreatmentCompiler/UCEI04_All.mqh>
input bool InpRunConformance=true;
int OnInit(){if(!InpRunConformance)return INIT_SUCCEEDED;UCEI04_ConformanceTelemetry t;string error;if(!UCEI04_RunConformance(t,error)){Print("UCE-I04 diagnostic failed: ",error);return INIT_FAILED;}PrintFormat("UCE-I04 PASS compiler=%d path=%d matrix=%d manual=%d",t.compiler_cases,t.path_cases,t.matrix_cases,t.manual_cases);return INIT_SUCCEEDED;}
void OnTick(){}
