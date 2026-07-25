#property strict
#include <AlphaLab/StrategyFactory/ClassicalAlgorithms/UCEI08_All.mqh>
int OnInit(){int failures=0;CUCEI08_Registry r;UCEI08_RegisterCatalog(r);if(r.Size()<20)failures++;UCEI08_AlgorithmDescriptor d;if(!r.ResolveExact("logistic_regression@1.0.0",d))failures++;if(d.family!=UCEI08_FAMILY_LINEAR)failures++;if(!d.probability_output)failures++;if(r.Register(d))failures++;UCEI08_ClassicalGate g;g.state=UCEI08_GATE_PASS;g.has_baseline=true;g.has_linear=true;g.has_tree=true;g.probability_disclosed=true;g.optional_failures_clean=true;if(!g.Passed())failures++;if(UCEI08_ExplanationSelectionAllowed("final_test",true))failures++;Print("UCE-I08 self-test failures=",failures);return failures==0?INIT_SUCCEEDED:INIT_FAILED;}
void OnTick(){}
