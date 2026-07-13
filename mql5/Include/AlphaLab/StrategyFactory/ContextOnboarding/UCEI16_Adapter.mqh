#ifndef ALPHALAB_UCEI16_ADAPTER_MQH
#define ALPHALAB_UCEI16_ADAPTER_MQH
struct UCEI16_LegacyAdapter { string adapter_id; string context_id; bool shared_treatment; bool shared_economics; bool shared_validation; bool shared_runtime; bool mutation_isolated; };
bool UCEI16_ValidateAdapter(const UCEI16_LegacyAdapter &a){ return StringLen(a.adapter_id)>0 && StringLen(a.context_id)>0 && a.shared_treatment && a.shared_economics && a.shared_validation && a.shared_runtime && a.mutation_isolated; }
#endif
