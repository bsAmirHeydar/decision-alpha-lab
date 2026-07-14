#ifndef FP_I15_ACCEPTANCE_GATE_MQH
#define FP_I15_ACCEPTANCE_GATE_MQH
bool FP_I15_SourceAccepted(const bool risk_cap,const bool sell_spread,const bool quota,const bool lifecycle,const bool restart){ return risk_cap&&sell_spread&&quota&&lifecycle&&restart; }
bool FP_I15_LiveReady(){ return false; }
#endif
