#ifndef ALPHALAB_UCEI16_SPECIFICATION_MQH
#define ALPHALAB_UCEI16_SPECIFICATION_MQH
#include "UCEI16_Types.mqh"
#include "UCEI16_Capability.mqh"
bool UCEI16_ValidVersion(const string v){ return StringLen(v)>=5 && StringFind(v,".")>0; }
bool UCEI16_ValidateContextSpec(const UCEI16_ContextSpec &s){ return StringLen(s.context_id)>0 && UCEI16_ValidVersion(s.version) && StringLen(s.doctrine_hash)==64 && StringLen(s.manual_policy_id)>0; }
#endif
