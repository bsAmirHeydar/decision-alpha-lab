#ifndef DECISION_ALPHA_LAB_SAED_V410_INTERPRETER_MQH
#define DECISION_ALPHA_LAB_SAED_V410_INTERPRETER_MQH
#include "SAEDV410Types.mqh"
bool SAEDV410StringCompare(const string actual,const string op,const string expected){
 if(op=="eq")return actual==expected;if(op=="ne")return actual!=expected;return false;
}
void SAEDV410InitTrace(SAEDV410Trace &trace,const string program_hash,const string fallback_node){trace.program_hash=program_hash;trace.projected_node_id=fallback_node;trace.matched_rule_id="";trace.reason_code="fallback_abstain";trace.selection_authority=false;trace.execution_authority=false;}
#endif
