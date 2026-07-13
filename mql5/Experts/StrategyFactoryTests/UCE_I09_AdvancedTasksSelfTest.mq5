#property strict
#include <AlphaLab/StrategyFactory/AdvancedTasks/UCEI09_All.mqh>
int OnInit(){int failures=0;CUCEI09Registry registry;if(!registry.BuildDefault())failures++;registry.Freeze();if(!registry.Frozen() || registry.Count()!=18)failures++;UCEI09_AlgorithmDescriptor d;if(!registry.ResolveExact("pairwise_linear_ranker@1.0.0",d) || !d.Valid())failures++;UCEI09_QuantilePrediction q;q.prediction_id="q";q.row_id="r";q.evidence_hash="h";ArrayResize(q.levels,3);ArrayResize(q.values,3);q.levels[0]=0.1;q.levels[1]=0.5;q.levels[2]=0.9;q.values[0]=-1;q.values[1]=0;q.values[2]=1;if(!q.Valid())failures++;Print("UCE-I09 self-test failures=",failures);return failures==0?INIT_SUCCEEDED:INIT_FAILED;}
void OnTick(){}
