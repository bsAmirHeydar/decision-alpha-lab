#ifndef FP_SAEDV430CHAIN_MQH
#define FP_SAEDV430CHAIN_MQH
struct FP_SAEDV430ChainEntry { int sequence; string previous_hash; string entry_hash; string chain; };
bool FP_SAEDV430ChainEntryShape(const FP_SAEDV430ChainEntry &value) { return(value.sequence>0 && StringLen(value.previous_hash)==64 && StringLen(value.entry_hash)==64 && StringLen(value.chain)>0); }
#endif
