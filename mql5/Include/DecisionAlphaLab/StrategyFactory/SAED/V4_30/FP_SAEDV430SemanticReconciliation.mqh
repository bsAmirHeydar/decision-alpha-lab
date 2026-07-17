#ifndef FP_SAEDV430SEMANTICRECONCILIATION_MQH
#define FP_SAEDV430SEMANTICRECONCILIATION_MQH
struct FP_SAEDV430SemanticReconciliation { int pair_count; int unique_semantic_hashes; bool all_match; };
bool FP_SAEDV430SemanticAccepted(const FP_SAEDV430SemanticReconciliation &value) { return(value.pair_count>=3 && value.unique_semantic_hashes==1 && value.all_match); }
#endif
