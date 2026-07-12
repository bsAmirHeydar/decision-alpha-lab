#ifndef ALPHALAB_UCEI06_LABEL_COMPILER_MQH
#define ALPHALAB_UCEI06_LABEL_COMPILER_MQH
#include "UCEI06_Contracts.mqh"
#include "UCEI06_Identity.mqh"
class CUCEI06LabelCompiler{
public:
 double Metric(const UCEI06_OutcomeCell &c,const string name,bool &ok)const{ok=true;if(name=="net_r")return c.net_r;if(name=="net_pnl_cash")return c.net_pnl_cash;if(name=="mfe_r")return c.mfe_r;if(name=="mae_r")return c.mae_r;if(name=="max_drawdown_r")return c.max_drawdown_r;ok=false;return 0.0;}
 bool Compile(const UCEI06_OutcomeCell &c,const UCEI06_LabelTask &t,UCEI06_LabelRecord &out,string &reason)const{reason="";bool metric_ok=false;double v=Metric(c,t.metric,metric_ok);if(!metric_ok){reason="unknown_metric";return false;}out.opportunity_id=c.opportunity_id;out.treatment_id=c.treatment_id;out.task_key=t.task_id+"@"+t.version;out.cell_id=c.cell_id;out.mature=(!t.require_resolved||c.state==UCEI06_RESOLVED);out.mask=!out.mature;out.scalar_value=v;out.class_value=t.maximize?(v>=t.threshold):(v<=t.threshold);out.duration_ms=c.time_to_exit_ms;out.event_observed=(c.state==UCEI06_RESOLVED);out.competing_event=IntegerToString((long)c.terminal_reason);out.rank=0;out.sample_weight=1.0;out.known_time_ms=c.maturity.observation_end_ms;out.reason=out.mask?"maturity_gate":"";out.evidence_hash=UCEI06_StableId("uceevidence",c.cell_id+"|"+out.task_key);out.label_id=UCEI06_StableId("ucelabel",c.cell_id+"|"+out.task_key+"|"+IntegerToString((long)out.class_value));return true;}
};
#endif
