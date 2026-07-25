#property strict
#include <AlphaLab/StrategyFactory/TreatmentCompiler/UCEI04_All.mqh>
int OnInit(){UCEI04_ConformanceTelemetry t;string error;if(!UCEI04_RunConformance(t,error)){Print("UCE-I04 self-test FAIL: ",error);return INIT_FAILED;}if(t.failures!=0||t.compiler_cases<1||t.path_cases<1){Print("UCE-I04 self-test incomplete evidence");return INIT_FAILED;}Print("UCE-I04 self-test PASS");return INIT_SUCCEEDED;}
void OnTick(){}
