#ifndef FP_SAEDV430PROTOCOL_MQH
#define FP_SAEDV430PROTOCOL_MQH
struct FP_SAEDV430Protocol { string protocol_id; string protocol_hash; int minimum_labs; bool one_run_per_lab; bool semantic_hash_required; bool research_only; };
bool FP_SAEDV430ProtocolValid(const FP_SAEDV430Protocol &value) { return(value.minimum_labs>=3 && value.one_run_per_lab && value.semantic_hash_required && value.research_only); }
#endif
