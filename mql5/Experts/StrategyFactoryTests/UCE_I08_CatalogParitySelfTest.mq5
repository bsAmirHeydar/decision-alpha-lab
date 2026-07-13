#property strict
#include <AlphaLab/StrategyFactory/ClassicalAlgorithms/UCEI08_All.mqh>
int OnInit(){CUCEI08_Registry r;UCEI08_RegisterCatalog(r);string required[]={"never_trade@1.0.0","manual_threshold@1.0.0","logistic_regression@1.0.0","decision_tree_classifier@1.0.0","random_forest_classifier@1.0.0","gaussian_nb@1.0.0"};int failures=0;for(int i=0;i<ArraySize(required);i++){UCEI08_AlgorithmDescriptor d;if(!r.ResolveExact(required[i],d))failures++;}Print("UCE-I08 catalog parity failures=",failures);return failures==0?INIT_SUCCEEDED:INIT_FAILED;}
void OnTick(){}
