#ifndef ALPHALAB_UCEI06_MATURITY_MQH
#define ALPHALAB_UCEI06_MATURITY_MQH
#include "UCEI06_Contracts.mqh"
class CUCEI06MaturityEngine{
public:
 UCEI06_MaturityEvidence Evaluate(const UCEI06_OUTCOME_STATE state,const UCEI06_TERMINAL_REASON reason,const long observation_end_ms,const long required_end_ms)const{UCEI06_MaturityEvidence m;m.state=state;m.observation_end_ms=observation_end_ms;m.required_end_ms=required_end_ms;m.competing_event="";m.reason=IntegerToString((long)reason);m.event_observed=(state==UCEI06_RESOLVED);if(state==UCEI06_RESOLVED||state==UCEI06_REJECTED||(state==UCEI06_UNFILLED&&observation_end_ms>=required_end_ms)){m.censoring=0;m.mature=true;}else if((state==UCEI06_OPEN||state==UCEI06_CENSORED)&&observation_end_ms>=required_end_ms){m.state=UCEI06_CENSORED;m.censoring=1;m.mature=false;}else{m.state=UCEI06_UNRESOLVED;m.censoring=4;m.mature=false;}return m;}
};
#endif
