#ifndef ALPHALAB_UCEI15_CONTEXT_MQH
#define ALPHALAB_UCEI15_CONTEXT_MQH
bool UCEI15_KnownTimePass(const long event_ms,const long known_ms,const long causal_cut_ms){return(event_ms<=known_ms&&known_ms<=causal_cut_ms);}
bool UCEI15_ForbiddenFeature(const string name){return(name=="future_return"||name=="outcome_label"||name=="future_path");}
#endif
