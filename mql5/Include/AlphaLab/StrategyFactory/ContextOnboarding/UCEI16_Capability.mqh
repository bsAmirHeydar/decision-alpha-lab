#ifndef ALPHALAB_UCEI16_CAPABILITY_MQH
#define ALPHALAB_UCEI16_CAPABILITY_MQH
struct UCEI16_Capability { string capability_id; bool allowed; bool declared_exception; string reason; };
bool UCEI16_IsForbiddenCapability(const string id){ return id=="order_send" || id=="broker_write" || id=="network_fetch" || id=="future_data"; }
bool UCEI16_ValidateCapability(const UCEI16_Capability &c){ if(UCEI16_IsForbiddenCapability(c.capability_id) && c.allowed) return false; if(c.declared_exception && StringLen(c.reason)==0) return false; return true; }
#endif
