#ifndef __FP_I14_ACCEPTANCE_GATE_MQH__
#define __FP_I14_ACCEPTANCE_GATE_MQH__
bool FP_I14_SourceAcceptance(const long mismatches,const bool authority_clean,const bool trace_complete,string &reason){if(!authority_clean){reason="FP_DIAG_AUTHORITY_VIOLATION";return false;}if(!trace_complete){reason="FP_DIAG_TRACE_INCOMPLETE";return false;}if(mismatches>0){reason="FP_DIAG_DIFFERENTIAL_MISMATCH";return false;}reason="FP_DIAG_SOURCE_ACCEPTED";return true;}
#endif
