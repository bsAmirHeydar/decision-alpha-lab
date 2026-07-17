#ifndef FP_SAEDV430HANDOFF_MQH
#define FP_SAEDV430HANDOFF_MQH
struct FP_SAEDV430Handoff { string handoff_id; string handoff_hash; string next_phase; bool research_only; bool promotion; bool runtime; bool execution; bool production; };
bool FP_SAEDV430HandoffValid(const FP_SAEDV430Handoff &value) { return(value.next_phase=="SAED_V4_31" && value.research_only && !value.promotion && !value.runtime && !value.execution && !value.production); }
#endif
