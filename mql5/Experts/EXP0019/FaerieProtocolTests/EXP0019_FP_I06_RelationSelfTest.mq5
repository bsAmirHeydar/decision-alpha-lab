#property strict
#include <AlphaLab/EXP0019/FaerieProtocol/I06/FP_I06_All.mqh>
int OnInit(){int failures=0;if(FP_I06_RelationRegistry::RelationCount()!=7)failures++;if(FP_I06_RelationRegistry::SupportedCount()!=6)failures++;if(!FP_I06_Engine::SameMinuteHasNoOrder())failures++;if(!FP_I06_Engine::WWDeferred())failures++;if(FP_I06_CandidateEngine::DirectionForSide(FP_I06_LOW)!=FP_I06_BULLISH)failures++;if(FP_I06_CandidateEngine::DirectionForSide(FP_I06_HIGH)!=FP_I06_BEARISH)failures++;Print("FP-I06 self-test failures=",failures);return failures==0?INIT_SUCCEEDED:INIT_FAILED;}
void OnTick(){}
