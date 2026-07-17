#ifndef FP_SAEDV430REPLAY_MQH
#define FP_SAEDV430REPLAY_MQH
struct FP_SAEDV430ReplayReceipt { string exact_replay_hash; int future_suffix_records_seen; bool deterministic; bool future_suffix_invariant; bool network_access; };
bool FP_SAEDV430ReplayValid(const FP_SAEDV430ReplayReceipt &value) { return(StringLen(value.exact_replay_hash)==64 && value.future_suffix_records_seen==0 && value.deterministic && value.future_suffix_invariant && !value.network_access); }
#endif
