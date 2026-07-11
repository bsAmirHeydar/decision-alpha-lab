#property strict
#property version "1.00"
#include <AlphaLab\StrategyFactory\Generation\SF05_AllGeneration.mqh>
int OnInit(){SF05_ResultSinkConfig s=SF05_DefaultResultSinkConfig();Print("SF05 sink_hash=",SF05_ResultSinkConfigHash(s)," mode=",(int)s.mode," append_only=",s.append_only);Print("SF05 generation states: ",SF05_GenerationStateToString(SF05_GENERATION_DRAFT)," -> ",SF05_GenerationStateToString(SF05_GENERATION_ACTIVE));return INIT_SUCCEEDED;}
