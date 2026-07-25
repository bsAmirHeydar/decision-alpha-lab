#ifndef ALPHALAB_ACL07_GATE_RESULT_MQH
#define ALPHALAB_ACL07_GATE_RESULT_MQH
#include "ACL07GateStatus.mqh"
struct ACL07GateResult { string gate_id; ENUM_ACL07_GATE_STATUS status; string reason_code; string evidence_digest; };
#endif
