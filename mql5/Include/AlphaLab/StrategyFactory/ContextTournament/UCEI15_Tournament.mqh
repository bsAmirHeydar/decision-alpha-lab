#ifndef ALPHALAB_UCEI15_TOURNAMENT_MQH
#define ALPHALAB_UCEI15_TOURNAMENT_MQH
long UCEI15_DeclaredTrials(const int contexts,const int treatments,const int algorithms,const int folds){return((long)contexts*treatments*algorithms*folds);}
bool UCEI15_CountsPass(const long declared_count,const long executed_count,const long succeeded_count,const long failed_count){return(executed_count==succeeded_count+failed_count&&executed_count<=declared_count);}
#endif
